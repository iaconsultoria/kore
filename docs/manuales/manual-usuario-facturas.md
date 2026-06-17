# Manual de Usuario: Módulo Facturas

## Introducción

Este manual documenta el flujo completo del módulo Facturas de Kore:
- Administrador: Crea y gestiona facturas en Django admin
- Usuario final: Revisa, edita y guarda facturas desde web

## PARTE 1: Administrador — Crear y gestionar facturas

### 1.1 Acceder a Django admin

1. Ve a http://localhost:8000/admin/
2. Inicia sesión con credenciales de administrador

### 1.2 Crear Proveedor (requisito previo)

1. En admin, haz clic en Proveedores -> Agregar proveedor
2. Rellena:
   - Nombre: Nombre de la empresa (obligatorio)
   - NIF: NIF, NIE o CIF español válido (obligatorio)
   - Dirección: Domicilio (opcional)
   - País: Código ISO de 2 letras (por defecto "ES")
3. Haz clic en Guardar

### 1.3 Crear CategoriaGasto (opcional, pero recomendado)

1. En admin, haz clic en Categorías de gasto -> Agregar categoría de gasto
2. Rellena:
   - Nombre: Ej. "Suministros", "Transporte", "Servicios" (obligatorio)
   - Deducible IVA: Marca si el gasto es deducible en IVA (por defecto sí)
   - Cuenta contable: Código de cuenta contable (opcional)
3. Haz clic en Guardar

### 1.4 Crear Factura

1. En admin, haz clic en Facturas -> Agregar factura
2. Rellena los datos principales:
   - Número de factura: Ej: "2026-001234" (obligatorio, único por proveedor)
   - Fecha de emisión: Fecha de la factura (obligatorio)
   - Fecha de vencimiento: Fecha de pago. Si dejas vacía, se calcula automáticamente 30 días desde emisión
   - Proveedor: Selecciona de la lista (obligatorio)
   - Categoría: Selecciona de la lista o deja vacía (opcional)
   - Base imponible: Importe sin IVA (obligatorio)
   - IVA total: Importe total del IVA (obligatorio)
   - Total: Importe final (obligatorio)
   - Archivo original: Sube PDF, JPG o PNG si tienes (opcional, máx. 10 MB)

3. Agregar líneas de factura (abajo del formulario, sección "Líneas de factura"):
   - Haz clic en Agregar otra Línea de factura
   - Para cada línea, rellena:
     - Concepto: Descripción del concepto (obligatorio)
     - Cantidad: Número de unidades (obligatorio)
     - Precio unitario: Precio sin IVA por unidad (obligatorio)
     - IVA %: Selecciona el porcentaje: 21%, 10%, 4%, o 0% (obligatorio)

4. Haz clic en Guardar

Restricción importante: No puedes guardar dos facturas con el mismo número + proveedor. El sistema lo detecta y rechaza el duplicado.

### 1.5 Editar Factura

1. En admin, busca la factura en la lista o usa búsqueda por número
2. Haz clic para abrir
3. Edita cualquier campo y haz clic en Guardar

## PARTE 2: Usuario Final — Revisar, editar y trabajar con facturas

### 2.1 Acceder a la lista de facturas

1. Ve a http://localhost:8000/facturas/ (o sigue el enlace desde el menú)
2. Verás una tabla con todas las facturas:
   - Número: Identificador de la factura
   - Proveedor: Nombre de la empresa
   - Fecha emisión: Fecha de la factura
   - Total: Importe final en €

### 2.2 Revisar una factura

1. Haz clic en el número de factura que quieras revisar
2. Se abre la pantalla de Revisión, donde ves:
   - Todos los datos de la factura en un formulario editable
   - Líneas desglosadas (concepto, cantidad, precio unitario, IVA%)
   - Información de apoyo (ver sección 2.5)

### 2.3 Editar datos de la factura

En la pantalla de revisión, puedes cambiar:
- Número de factura
- Fecha de emisión
- Proveedor (selecciona de la lista; se busca dinámicamente)
- Categoría (selecciona o deja vacía)
- Base imponible, IVA total, Total (introduce los valores correctos)
- Archivo original (sube o reemplaza PDF/JPG/PNG)

Validación automática:
- El sistema avisa si intentas guardar un número de factura + proveedor que ya existe

### 2.4 Asignar categoría automáticamente

