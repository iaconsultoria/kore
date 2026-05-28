# Elección de modelo para extracción de facturas

## Comparativa

| Modelo | Coste entrada (1K tokens) | Coste salida (1K tokens) | Coste entrada (€) | Coste salida (€) | Latencia estimada | Privacidad | Precisión extracción |
|---|---|---|---|---|---|---|---|
| gpt-4o-mini | $0.00015 | $0.0006 | €0.000138 | €0.000552 | 1-2s | OpenAI (EEUU, RGPD DPA) | Alta |
| claude-3-haiku | $0.00025 | $0.00125 | €0.000230 | €0.001150 | 1-2s | Anthropic (EEUU, RGPD DPA) | Alta |
| claude-3-sonnet | $0.003 | $0.015 | €0.00276 | €0.01380 | 3-5s | Anthropic (EEUU, RGPD DPA) | Muy alta |
| gemini-1.5-flash | $0.000075 | $0.0003 | €0.000069 | €0.000276 | 1s | Google (EEUU, RGPD DPA) | Media |
| gpt-4o | $0.005 | $0.015 | €0.00460 | €0.01380 | 3-5s | OpenAI (EEUU, RGPD DPA) | Muy alta |
| gemini-1.5-pro | $0.00125 | $0.005 | €0.00115 | €0.00460 | 2-3s | Google (EEUU, RGPD DPA) | Alta |

## Modelo elegido: claude-3-haiku

Elijo claude-3-haiku porque sonsidero que es el más equilibrado para la extracción de facturas españolas con mejor precisión que gemini-1.5-flash en campos estructurados como NIF, importes o fechas con un coste más bajo que gpt-4o-mini en volumen alto y buena latencia. claude-3-sonnet y gpt-4o tienen mejor precisión pero su coste es 15 veces mayor sin justificación. Así que comparando todos los puntos importantes esta es mi elección.

## Fuentes

- Precios OpenAI: https://openai.com/api/pricing
- Precios Anthropic: https://claude.com/pricing#api
- Precios Google Gemini: https://ai.google.dev/pricing
