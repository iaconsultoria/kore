# Diagrama Entidad-Relación: Módulo Facturas

```mermaid
erDiagram
    PROVEEDOR ||--o{ FACTURA : "emite"
    CATEGORIA_GASTO ||--o{ FACTURA : "clasifica"
    FACTURA ||--|{ LINEA_FACTURA : "contiene"

    PROVEEDOR {
        int id PK
        string nombre
        string nif
        text direccion
        string pais
    }

    FACTURA {
        int id PK
        string numero_factura
        date fecha_emision
        date fecha_vencimiento
        int proveedor_id FK
        int categoria_id FK "nullable"
        decimal base_imponible
        decimal iva_total
        decimal total
        string archivo_original
        boolean extraccion_fallida
        text error_extraccion
    }

    LINEA_FACTURA {
        int id PK
        int factura_id FK
        string concepto
        decimal cantidad
        decimal precio_unitario
        int iva_porcentaje
    }

    CATEGORIA_GASTO {
        int id PK
        string nombre
        boolean deducible_iva
        string cuenta_contable
    }
```

## Descripción de relaciones

- Proveedor -> Factura (1:N): Un proveedor emite múltiples facturas. FK proveedor_id en Factura. ON_DELETE PROTECT.
- CategoriaGasto -> Factura (1:N): Una categoría clasifica múltiples facturas. FK categoria_id nullable. ON_DELETE SET_NULL.
- Factura -> LineaFactura (1:N): Una factura contiene múltiples líneas. FK factura_id en LineaFactura. ON_DELETE CASCADE.
