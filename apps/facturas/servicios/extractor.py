import json
import os
import base64
from dotenv import load_dotenv
import litellm
from .prompt_extraccion import PROMPT_SISTEMA, EJEMPLOS
from ..domain.extractores import ExtractorOCR

load_dotenv()


class ExtractorGoogle(ExtractorOCR):
    """
    Implementación de ExtractorOCR usando Google Gemma vía OpenRouter.
    """

    def __init__(self):
        self.modelo = "openrouter/google/gemma-4-31b-it:free"
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_base = "https://openrouter.ai/api/v1"
        self._confianza_ultima = 0.0

    def extraer(self, imagen_bytes: bytes) -> dict:
        """
        Extrae datos de una imagen de factura.

        Args:
            imagen_bytes: contenido binario (PDF, JPG, PNG)

        Returns:
            dict con datos extraídos o error
        """
        try:
            contenido = base64.b64encode(imagen_bytes).decode("utf-8")

            # Determinar media_type (por ahora asumimos JPG, mejorable)
            media_type = "image/jpeg"

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
                model=self.modelo,
                messages=mensajes,
                max_tokens=1000,
                api_key=self.api_key,
                api_base=self.api_base,
            )

            texto = respuesta.choices[0].message.content.strip()
            if not texto:
                self._confianza_ultima = 0.0
                return {"extraccion_fallida": True, "error": "respuesta no válida del modelo"}

            texto = texto.replace("```json", "").replace("```", "").strip()

            try:
                datos = json.loads(texto)
            except json.JSONDecodeError:
                self._confianza_ultima = 0.0
                return {"extraccion_fallida": True, "error": "respuesta no válida del modelo"}

            campos_obligatorios = ["numero_factura", "fecha_emision", "nombre_emisor"]
            if not all(campo in datos for campo in campos_obligatorios):
                self._confianza_ultima = 0.5
                return {"extraccion_fallida": True, "error": "campos obligatorios ausentes"}

            self._confianza_ultima = 0.95
            return datos

        except Exception as e:
            self._confianza_ultima = 0.0
            return {"extraccion_fallida": True, "error": str(e)}

    def obtener_confianza(self) -> float:
        """Retorna confianza de la última extracción."""
        return self._confianza_ultima

    def obtener_modelo(self) -> str:
        """Retorna el nombre del modelo usado."""
        return self.modelo


def extraer_factura(ruta: str) -> dict:
    """
    Función legacy para compatibilidad con código existente.

    Recibe ruta a archivo y delega a ExtractorGoogle.
    """
    try:
        with open(ruta, "rb") as f:
            contenido = f.read()

        extractor = ExtractorGoogle()
        return extractor.extraer(contenido)

    except Exception as e:
        return {"extraccion_fallida": True, "error": str(e)}
