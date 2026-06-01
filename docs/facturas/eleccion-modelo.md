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

## Modelo elegido: openrouter/google/gemma-4-31b-it:free

Al principio elegí claude-3-haiku por su coste y precisión. Pero Google AI Studio está bloqueado en España y Anthropic pide $5 de crédito inicial. Una alternativa gratuita con soporte de visión disponible en OpenRouter fue google/gemma-4-31b-it:free. El resto de la lógica no cambia, si en el futuro tenemos una clave de Anthropic u OpenAI, solo tendríamo que cambiar el modelo en extractor.py.

## Fuentes

- Precios OpenAI: https://openai.com/api/pricing
- Precios Anthropic: https://claude.com/pricing#api
- Precios Google Gemini: https://ai.google.dev/pricing
