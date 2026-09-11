"""
Analizador léxico para un subconjunto de Prolog
Tarea INFO1148 - Teoría de la Computación

Este es un ESQUELETO INICIAL: ya funciona para las categorías que
tenemos definidas (espacios, comentario de línea, átomo, variable),
y deja marcados los TODO para las categorías que faltan (números,
cadenas, comentario de bloque, operadores, delimitadores).

Cómo se agrega un token nuevo:
1. Cerrar la fila correspondiente en la tabla de especificación
   (especificacion_tokens_prolog.md)
2. Agregar una tupla (NOMBRE_TOKEN, regex) en TOKEN_SPEC, en el
   ORDEN CORRECTO DE PRIORIDAD (lo más específico primero: por
   ejemplo "=<" debe ir antes que "<" y que "=")
3. Probar con casos del corpus de pruebas (mínimo 1 caso válido y
   1 inválido por token nuevo)
"""

import re
import sys


class Token:
    def __init__(self, tipo, lexema, linea, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"<{self.tipo}, {self.lexema!r}, {self.linea}, {self.columna}>"


class LexicalError(Exception):
    def __init__(self, mensaje, linea, columna, fragmento):
        super().__init__(mensaje)
        self.linea = linea
        self.columna = columna
        self.fragmento = fragmento

    def __str__(self):
        return (
            f"Error léxico en línea {self.linea}, columna {self.columna}: "
            f"{super().__str__()} (fragmento: {self.fragmento!r})"
        )


# ---------------------------------------------------------------
# Especificación de tokens: (NOMBRE, regex)
# IMPORTANTE: el orden importa. Los patrones más específicos van
# ANTES que los más generales (ej: "=<" antes que "<" y que "=").
# ---------------------------------------------------------------
TOKEN_SPEC = [
    ("ESPACIO_BLANCO",   r"[ \t\r\n]+"),
    ("COMENTARIO_LINEA", r"%[^\n]*"),
    # TODO (Bloque B): COMENTARIO_BLOQUE  /* ... */
    #   ojo: usar patrón NO codicioso, ej: r"/\*.*?\*/" con re.DOTALL,
    #   y pensar qué pasa si el archivo termina sin cerrar el comentario.

    ("VARIABLE",  r"[A-Z_][a-zA-Z0-9_]*"),
    ("ATOMO",     r"[a-z][a-zA-Z0-9_]*"),
    ("OP_CLAUSULA",       r":-"),
    ("PARENTESIS_IZQ",    r"\("),
    ("PARENTESIS_DER",    r"\)"),
    ("COMA",               r","),
    ("PUNTO",              r"\."),
    ("CORCHETE_IZQ",     r"\["),
    ("CORCHETE_DER",     r"\]"),
    ("LLAVE_IZQ",        r"\{"),
    ("LLAVE_DER",        r"\}"),
    ("BARRA_VERTICAL",   r"\|"),
    ("PUNTO_COMA",       r";"),
    ("NEGACION",         r"\\\+"),
    ("CORTE",            r"!"),
    ("OP_CONSULTA",      r"\?-"),
    # TODO (Bloque A): ATOMO_COMILLADO   'texto con espacios o especiales'
    # TODO (Bloque B): CADENA             "texto"  (definir escapes)
    # TODO (Bloque B): NUMERO_REAL antes que NUMERO_ENTERO (más específico primero)
    # TODO (Bloque B): NUMERO_ENTERO

    # TODO (Bloque C): operadores de cláusula/consulta: :-  ?-  --> (opcional)
    # TODO (Bloque C): operadores de unificación/comparación, en este orden
    #        de más largos a más cortos: =..  ==  \==  =<  >=  \=  =  <  >
    # TODO (Bloque C): operadores aritméticos: **  //  + - * /   is   mod
    # TODO (Bloque C): operadores de control: \+  !  ;  ,
    # TODO (Bloque C): delimitadores: ( ) [ ] { } | .

    ("DESCONOCIDO", r"."),  # catch-all: cualquier carácter no reconocido -> error
]

MAESTRA = re.compile(
    "|".join(f"(?P<{nombre}>{patron})" for nombre, patron in TOKEN_SPEC)
)

# Tokens que se reconocen pero NO se emiten como token (se descartan)
TOKENS_IGNORADOS = {"ESPACIO_BLANCO", "COMENTARIO_LINEA", "COMENTARIO_BLOQUE"}


def tokenizar(codigo_fuente):
    """Recorre el código fuente y devuelve (tokens, errores)."""
    tokens = []
    errores = []
    linea = 1
    inicio_linea = 0  # posición (offset) donde empieza la línea actual

    for match in MAESTRA.finditer(codigo_fuente):
        tipo = match.lastgroup
        lexema = match.group()
        columna = match.start() - inicio_linea + 1

        if tipo == "DESCONOCIDO":
            errores.append(LexicalError("carácter no admitido", linea, columna, lexema))
        elif tipo not in TOKENS_IGNORADOS:
            tokens.append(Token(tipo, lexema, linea, columna))

        # Actualizar línea/columna si el lexema abarcó saltos de línea
        saltos = lexema.count("\n")
        if saltos:
            linea += saltos
            inicio_linea = match.start() + lexema.rfind("\n") + 1

    return tokens, errores


def main():
    if len(sys.argv) != 2:
        print("Uso: python lexer.py <archivo.pl>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        codigo = f.read()

    tokens, errores = tokenizar(codigo)

    for t in tokens:
        print(t)

    if errores:
        print("\n--- Errores léxicos ---")
        for e in errores:
            print(e)


if __name__ == "__main__":
    main()