import os
import litellm
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from apps.facturas.models import FragmentoNormativa

load_dotenv()

FRAGMENTOS = [
    {
        "fuente": "AEAT - IRPF Autónomos - Gastos deducibles",
        "texto": "Los autónomos en estimación directa pueden deducir los gastos necesarios para el desarrollo de su actividad económica. Entre los gastos deducibles se encuentran: consumos de explotación, sueldos y salarios, seguridad social a cargo de la empresa, arrendamientos y cánones, reparaciones y conservación, servicios de profesionales independientes, otros servicios exteriores, tributos fiscalmente deducibles, gastos financieros y amortizaciones. Para que un gasto sea deducible debe estar vinculado a la actividad, estar justificado documentalmente y estar registrado en la contabilidad."
    },
    {
        "fuente": "AEAT - IVA - Cuotas deducibles",
        "texto": "Los sujetos pasivos del IVA podrán deducir las cuotas soportadas en la adquisición de bienes y servicios destinados a la realización de operaciones sujetas y no exentas. Para ejercer el derecho a la deducción es necesario estar en posesión de la factura original, que las cuotas estén debidamente contabilizadas y que la deducción se efectúe en la declaración-liquidación correspondiente al período en que se soportaron las cuotas o en los siguientes cuatro años."
    },
    {
        "fuente": "AEAT - IRPF - Gastos no deducibles",
        "texto": "No tendrán la consideración de gastos fiscalmente deducibles: las multas y sanciones penales y administrativas, el recargo de apremio y el recargo por presentación fuera de plazo de declaraciones-liquidaciones y autoliquidaciones, las pérdidas del juego, los donativos y liberalidades, los gastos de atenciones a clientes o proveedores que superen el 1 por ciento del importe neto de la cifra de negocios del período impositivo, y los gastos realizados con personas o entidades residentes en paraísos fiscales."
    },
    {
        "fuente": "AEAT - IVA - Tipos impositivos",
        "texto": "El Impuesto sobre el Valor Añadido se aplica en España con tres tipos impositivos: el tipo general del 21 por ciento aplicable a la mayoría de bienes y servicios, el tipo reducido del 10 por ciento aplicable entre otros a alimentos no básicos, transporte de viajeros y hostelería, y el tipo superreducido del 4 por ciento aplicable a alimentos básicos, libros, periódicos y medicamentos. Existen además determinadas operaciones exentas de IVA como los servicios médicos, educativos y financieros."
    },
    {
        "fuente": "AEAT - IRPF - Seguridad Social autónomos",
        "texto": "Las cuotas de la Seguridad Social abonadas por el trabajador autónomo son gasto deducible en el IRPF. Esto incluye tanto la cuota de autónomos mensual como las cuotas de los trabajadores que tenga contratados. Las cuotas satisfechas por el autónomo al Régimen Especial de Trabajadores Autónomos son deducibles en su totalidad como gasto de la actividad económica, siempre que estén debidamente acreditadas y registradas."
    },
]


class Command(BaseCommand):
    help = "Ingesta fragmentos de normativa AEAT con embeddings en la base de datos"

    def handle(self, *args, **options):
        FragmentoNormativa.objects.all().delete()
        self.stdout.write("Fragmentos anteriores eliminados.")

        for fragmento in FRAGMENTOS:
            respuesta = litellm.embedding(
                model="openrouter/nvidia/llama-nemotron-embed-vl-1b-v2:free",
                input=[fragmento["texto"]],
                api_key=os.getenv("OPENROUTER_API_KEY"),
                api_base="https://openrouter.ai/api/v1",
            )
            embedding = respuesta.data[0]["embedding"]

            FragmentoNormativa.objects.create(
                texto=fragmento["texto"],
                fuente=fragmento["fuente"],
                embedding=embedding,
            )
            self.stdout.write(f"Fragmento ingresado: {fragmento['fuente']}")

        self.stdout.write("Ingestión completada.")
