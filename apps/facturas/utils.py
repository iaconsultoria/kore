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
