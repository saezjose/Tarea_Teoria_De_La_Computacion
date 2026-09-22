% Archivo de prueba: valido.pl
% Contiene 20 pruebas válidas que cubren todas las categorías léxicas de Prolog.

% 1. Átomos simples y delimitadores
animal(zorro).
animal(condor).

% 2. Átomos con guion bajo y números enteros
planta(arbol_nativo).
altura(arbol_nativo, 15).

% 3. Reglas, variables y operador de cláusula (:-)
crece(X, Y) :- riega(X, Y).

% 4. Operadores de unificación y átomos entrecomillados
especie('Puma Concolor').
fauna(V) :- V == 'Puma Concolor'.

% 5. Cadenas de texto y variables anónimas
paisaje(_) = "Amanecer dorado sobre la cordillera nevada".

% 6. Números reales y operadores aritméticos
temperatura_ideal is 38.5 + 1.2.

% 7. Comentarios de bloque y conjunciones (,)
/* La fotosintesis de la planta
   requiere revision de la clorofila */
crecimiento(A, P) :- luz(A), agua(P).

% 8. Operador alfabético (mod) y paréntesis
resto is (100 * 2) mod 3.

% 9. Operador alfabético (is) y divisiones
caudal is 220 // 2.

% 10. Operadores de control (\+)
\+ sequia(bosque).

% 11. Comparaciones numéricas (>=, =<)
nivel_humedad(H) :- H >= 40, H =< 80.

% 12. Operador de disyunción (;)
habitat(H) :- bioma(selva) ; bioma(sabana).

% 13. Operador de desigualdad (\=)
especie(aguila) \= especie(condor).

% 14. Operador de estructura (=..)
Termino =.. [florece, orquidea].

% 15. Consultas (?-), punto final y mayúsculas
?- crece(semilla, Quien).

% 16. Variables múltiples en una misma cláusula
conexion(rio, mar, Afluente).

% 17. Desigualdad estricta (\==)
'Secoya' \== 'Baobab'.

% 18. Operador de gramática (-->)
avistamiento --> cielo_despejado.

% 19. Operador de potencia (**)
energia is 10 ** 2.

% 20. Uso de corchetes y barras para listas
coleccion_especies = [colibri | resto_de_aves].