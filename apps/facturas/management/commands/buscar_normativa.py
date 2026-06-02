import os
import litellm
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from pgvector.django import CosineDistance
from apps.facturas.models import FragmentoNormativa

load_dotenv()

UMBRAL_DISTANCIA = 0.70


class Command(BaseCommand):
    help = "Busca fragmentos de normativa relevantes dado un texto de gasto"

    def add_arguments(self, parser):
        parser.add_argument("texto", type=str, help="Texto del gasto a consultar")

    def handle(self, *args, **options):
        texto = options["texto"]

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

        # Debug temporal que muestra distancias de los resultados
        for f in fragmentos:
            self.stdout.write(f"DEBUG distancia: {f.distancia:.4f} | {f.fuente[:60]}")

        # Comprobar umbral con el resultado más cercano
        if not fragmentos or fragmentos[0].distancia > UMBRAL_DISTANCIA:
            self.stdout.write("Sin normativa relevante encontrada")
            return

        self.stdout.write(f"\nConsulta: {texto}\n")
        for i, f in enumerate(fragmentos, 1):
            self.stdout.write(f"--- Resultado {i} (distancia: {f.distancia:.4f}) ---")
            self.stdout.write(f"Fuente: {f.fuente}")
            self.stdout.write(f"Texto: {f.texto[:200]}...\n")
