import json
import os
import base64
from dotenv import load_dotenv
import litellm
from .prompt_extraccion import PROMPT_SISTEMA, EJEMPLOS

load_dotenv()


def extraer_factura(ruta: str) -> dict:
    """
    Recibe la ruta a un archivo de factura PDF, JPG o PNG
    y devuelve un diccionario con los campos extraídos vía LiteLLM.
    """
    with open(ruta, "rb") as f:
        contenido = base64.b64encode(f.read()).decode("utf-8")

    extension = os.path.splitext(ruta)[1].lower()
    media_types = {
        ".pdf": "application/pdf",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
    }
    media_type = media_types.get(extension, "image/jpeg")

    mensajes = [{"role": "system", "content": PROMPT_SISTEMA}]
    for ejemplo in EJEMPLOS:
        mensajes.append({"role": ejemplo["role"], "content": ejemplo["content"]})

    mensajes.append({
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{media_type};base64,{contenido}"
                }
            }
        ]
    })

    respuesta = litellm.completion(
        model="openrouter/google/gemma-4-31b-it:free",
        messages=mensajes,
        max_tokens=1000,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1",
    )

    texto = respuesta.choices[0].message.content.strip()
    texto = texto.replace("```json", "").replace("```", "").strip()

    datos = json.loads(texto)
    return datos
