import os
import litellm
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from apps.facturas.models import FragmentoNormativa

load_dotenv()

FRAGMENTOS = [
    {
        "fuente": "AEAT - Income Tax Self-Employed - Deductible Expenses",
        "texto": "Self-employed workers in direct estimation can deduct necessary expenses for their economic activity. Deductible expenses include: operating costs, salaries, social security contributions, rental and fees, repairs and maintenance, professional services, other external services, deductible taxes, financial expenses and depreciation. For an expense to be deductible it must be linked to the activity, be properly documented and be registered in the accounting."
    },
    {
        "fuente": "AEAT - VAT - Deductible Quotas",
        "texto": "VAT taxpayers may deduct quotas paid in the acquisition of goods and services intended for the performance of taxed and non-exempt operations. To exercise the right to deduction it is necessary to be in possession of the original invoice, that the quotas are properly accounted for and that the deduction is made in the return corresponding to the period in which the quotas were incurred or in the following four years."
    },
    {
        "fuente": "AEAT - Income Tax - Non-Deductible Expenses",
        "texto": "The following shall not be considered fiscally deductible expenses: fines and criminal and administrative sanctions, default surcharge and surcharge for late submission of returns and self-assessments, gambling losses, gifts and liberalities, expenses for client or supplier attention exceeding 1 percent of net turnover for the tax period, and expenses with persons or entities resident in tax havens."
    },
    {
        "fuente": "AEAT - VAT - Tax Rates",
        "texto": "Value Added Tax is applied in Spain with three tax rates: the general rate of 21 percent applicable to most goods and services, the reduced rate of 10 percent applicable to non-basic food, passenger transport and hospitality, and the super-reduced rate of 4 percent applicable to basic food, books, newspapers and medicines. There are also certain VAT-exempt operations such as medical, educational and financial services."
    },
    {
        "fuente": "AEAT - Income Tax - Self-Employed Social Security",
        "texto": "Social Security contributions paid by the self-employed worker are deductible in Income Tax. This includes both the monthly self-employed contribution and the contributions for contracted workers. Contributions to the Special Regime for Self-Employed Workers are deductible in full as an expense of the economic activity, provided they are duly credited and registered."
    },
    {
        "fuente": "AEAT - Income Tax - Employee Food Allowances and Allowances",
        "texto": "Employee meal allowances and travel allowances for work are deductible when paid to employees for reasons of their work and within the limits established by regulations. Daily allowances for employees on business travel can be deductible when they comply with the requirements of amount and documentation, provided they do not constitute salary remuneration but reimbursement of expenses."
    },
    {
        "fuente": "AEAT - Income Tax - Client Representation and Hospitality Expenses",
        "texto": "Public relations expenses with clients or suppliers may be deductible when directly related to the economic activity and properly documented, without prejudice to the limitations applicable to gifts. These expenses must be reasonable in amount and justified by the business nature of the relationship with clients and suppliers."
    },
    {
        "fuente": "AEAT - Income Tax - Partially Used Housing Supplies",
        "texto": "When the habitual residence is partially used for economic activity, supply expenses can be deducted in the percentage corresponding to the square meters allocated to the activity, in accordance with legal provisions. Proper documentation of the allocation percentage and calculation of the deductible portion is required."
    },
    {
        "fuente": "AEAT - Income Tax - Vehicles Allocated to Activity",
        "texto": "Passenger vehicles are considered allocated to economic activity only when their use is exclusive to the activity, except for exceptions expressly provided for in Income Tax regulations. Mixed-use vehicles require documentation demonstrating the allocation percentage to the activity."
    },
    {
        "fuente": "AEAT - Income Tax - Fuel and Maintenance Expenses",
        "texto": "Fuel, maintenance, repair, insurance and other expenses associated with vehicles allocated to economic activity may be deductible when there is exclusive allocation and adequate documentary evidence. Records of mileage and maintenance are required to justify the allocation and amount of deductible expenses."
    },
    {
        "fuente": "AEAT - Income Tax - Professional Training",
        "texto": "Professional training expenses are deductible when directly related to the economic activity developed and contribute to the updating or improvement of professional skills. Training expenses must be properly documented and directly related to the current or future professional activity."
    },
    {
        "fuente": "AEAT - Income Tax - Insurance Premiums",
        "texto": "Insurance premiums related to economic activity, such as civil liability, fire, theft or others affecting assets allocated to the activity, can be considered deductible expenses. Professional liability insurance and all insurances protecting assets used in the activity qualify as deductible."
    },
    {
        "fuente": "AEAT - Income Tax - Office Material and Consumables",
        "texto": "Expenses for office materials, computer consumables and elements necessary for the development of economic activity can be deductible provided they are properly documented and linked to the activity. Small materials, stationery, printing and similar expenses qualify as deductible supplies."
    },
    {
        "fuente": "AEAT - Income Tax - Computer Equipment and Depreciation",
        "texto": "Computer equipment and investment assets allocated to economic activity can be deducted through depreciation according to officially approved schedules or according to applicable tax treatment. Depreciation rates are defined based on the estimated useful life of each asset."
    },
    {
        "fuente": "AEAT - Income Tax - Rental of Premises and Coworking",
        "texto": "Expenses arising from the rental of premises, offices or coworking spaces allocated to economic activity are considered deductible expenses when there is documentary evidence and allocation to the activity. Lease agreements and proof of payment are required to justify the deduction."
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
