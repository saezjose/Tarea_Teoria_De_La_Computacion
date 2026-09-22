% Archivo de prueba: errores.pl
% Contiene al menos 8 errores léxicos para evaluar la recuperación del lexer.

% 1. Caracter no admitido (@)
correo(bosque@nativo).

% 2. Caracter no admitido (~)
ruta(~sendero).

% 3. Caracter no admitido ($)
precio(Semilla, $100).

% 4. Átomo entrecomillado sin cierre
atomo_roto = 'Falta comilla final .

% 5. Cadena sin cierre
texto_roto = "Falta comilla doble final .

% 6. Número mal formado (múltiples puntos)
altura is 3.14.15.

% 7. Número mal formado (letra pegada a dígito)
calculo is 42x + 5.

% 8. Comentario de bloque sin cierre
/* Este bloque nunca termina y generara lectura huerfana