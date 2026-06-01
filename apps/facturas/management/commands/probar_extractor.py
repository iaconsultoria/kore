import json
import time
from django.core.management.base import BaseCommand
from apps.facturas.servicios.extractor import extraer_factura


class Command(BaseCommand):
    help = "Prueba el extractor de facturas con un archivo dado"

    def add_arguments(self, parser):
        parser.add_argument("ruta", type=str, help="Ruta al archivo de factura")

    def handle(self, *args, **options):
        ruta = options["ruta"]

        inicio = time.time()
        datos = extraer_factura(ruta)
        tiempo = time.time() - inicio

        self.stdout.write(json.dumps(datos, indent=2, ensure_ascii=False))
        self.stdout.write(f"\nTiempo: {tiempo:.2f}s")
        self.stdout.write(f"Modelo: openrouter/google/gemma-4-31b-it:free")
        self.stdout.write(f"Coste estimado: €0.00 (modelo gratuito OpenRouter)")
