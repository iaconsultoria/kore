import json
import os
from litellm import completion
from django.conf import settings

api_key=settings.OPENROUTER_API_KEY,

SYSTEM_PROMPT = """
Eres un asistente que convierte texto libre en español a JSON estructurado para crear citas en un calendario.

Devuelve ÚNICAMENTE un objeto JSON válido, sin explicaciones ni texto adicional.

Los campos del JSON son:
- titulo (string): título breve de la cita
- inicio (string): fecha en formato YYYY-MM-DD
- hora_inicio (string|null): hora en formato HH:MM o null si no se menciona
- categoria_sugerida (string): una de estas — Cliente, Personal, Foco, Formación, Salud
- notas (string): información adicional relevante o cadena vacía

Si falta información imprescindible para crear la cita (como la fecha o el título), devuelve:
{"clarificacion_necesaria": "pregunta concreta para obtener el dato que falta"}

Ejemplos:

Entrada: "ponme reunión con Juan el lunes a las 10"
Salida: {"titulo": "Reunión con Juan", "inicio": "2026-06-02", "hora_inicio": "10:00", "categoria_sugerida": "Cliente", "notas": ""}

Entrada: "tengo revisión médica el 15 de junio a las 9 y media"
Salida: {"titulo": "Revisión médica", "inicio": "2026-06-15", "hora_inicio": "09:30", "categoria_sugerida": "Salud", "notas": ""}

Entrada: "bloquea el jueves por la tarde para trabajar en el informe"
Salida: {"titulo": "Trabajo en informe", "inicio": "2026-06-05", "hora_inicio": "16:00", "categoria_sugerida": "Foco", "notas": "Bloque de trabajo sin interrupciones"}
""".strip()

import json
import os
from datetime import date
from litellm import completion
from django.conf import settings

DIAS_SEMANA = {
    "Monday": "lunes",
    "Tuesday": "martes",
    "Wednesday": "miércoles",
    "Thursday": "jueves",
    "Friday": "viernes",
    "Saturday": "sábado",
    "Sunday": "domingo",
}

MESES = {
    "January": "enero", "February": "febrero", "March": "marzo",
    "April": "abril", "May": "mayo", "June": "junio",
    "July": "julio", "August": "agosto", "September": "septiembre",
    "October": "octubre", "November": "noviembre", "December": "diciembre",
}

SYSTEM_PROMPT = """..."""  # el tuyo sin cambios


def parsear_texto_a_cita(texto: str) -> dict:
    hoy = date.today()
    dia_semana = DIAS_SEMANA[hoy.strftime("%A")]
    mes = MESES[hoy.strftime("%B")]
    prompt = SYSTEM_PROMPT + f"\n\nFecha de hoy: {hoy.strftime('%Y-%m-%d')} ({dia_semana} {hoy.day} de {mes} de {hoy.year}). Usa esta fecha como referencia para calcular cualquier expresión temporal."

    response = completion(
        model="openrouter/z-ai/glm-4.5-air:free",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": texto},
        ],
        api_key=settings.OPENROUTER_API_KEY,
    )

    contenido = response.choices[0].message.content.strip()

    if contenido.startswith("```"):
        contenido = contenido.split("```")[1]
        if contenido.startswith("json"):
            contenido = contenido[4:]

    return json.loads(contenido)