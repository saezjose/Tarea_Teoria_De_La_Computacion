padre(juan, ana).
padre(juan, pedro).
abuelo(X, Z) :-
 padre(X, Y),
 padre(Y, Z).
lista([a,b|c]).
regla :- a, b ; c.
neg :- \+ a.
corte :- a, !.
consulta :- padre(juan, ana).
?- padre(juan, X).