1. En la revisión, haz clic en el botón Sugerir categoría
2. El sistema analiza el proveedor y los conceptos de las líneas
3. Verás una sugerencia con dos opciones:
   - Aceptar: La categoría se asigna a la factura
   - Ignorar: Se descarta la sugerencia y dejas el campo vacío

### 2.5 Información de apoyo (contexto)

Mientras revisas, puedes ver dos secciones opcionales:

Contexto normativo: Fragmentos de normativa (leyes y regulaciones) relacionados con la factura. Aparece si hay datos disponibles. Es solo referencia.

Citas del calendario: Eventos programados en el calendario para el mismo día de la factura. Es solo información de contexto.

Estas secciones son informativas y no afectan al guardado.

### 2.6 Guardar cambios

1. Verifica que todos los datos obligatorios estén completos
2. Haz clic en Guardar
3. La factura se actualiza en la base de datos

### 2.7 Ver avisos de vencimiento

1. En la lista de facturas, haz clic en Ver avisos de vencimiento
2. Verás las facturas que vencen en los próximos 7 días
3. Las marcadas como "urgentes" vencen en ≤ 2 días

### 2.8 Ver dashboard fiscal

1. En la lista de facturas, haz clic en Dashboard fiscal
2. Verás un resumen mensual:
   - IVA soportado en el mes actual
   - Gastos por categoría
   - Facturas sin clasificar
   - Comparativa mes anterior

## Referencia: Campos obligatorios vs opcionales

| Campo | Obligatorio | Notas |
|-------|-----------|-------|
| Número de factura | Sí | Único por proveedor |
| Fecha emisión | Sí | Formato: YYYY-MM-DD |
| Proveedor | Sí | Debe existir en la BD |
| Categoría | No | Se puede dejar vacía; se puede sugerir automáticamente |
| Base imponible | Sí | Importe sin IVA |
| IVA total | Sí | Suma total del IVA |
| Total | Sí | Importe final (base + IVA) |
| Fecha vencimiento | No | Se calcula 30 días si no especificas |
| Archivo original | No | PDF/JPG/PNG, máx. 10 MB |
| Líneas | Sí | Mínimo una línea |

## Validaciones automáticas

- Duplicados: No permite guardar factura con número + proveedor duplicado
- Fecha vencimiento: Si no la especificas, se calcula automáticamente 30 días desde emisión
- Líneas: Cada línea calcula internamente su subtotal: cantidad × precio unitario × (1 + IVA%)
- NIF en proveedor: Valida formato de NIF/NIE/CIF español

## Preguntas frecuentes

¿Dónde creo un proveedor nuevo?
En Django admin (/admin/ → Proveedores → Agregar proveedor). Es requisito previo.

¿Puedo editar las líneas de una factura después de crearla?
Sí, desde Django admin. En web solo puedes verlas, no editarlas directamente.

¿Qué pasa si no asigno categoría?
La factura se guarda sin categoría. Puedes asignarla después manualmente o pedir una sugerencia automática.

¿Se calcula el total automáticamente?
No. Base imponible, IVA y total son datos que introduces manualmente. Las líneas se usan como referencia desglosada.

¿Puedo subir la factura en PDF?
Sí, como "Archivo original" (opcional). Es solo almacenamiento; los datos se introducen manualmente.

¿Qué significa "extracción fallida"?
Solo aparece si se intentó extraer automáticamente vía API y falló. En el flujo manual (admin) no aplica.

¿Cómo descargo las facturas?
Función en desarrollo. Por ahora, puedes ver todas en la lista y detalles en la revisión.

¿Puedo editar desde web o solo en admin?
En web puedes revisar y editar los campos principales (número, fecha, proveedor, categoría, importes, archivo). Las líneas se editan en admin.

¿Qué pasa si asigno una categoría incorrecta?
Puedes cambiarla en cualquier momento desde web (botón Sugerir categoría) o editarla manualmente.

## Flujo resumido

1. Admin crea facturas (Django admin): Proveedor -> Factura + Líneas
2. Usuario revisa (web): /facturas/revisar/<pk>/
3. Usuario edita y guarda (web): Actualiza datos
4. Usuario consulta (web): Lista, avisos, dashboard

## Soporte

Si encuentras problemas o necesitas crear nuevos proveedores, contacta con el equipo técnico o accede a Django admin.
