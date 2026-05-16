# Hackeo cruzado — Reglas

Objetivo: aprender seguridad **haciendo**, no leyendo. Cada uno intenta romper el código del otro de forma deportiva y constructiva.

## Cuándo

- **Semana 5**, martes (M 16/06) y miércoles (X 17/06). Solo entonces.
- Código del compañero queda **congelado** al cerrar V 12/06 — no se toca después.

## Qué SÍ está permitido

- Atacar el **código** del compañero: lógica, validación, autorización, inyección (SQL, prompt, fórmula Excel), XSS, CSRF, secretos en repo, dependencias inseguras, manejo de ficheros (path traversal, MIME spoofing), errores que filtran información.
- Usar **IA** como ayuda para encontrar vulnerabilidades (es parte de la pedagogía).
- Leer todo el código del compañero. Es público entre ambos durante S5.
- Crear PoC (prueba de concepto) que demuestre la vulnerabilidad.

## Qué NO está permitido

- Atacar **al compañero como persona**: nada de ingeniería social, suplantación, robo de cuentas, mensajes privados, etc.
- Atacar **infraestructura común**: ni servidor compartido, ni cuenta GitHub, ni el repo `kore` salvo en lo que sea su código.
- Borrar, modificar u ocultar el código del otro. Solo se documenta y demuestra.
- Ataques físicos al equipo del otro.
- Sembrar puertas traseras durante S1-S4 para "encontrarlas" en S5. Eso es trampa.

## Cómo se documenta cada hallazgo

Cada vulnerabilidad encontrada va en un fichero markdown dentro de `hackeo/` del repo `kore`, formato:

```
# VULN-XX — Título corto
- Autor del hallazgo:
- Tipo: [validación / autorización / inyección / secretos / deps / lógica / otro]
- Severidad: [baja / media / alta / crítica]
- Descripción: qué falla y por qué
- PoC: pasos para reproducir o snippet de código
- Mitigación propuesta:
```

## Puntuación (orientativa, no es lo importante)

- Vuln crítica: 4 pts
- Alta: 3
- Media: 2
- Baja: 1
- Mitigación correcta que el atacado proponga: +1 a la defensa
- Falsos positivos: 0 pts y nota negativa si se han colado varios

## Cierre J 18/06

- Cada uno presenta sus hallazgos en 15 min al otro y a la tutora.
- El atacado tiene derecho a réplica: explica por qué, propone mitigación.
- Se hace una lista conjunta de "lecciones aprendidas" que va al README final.

## Honor code

- Todo lo encontrado se hace público al cerrar el ejercicio. No se ocultan vulns para usarlas más adelante.
- No se busca humillar. Se busca aprender que el código siempre tiene grietas y que la IA también introduce errores que hay que ver.
- Si uno detecta que el otro lo está pasando mal, lo dice. La tutora para el ejercicio.

---

## Decisiones pendientes (cerrar la tutora antes de S5)

- [ ] ¿Premio simbólico al ganador o puramente colaborativo?
- [ ] ¿La tutora puede meter vulns "plantadas" para que las encuentren? (recomendación: sí, 1-2 por app, anunciado por adelantado)
- [ ] ¿Las vulnerabilidades en código generado por IA cuentan igual que las escritas a mano? (sí: el responsable es quien commiteó).
