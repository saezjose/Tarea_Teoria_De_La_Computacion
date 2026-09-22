# Analizador léxico del lenguaje Prolog

Tarea de la asignatura **Teoría de la Computación (INFO1148)** — Semestre II, 2026.
Universidad Católica de Temuco, Facultad de Ingeniería.

Implementación de un analizador léxico para un subconjunto de Prolog, aplicando
alfabetos, lenguajes regulares, expresiones regulares y autómatas finitos.
El detalle formal (especificación léxica, diseño de autómatas, determinización,
minimización, reglas de prioridad y resultados de pruebas) está documentado
en el informe técnico entregado junto con esta tarea.

## Integrantes

| Integrante | Rol |
|---|---|
| José Sáez | Jefe de grupo |
| Catalina Vergara | Integrante |
| Alexa Galeano | Integrante |

**Profesor:** M. Lévano

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `lexer.py` | Analizador léxico. Combina todas las reglas léxicas en un único patrón maestro con `re`, evaluado en orden de prioridad (máxima coincidencia). |
| `valido.pl` | Corpus de **20 pruebas válidas**, cubriendo todas las categorías léxicas definidas. Debe ejecutarse sin errores. |
| `errores.pl` | Corpus con **8 errores léxicos inyectados**, cubriendo los 4 tipos exigidos: carácter no admitido, átomo/cadena sin cierre, comentario de bloque sin cierre y número mal formado. |
| `prioridad.pl` | Corpus de **16 casos** enfocados en prioridad y máxima coincidencia (operadores compuestos, palabras clave `is`/`mod` vs. átomos, variable anónima, etc.). |
| `ejemplo.pl` | Archivo de prueba adicional usado durante el desarrollo. |

## Requisitos

- Python 3.
- **Sin dependencias externas**: el analizador usa únicamente los módulos estándar `re` y `sys`.

## Ejecución

```bash
python lexer.py <archivo.pl>
```

Si no se indica un archivo, el programa usa `valido.pl` por defecto:

```bash
python lexer.py
```

### Ejemplos

```bash
python lexer.py valido.pl       # 20 casos válidos, 0 errores esperados
python lexer.py errores.pl      # 8 errores léxicos esperados
python lexer.py prioridad.pl    # 16 casos de prioridad, 0 errores esperados
```

## Salida del programa

Por cada token reconocido, el analizador imprime:

```
<TIPO_TOKEN, 'lexema', línea, columna, atributo>
```

El campo `atributo` indica el índice del lexema en la tabla de lexemas
(`idx:n`) cuando el token es un identificador o literal (átomo, variable,
número, cadena), o un guion (`-`) cuando es un operador, delimitador o el
punto final, ya que en esos casos el tipo de token ya determina su
significado.

Los errores léxicos se reportan en el formato:

```
ERROR LÉXICO (<tipo de error>): fragmento '<...>' en línea <n>, columna <n>
```

y **no detienen el análisis**: el programa continúa procesando el resto del
archivo.

Al finalizar, se imprime la **tabla de lexemas** (sin entradas duplicadas)
y el **total de errores léxicos** detectados.

## Alcance

Este analizador realiza **únicamente análisis léxico**. No construye árboles
sintácticos, no valida la gramática de las cláusulas ni realiza ningún tipo
de análisis semántico (unificación, aridad, ámbito de variables, etc.), de
acuerdo con lo solicitado en el enunciado de la tarea.

## Historial de contribuciones

El historial de commits de este repositorio refleja las contribuciones de
los tres integrantes del grupo.
