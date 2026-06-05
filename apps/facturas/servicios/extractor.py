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
    try:
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
        if not texto:
            return {"extraccion_fallida": True, "error": "respuesta no válida del modelo"}

        texto = texto.replace("```json", "").replace("```", "").strip()

        try:
            datos = json.loads(texto)
        except json.JSONDecodeError:
            return {"extraccion_fallida": True, "error": "respuesta no válida del modelo"}

        campos_obligatorios = ["proveedor", "numero_factura", "fecha_factura"]
        if not all(campo in datos for campo in campos_obligatorios):
            return {"extraccion_fallida": True, "error": "campos obligatorios ausentes"}

        return datos

    except Exception as e:
        return {"extraccion_fallida": True, "error": str(e)}
