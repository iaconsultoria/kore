```mermaid
erDiagram
    CATEGORIA {
        bigint id PK
        varchar(50) nombre
        varchar(7) color
        smallint prioridad
        varchar(20) politica_reprog
        text plantilla_notas
    }

    CITA {
        bigint id PK
        varchar(200) titulo
        date inicio
        date fin
        time hora_inicio
        time hora_fin
        bigint categoria_id FK
        text anotaciones
        smallint prioridad
        varchar(10) repetir
        varchar(255) ubicacion
    }

    RECORDATORIO {
        bigint id PK
        bigint cita_id FK
        datetime fecha_aviso
        varchar(15) tipo
    }

    CATEGORIA ||--o{ CITA : "clasifica"
    CITA ||--o| RECORDATORIO : "tiene"
```
Diagrama entidad-relación de la app Calendario. Muestra las tres entidades principales — Categoria, Cita y Recordatorio — con sus atributos y las relaciones entre ellas: una categoría clasifica muchas citas, y una cita puede tener como máximo un recordatorio.
