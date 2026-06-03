import os
import litellm
from pgvector.django import CosineDistance
from .models import FragmentoNormativa

UMBRAL_DISTANCIA = 0.70


def buscar_normativa_por_texto(texto):
    """
    Busca fragmentos de normativa relevantes para un texto.
    Retorna lista de hasta 3 fragmentos si la distancia del más cercano está bajo el umbral.
    Si no, retorna lista vacía.
    """
    respuesta = litellm.embedding(
        model="openrouter/nvidia/llama-nemotron-embed-vl-1b-v2:free",
        input=[texto],
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1",
    )
    embedding = respuesta.data[0]["embedding"]

    fragmentos = (
        FragmentoNormativa.objects
        .annotate(distancia=CosineDistance("embedding", embedding))
        .order_by("distancia")[:3]
    )

    # Si no hay fragmentos o el más cercano supera el umbral, retorna vacío
    if not fragmentos or fragmentos[0].distancia > UMBRAL_DISTANCIA:
        return []

    return list(fragmentos)


def sugerir_categoria(proveedor_nombre, lineas):
    """
    Sugiere una categoría de gasto basada en proveedor y líneas de factura.
    Retorna el nombre sugerido o None si no puede sugerir.
    """
    concepto = lineas[0].concepto if lineas else "gasto"

    prompt = f"Proveedor: {proveedor_nombre}\nConcepto: {concepto}\n\nSugiere una sola categoría de gasto (máximo 5 palabras). Solo la categoría, sin explicación."

    respuesta = litellm.completion(
        model="openrouter/google/gemma-4-31b-it:free",
        messages=[{"role": "user", "content": prompt}],
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1",
    )

    return respuesta.choices[0].message.content.strip()
