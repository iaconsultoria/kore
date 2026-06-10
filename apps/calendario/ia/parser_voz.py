from datetime import datetime, timedelta
import re
import json
import time
import unicodedata
from litellm import completion
from litellm.exceptions import RateLimitError
from django.conf import settings

SYSTEM_PROMPT = """
Eres un asistente que convierte texto libre en español a JSON estructurado para crear citas en un calendario.

Devuelve ÚNICAMENTE un objeto JSON válido.

Los campos del JSON son:
- titulo (string)
- inicio (string): YYYY-MM-DD
- hora_inicio (string|null): HH:MM
- categoria_sugerida (string)
- anotaciones (string)

IMPORTANTE:
- La fecha y hora ya han sido interpretadas previamente y se te proporcionan.
- Usa EXACTAMENTE los valores de inicio y hora_inicio que se te dan. No los recalcules.
- Si no hay un título claro en el texto, devuelve: {"clarificacion_necesaria": "pregunta"}

Ejemplos:

Entrada: "ponme reunión con Juan el lunes a las 10"
Fecha detectada: inicio=2026-06-09, hora_inicio=10:00
Salida: {"titulo": "Reunión con Juan", "inicio": "2026-06-09", "hora_inicio": "10:00", "categoria_sugerida": "Cliente", "anotaciones": ""}

Entrada: "tengo revisión médica el 15 de junio a las 9 y media"
Fecha detectada: inicio=2026-06-15, hora_inicio=09:30
Salida: {"titulo": "Revisión médica", "inicio": "2026-06-15", "hora_inicio": "09:30", "categoria_sugerida": "Salud", "anotaciones": ""}

Entrada: "el lunes a las 10"
Fecha detectada: inicio=2026-06-09, hora_inicio=10:00
Salida: {"clarificacion_necesaria": "¿Para qué es la cita del lunes a las 10?"}
""".strip()

DIAS_SEMANA = {
    "lunes": 0,
    "martes": 1,
    "miercoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sabado": 5,
    "domingo": 6,
}

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}


def quitar_tildes(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def extraer_fecha(texto: str):
    print(">>> extraer_fecha llamada con:", repr(texto))
    texto = quitar_tildes(texto.lower())
    ahora = datetime.now()
    fecha = None
    hora = None

    # ── Fechas relativas ──────────────────────────────────────────────────
    if "pasado manana" in texto:
        fecha = ahora + timedelta(days=2)
    elif "manana" in texto:
        fecha = ahora + timedelta(days=1)
    elif "hoy" in texto:
        fecha = ahora
    elif "en dos semanas" in texto or "dentro de dos semanas" in texto:
        fecha = ahora + timedelta(weeks=2)
    elif "en una semana" in texto or "dentro de una semana" in texto:
        fecha = ahora + timedelta(weeks=1)
    elif "la semana que viene" in texto or "la proxima semana" in texto:
        dias_hasta_lunes = (7 - ahora.weekday()) % 7 or 7
        fecha = ahora + timedelta(days=dias_hasta_lunes)

    # ── Día de la semana (solo si no se detectó fecha relativa) ──────────
    if fecha is None:
        for nombre, numero in DIAS_SEMANA.items():
            if nombre in texto:
                dias_hasta = (numero - ahora.weekday()) % 7
                if dias_hasta == 0:
                    dias_hasta = 7
                fecha = ahora + timedelta(days=dias_hasta)
                break

    # ── Fecha explícita "dd de mes" ───────────────────────────────────────
    if fecha is None:
        m = re.search(r"(\d{1,2})\s+de\s+([a-z]+)", texto)
        if m:
            mes = MESES.get(quitar_tildes(m.group(2)))
            if mes:
                dia = int(m.group(1))
                anio = ahora.year
                candidata = datetime(anio, mes, dia)
                if candidata.date() < ahora.date():
                    candidata = datetime(anio + 1, mes, dia)
                fecha = candidata

    # ── Fecha explícita dd/mm(/yyyy) ──────────────────────────────────────
    if fecha is None:
        m = re.search(r"(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?", texto)
        if m:
            anio = int(m.group(3)) if m.group(3) else ahora.year
            if anio < 100:
                anio += 2000
            fecha = datetime(anio, int(m.group(2)), int(m.group(1)))

    # ── Hora ──────────────────────────────────────────────────────────────
    if "mediodia" in texto:
        hora = "12:00"
    elif "medianoche" in texto:
        hora = "00:00"
    elif "por la manana" in texto and not re.search(r"(?:a las|a la)\s*\d", texto):
        hora = "09:00"
    elif "por la tarde" in texto and not re.search(r"(?:a las|a la)\s*\d", texto):
        hora = "16:00"
    elif "por la noche" in texto and not re.search(r"(?:a las|a la)\s*\d", texto):
        hora = "20:00"
    else:
        m = re.search(r"(?:a las|a la)\s*(\d{1,2})(?::(\d{2}))?", texto)
        if m:
            hora_num = int(m.group(1))
            if 0 <= hora_num <= 23:
                minutos = m.group(2) or "00"
                hora = f"{hora_num:02}:{minutos}"

    inicio = fecha.strftime("%Y-%m-%d") if fecha else None
    return inicio, hora


def _completion_con_retry(model, messages, api_key, intentos=3):
    modelos = [model, "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"]
    for modelo_actual in modelos:
        for i in range(intentos):
            try:
                return completion(model=modelo_actual, messages=messages, api_key=api_key)
            except RateLimitError as e:
                if i < intentos - 1:
                    try:
                        import re as _re
                        segundos = int(_re.search(r'"retry_after_seconds":(\d+)', str(e)).group(1))
                    except Exception:
                        segundos = 30
                    print(f"Rate limit en {modelo_actual}, esperando {segundos}s (intento {i+1}/{intentos})")
                    time.sleep(segundos)
                else:
                    print(f"Rate limit agotado en {modelo_actual}, probando siguiente modelo...")
                    break
    raise Exception("Todos los modelos están saturados, inténtalo en unos minutos.")


def parsear_texto_a_cita(texto: str) -> dict:
    inicio, hora_inicio = extraer_fecha(texto)

    contexto_fecha = f"""
Fecha detectada automáticamente:
- inicio: {inicio}
- hora_inicio: {hora_inicio}

NO recalcules estas fechas.
""".strip()

    response = _completion_con_retry(
        model="openrouter/openai/gpt-oss-120b:free",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"{contexto_fecha}\n\nTexto original: {texto}",
            },
        ],
        api_key=settings.OPENROUTER_API_KEY,
    )

    contenido = response.choices[0].message.content.strip()

    if contenido.startswith("```"):
        contenido = contenido.split("```")[1]
        if contenido.startswith("json"):
            contenido = contenido[4:]

    resultado = json.loads(contenido)

    resultado["inicio"] = inicio
    resultado["hora_inicio"] = hora_inicio

    return resultado