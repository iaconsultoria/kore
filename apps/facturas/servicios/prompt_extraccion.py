PROMPT_SISTEMA = """
Eres un asistente especializado en extraer datos de facturas españolas.
Devuelve ÚNICAMENTE un JSON con estos campos:
{
  "numero_factura": string,
  "fecha_emision": "YYYY-MM-DD",
  "nif_emisor": string,
  "nombre_emisor": string,
  "base_imponible": decimal,
  "iva_porcentaje": entero,
  "iva_total": decimal,
  "total": decimal
}
Si no encuentras un campo, usa null. Sin texto adicional, solo el JSON.
"""

EJEMPLOS = [
    {
        "role": "user",
        "content": "Factura nº F-2024-001, emitida el 15/01/2024 por Servicios Informáticos SL (CIF B12345678). Base imponible: 1.000,00 €, IVA 21%: 210,00 €, Total: 1.210,00 €."
    },
    {
        "role": "assistant",
        "content": '{"numero_factura":"F-2024-001","fecha_emision":"2024-01-15","nif_emisor":"B12345678","nombre_emisor":"Servicios Informáticos SL","base_imponible":1000.00,"iva_porcentaje":21,"iva_total":210.00,"total":1210.00}'
    },
    {
        "role": "user",
        "content": "Factura 2024/42, fecha 03-03-2024. Emisor: Juan García Pérez, NIF 12345678A. Base: 500,00 €. IVA 21%: 105,00 €. Total: 605,00 €."
    },
    {
        "role": "assistant",
        "content": '{"numero_factura":"2024/42","fecha_emision":"2024-03-03","nif_emisor":"12345678A","nombre_emisor":"Juan García Pérez","base_imponible":500.00,"iva_porcentaje":21,"iva_total":105.00,"total":605.00}'
    },
    {
        "role": "user",
        "content": "Fra. A-2024-0089, 28/06/2024. Proveedor: Consultoría Digital SA, CIF A87654321. Base imponible: 2.500,00 €. IVA (21%): 525,00 €. Total a pagar: 3.025,00 €."
    },
    {
        "role": "assistant",
        "content": '{"numero_factura":"A-2024-0089","fecha_emision":"2024-06-28","nif_emisor":"A87654321","nombre_emisor":"Consultoría Digital SA","base_imponible":2500.00,"iva_porcentaje":21,"iva_total":525.00,"total":3025.00}'
    },
    {
        "role": "user",
        "content": "Factura simplificada: Ref. S-2024-156, 10/05/2024. Emitida por TecnoSoluciones Ltd, NIF W98765432. Total: 850,00 €. (IVA incluido, sin desglose)."
    },
    {
        "role": "assistant",
        "content": '{"numero_factura":"S-2024-156","fecha_emision":"2024-05-10","nif_emisor":"W98765432","nombre_emisor":"TecnoSoluciones Ltd","base_imponible":null,"iva_porcentaje":null,"iva_total":null,"total":850.00}'
    },
    {
        "role": "user",
        "content": "Factura 2024-045, emitida 22/04/2024. Proveedor: Supplies & Co, CIF D11223344. Items: Cables USB (5x 12,50€ = 62,50€), Conectores (10x 8,00€ = 80,00€), Fuentes (3x 45,00€ = 135,00€). Subtotal: 277,50€. IVA 21%: 58,28€. Total: 335,78€."
    },
    {
        "role": "assistant",
        "content": '{"numero_factura":"2024-045","fecha_emision":"2024-04-22","nif_emisor":"D11223344","nombre_emisor":"Supplies & Co","base_imponible":277.50,"iva_porcentaje":21,"iva_total":58.28,"total":335.78}'
    },
    {
        "role": "user",
        "content": "Invoice #INV-2024-789, issued 15/06/2024 by Global IT Services Inc, Tax ID E44556677. Net amount: 1.500,00 EUR, VAT (21%): 315,00 EUR, Total due: 1.815,00 EUR."
    },
    {
        "role": "assistant",
        "content": '{"numero_factura":"INV-2024-789","fecha_emision":"2024-06-15","nif_emisor":"E44556677","nombre_emisor":"Global IT Services Inc","base_imponible":1500.00,"iva_porcentaje":21,"iva_total":315.00,"total":1815.00}'
    },
]
