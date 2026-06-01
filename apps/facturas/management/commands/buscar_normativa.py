import os
import litellm
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from pgvector.django import CosineDistance
from apps.facturas.models import FragmentoNormativa

load_dotenv()


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

        fragmentos = FragmentoNormativa.objects.order_by(
            CosineDistance("embedding", embedding)
        )[:3]

        self.stdout.write(f"\nConsulta: {texto}\n")
        for i, f in enumerate(fragmentos, 1):
            self.stdout.write(f"--- Resultado {i} ---")
            self.stdout.write(f"Fuente: {f.fuente}")
            self.stdout.write(f"Texto: {f.texto[:200]}...\n")
