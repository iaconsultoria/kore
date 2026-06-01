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
]
