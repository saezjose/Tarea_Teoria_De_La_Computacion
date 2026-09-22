
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

    
    ('NUM_MAL_MULTIPLES_PUNTOS', r'[0-9]+(\.[0-9]+){2,}'),          # ej: 3.14.15
    ('NUM_MAL_LETRA_PEGADA',     r'[0-9]+[a-zA-Z_][a-zA-Z0-9_]*'),  # ej: 42x
    ('NUM_REAL',                 r'[0-9]+\.[0-9]+'),
    ('NUM_ENTERO',               r'[0-9]+'),

    
    ('DELIMITADOR', r'\(|\)|\[|\]|\{|\}|\|'),
    ('PUNTO',       r'\.'),
    ('VARIABLE',    r'[A-Z_][a-zA-Z0-9_]*'),
    ('ATOMO',       r'[a-z][a-zA-Z0-9_]*'),
    ('ESPACIO',     r'\s+'),
]


TOKENS_IGNORADOS = {'ESPACIO', 'COMENTARIO_LINEA', 'COMENTARIO_BLOQ'}


TOKENS_ERROR = {
    'COMENTARIO_BLOQ_SIN_CERRAR': 'Comentario de bloque sin cierre',
    'CADENA_SIN_CERRAR':          'Cadena sin cierre',
    'ATOMO_COMILLAS_SIN_CERRAR':  'Átomo entrecomillado sin cierre',
    'NUM_MAL_MULTIPLES_PUNTOS':   'Número mal formado (múltiples puntos decimales)',
    'NUM_MAL_LETRA_PEGADA':       'Número mal formado (letra pegada a un dígito)',
}


patron_maestro = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in reglas_lexicas)
regex = re.compile(patron_maestro)


def analizador_lexico(codigo_fuente):
    """Recorre el código fuente de izquierda a derecha emitiendo tokens."""
    posicion = 0
    linea = 1
    inicio_linea = 0
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
                
                print(f"<{tipo_token}, '{lexema}', {linea}, {columna}, ->")

            posicion = match.end()

        else:
            
            total_errores += 1
            columna = posicion - inicio_linea + 1
            caracter_erroneo = codigo_fuente[posicion]
            print(f"ERROR LÉXICO (Carácter no admitido): '{caracter_erroneo}' "
                  f"en línea {linea}, columna {columna}")
            posicion += 1

    print(f"\n--- Total de errores léxicos detectados: {total_errores} ---")
    return total_errores


def main():
    ruta_archivo = sys.argv[1] if len(sys.argv) > 1 else "ejemplo.pl"

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            codigo_fuente = archivo.read()
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{ruta_archivo}'.")
        return 1

    analizador_lexico(codigo_fuente)
    return 0


if __name__ == "__main__":
    sys.exit(main())