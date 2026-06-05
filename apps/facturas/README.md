# App facturas

## Qué hace

Gestiona facturas de proveedores con extracción automática de datos desde PDF o imagen mediante IA, revisión manual, clasificación por categoría de gasto y trazabilidad de las sugerencias generadas por el modelo. Incluye un dashboard fiscal con resumen de IVA y gastos por categoría y un sistema de alertas para facturas próximas a vencer.

## Modelos principales

| Modelo | Para qué sirve |
|---|---|
| Proveedor | Almacena datos del emisor de la factura |
| Categoria Gasto | Categorías contables para clasificar facturas |
| Factura | Factura principal con importes, fechas, proveedor y categoría que tiene |
| Linea Factura | Líneas de detalle de cada factura |
| Fragmento Normativa | Fragmentos de normativa fiscal con embedding vectorial para búsqueda RAG |
| Sugerencia Categoria | Registro de cada sugerencia de categoría generada por IA con el resultado de la decisión del usuario |

## Cómo probar la extracción

1. Acceder a /facturas/ y entra en una factura
2. En la vista de revisión pulsa en "Sugerir categoría"
3. El modelo genera una sugerencia basada en el proveedor y las líneas de factura
4. Pulsa Aceptar para asignar la categoría a la factura o Ignorar para descartarla
5. Ambas decisiones quedan registradas en SugerenciaCategoria y son visibles en el admin en /admin/facturas/sugerenciacategoria/

## Dependencias clave

| Dependencia | Para qué se usa |
|---|---|
| litellm | Cliente unificado para llamadas a modelos de IA con extracción de facturas y sugerencia de categoría con OpenRouter |
| pgvector | Almacenamiento y búsqueda por similitud de embeddings vectoriales en PostgreSQL por búsqueda RAG de normativa |
| openpyxl | Exportación de datos a Excel |
