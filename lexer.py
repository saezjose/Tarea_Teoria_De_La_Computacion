import re
import sys


reglas_lexicas = [

    ('COMENTARIO_BLOQ',            r'/\*[\s\S]*?\*/'),

    ('COMENTARIO_BLOQ_SIN_CERRAR', r'/\*[^\n]*'),
    ('COMENTARIO_LINEA',           r'%[^\n]*'),

    ('CADENA',                     r'"[^"\n]*"'),
    ('CADENA_SIN_CERRAR',          r'"[^"\n]*'),
    ('ATOMO_COMILLAS',             r"'[^'\n]*'"),
    ('ATOMO_COMILLAS_SIN_CERRAR',  r"'[^'\n]*"),


    ('NUM_MAL_MULTIPLES_PUNTOS', r'[0-9]+(\.[0-9]+){2,}'),          
    ('NUM_MAL_LETRA_PEGADA',     r'[0-9]+[a-zA-Z_][a-zA-Z0-9_]*'),  
    ('NUM_REAL',                 r'[0-9]+\.[0-9]+'),
    ('NUM_ENTERO',               r'[0-9]+'),

    ('OP_CLAUSULA',      r':-|\?-|-->'),
    ('OP_UNIFICACION',   r'\\==|==|=\.\.|\\=|=<|>=|<|>|='),
    ('OP_ARITMETICO',    r'\*\*|//|\+|-|\*|/'),
    ('OP_ALFABETICO',    r'\b(is|mod)\b'),
    ('OP_CONTROL',       r'\\\+|!|;|,'),
    ('DELIMITADOR',      r'\(|\)|\[|\]|\{|\}|\|'),
    ('PUNTO',            r'\.'),
    ('VARIABLE',         r'[A-Z_][a-zA-Z0-9_]*'),
    ('ATOMO',            r'[a-z][a-zA-Z0-9_]*'),
    ('ESPACIO',          r'\s+'),
]


TOKENS_IGNORADOS = {'ESPACIO', 'COMENTARIO_LINEA', 'COMENTARIO_BLOQ'}


TOKENS_ERROR = {
    'COMENTARIO_BLOQ_SIN_CERRAR': 'Comentario de bloque sin cierre',
    'CADENA_SIN_CERRAR':          'Cadena sin cierre',
    'ATOMO_COMILLAS_SIN_CERRAR':  'Átomo entrecomillado sin cierre',
    'NUM_MAL_MULTIPLES_PUNTOS':   'Número mal formado (múltiples puntos decimales)',
    'NUM_MAL_LETRA_PEGADA':       'Número mal formado (letra pegada a un dígito)',
}


TOKENS_CON_ATRIBUTO = {
    'ATOMO', 'ATOMO_COMILLAS', 'VARIABLE', 'CADENA', 'NUM_ENTERO', 'NUM_REAL',
}


patron_maestro = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in reglas_lexicas)
regex = re.compile(patron_maestro)


class TablaLexemas:


    def __init__(self):
        self._entradas = {}  
        self._siguiente = 1

    def registrar(self, lexema, categoria):
 
        if lexema in self._entradas:
            return self._entradas[lexema][0]
        indice = self._siguiente
        self._entradas[lexema] = (indice, categoria)
        self._siguiente += 1
        return indice

    def filas(self):
   
        return sorted(
            ((idx, lex, cat) for lex, (idx, cat) in self._entradas.items()),
            key=lambda fila: fila[0],
        )

    def __len__(self):
        return len(self._entradas)


def analizador_lexico(codigo_fuente):
  
    posicion = 0
    linea = 1
    inicio_linea = 0
    tabla_lexemas = TablaLexemas()
    total_errores = 0

    print("--- INICIANDO ANÁLISIS LÉXICO ---")

    while posicion < len(codigo_fuente):
        match = regex.match(codigo_fuente, posicion)

        if match:
            tipo_token = match.lastgroup
            lexema = match.group(tipo_token)
            columna = posicion - inicio_linea + 1


            if '\n' in lexema:
                linea += lexema.count('\n')
                inicio_linea = posicion + lexema.rfind('\n') + 1

            if tipo_token in TOKENS_ERROR:

                total_errores += 1
                mensaje = TOKENS_ERROR[tipo_token]
                fragmento = lexema if len(lexema) <= 30 else lexema[:30] + '...'
                print(f"ERROR LÉXICO ({mensaje}): fragmento '{fragmento}' "
                      f"en línea {linea}, columna {columna}")

            elif tipo_token not in TOKENS_IGNORADOS:

                if tipo_token in TOKENS_CON_ATRIBUTO:
                    indice = tabla_lexemas.registrar(lexema, tipo_token)
                    atributo = f"idx:{indice}"
                else:

                    atributo = "-"
                print(f"<{tipo_token}, '{lexema}', {linea}, {columna}, {atributo}>")


            posicion = match.end()

        else:
         
            total_errores += 1
            columna = posicion - inicio_linea + 1
            caracter_erroneo = codigo_fuente[posicion]
            print(f"ERROR LÉXICO (Carácter no admitido): '{caracter_erroneo}' "
                  f"en línea {linea}, columna {columna}")
            posicion += 1

    print(f"\n--- Total de errores léxicos detectados: {total_errores} ---")
    return tabla_lexemas, total_errores


def imprimir_tabla(tabla):

    print("\n--- TABLA DE LEXEMAS ---")
    print(f"{'Indice':>6} | {'Lexema':<34} | Categoria")
    print("-" * 70)
    for indice, lexema, categoria in tabla.filas():
        print(f"{indice:>6} | {lexema:<34} | {categoria}")
    print("-" * 70)
    print(f"Total de entradas unicas: {len(tabla)}")

def main():
    ruta_archivo = sys.argv[1] if len(sys.argv) > 1 else "prioridad.pl"

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            codigo_fuente = archivo.read()
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{ruta_archivo}'.")
        return 1

    tabla, total_errores = analizador_lexico(codigo_fuente)
    imprimir_tabla(tabla)
    return 0


if __name__ == "__main__":
    sys.exit(main())