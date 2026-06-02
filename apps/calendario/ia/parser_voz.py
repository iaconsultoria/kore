from datetime import datetime, timedelta
import re
import json  
from litellm import completion  
from django.conf import settings

SYSTEM_PROMPT = """
Eres un asistente que convierte texto libre en español a JSON estructurado para crear citas en un calendario.

Devuelve ÚNICAMENTE un objeto JSON válido.

Los campos del JSON son:
- titulo (string)
- inicio (string): YYYY-MM-DD
- hora_inicio (string|null): HH:MM
- categoria_sugerida (string)
- notas (string)

IMPORTANTE:
- La fecha y hora ya han sido interpretadas previamente y se te proporcionan.
- Usa EXACTAMENTE los valores de inicio y hora_inicio que se te dan. No los recalcules.
- Si no hay un título claro en el texto, devuelve: {"clarificacion_necesaria": "pregunta"}

Ejemplos:

Entrada: "ponme reunión con Juan el lunes a las 10"
Fecha detectada: inicio=2026-06-09, hora_inicio=10:00
Salida: {"titulo": "Reunión con Juan", "inicio": "2026-06-09", "hora_inicio": "10:00", "categoria_sugerida": "Cliente", "notas": ""}

Entrada: "tengo revisión médica el 15 de junio a las 9 y media"
Fecha detectada: inicio=2026-06-15, hora_inicio=09:30
Salida: {"titulo": "Revisión médica", "inicio": "2026-06-15", "hora_inicio": "09:30", "categoria_sugerida": "Salud", "notas": ""}

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
import unicodedata

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

    # Detectar día de la semana
    for nombre, numero in DIAS_SEMANA.items():
        if nombre in texto:
            dias_hasta = (numero - ahora.weekday()) % 7
            if dias_hasta == 0:
                dias_hasta = 7
            fecha = ahora + timedelta(days=dias_hasta)
            break

    # Detectar hora — "a las" o "a la" es OBLIGATORIO
    match_hora = re.search(
        r"(?:a las|a la)\s*(\d{1,2})(?::(\d{2}))?",
        texto
    )

    if match_hora:
        hora_num = int(match_hora.group(1))
        if 0 <= hora_num <= 23:
            minutos = match_hora.group(2) or "00"
            hora = f"{hora_num:02}:{minutos}"

    inicio = fecha.strftime("%Y-%m-%d") if fecha else None

    return inicio, hora

def parsear_texto_a_cita(texto: str) -> dict:
    inicio, hora_inicio = extraer_fecha(texto)

    contexto_fecha = f"""
Fecha detectada automáticamente:
- inicio: {inicio}
- hora_inicio: {hora_inicio}

NO recalcules estas fechas.
""".strip()

    response = completion(
        model="openrouter/z-ai/glm-4.5-air:free",
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

    # FORZAR fecha/hora correctas
    resultado["inicio"] = inicio
    resultado["hora_inicio"] = hora_inicio

    return resultado