% Archivo de prueba: prioridad.pl
% Casos específicos de máxima coincidencia y prioridad, exigidos por el
% enunciado (punto 6): demuestra que el lexer elige el token MÁS LARGO
% posible en cada posición, y no se confunde entre operadores de
% distinta longitud que comparten prefijo, ni entre operadores
% alfabéticos (is, mod) y átomos comunes.

% 1. "=<" debe leerse como UN token OP_UNIFICACION, no como "=" + "<"
menor_o_igual :- A =< B.

% 2. "==" debe leerse como UN token, no como "=" + "="
igualdad_estricta :- A == B.

% 3. "\==" debe leerse como UN token, no como "\=" + "="
desigualdad_estricta :- A \== B.

% 4. "\=" debe leerse como UN token, no como "\" + "="
desigualdad :- A \= B.

% 5. "=.." debe leerse como UN token, no como "=" + "." + "."
estructura :- Termino =.. [rio, monte, valle].

% 6. ">=" debe leerse como UN token, no como ">" + "="
mayor_o_igual :- A >= B.

% 7. "=" solo (sin continuación) debe seguir reconociéndose como OP_UNIFICACION simple
unificacion_simple :- A = B.

% 8. ":-" debe leerse como UN token, no como ":" (inválido) + "-"
planta_simple(X) :- especie(X).

% 9. "?-" debe leerse como UN token de consulta, no como "?" (inválido) + "-"
?- planta_simple(algo).

% 10. "-->" debe leerse como UN token, no como "-" + "-" + ">" (o "--" + ">")
ecosistema --> bosque_lluvioso.

% 11. "**" debe leerse como UN token (potencia), no como "*" + "*"
potencia :- R is 2 ** 10.

% 12. "//" debe leerse como UN token (división entera), no como "/" + "/"
division_entera :- R is 10 // 3.

% 13. "is" como palabra completa debe ser OP_ALFABETICO...
suma :- R is 2 + 2.
% ...pero "istmo" o "isla" (que EMPIEZAN con "is") deben seguir siendo ATOMO,
% no confundirse con el operador "is" + resto de letras sueltas
geografia_istmo(istmo).
lugar(isla).

% 14. "mod" como palabra completa debe ser OP_ALFABETICO...
resto :- R is 10 mod 3.
% ...pero "modelo" o "modo" deben seguir siendo ATOMO
bioma(modelo).
paisaje(modo).

% 15. "!" (corte) no debe confundirse con "\+" (negación), aunque ambos
%     empiecen distinto pero se usen en contextos similares de control
con_corte :- especie(X), !.
con_negacion :- \+ especie(X).

% 16. Variable vs átomo: "X" y "x" deben distinguirse solo por may/minúscula
distincion(X, x).