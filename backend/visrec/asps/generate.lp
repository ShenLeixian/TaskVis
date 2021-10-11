% ====== Generators ======

% encodings

% maximum number for each multi channel encoding
#const max_extra_encs = 5.

obj_id(1..max_extra_encs).
encode(e0;e1;e2;e3;e4;e5;e6;e7;e8;e9;e10;e11;e12;e13).
{ encoding(E): obj_id(E) }.

:- not encoding(ID), encoding(ID-1), obj_id(ID), obj_id(ID-1).

% properties of encodings

% channel and type have to be present
0 { channel(E,C): channel(C) } 1 :- encoding(E).
% 0 { type(E,T): type(T) } 1 :- encoding(E).
{ type(E,T): type(T) } =1 :- channel(E,_).
% :- { channel(_,_)}<2.
:- { channel((e0;e1;e2;e3;e4;e5;e6;e7),_)}<1.
:- not type(ID,_),field(ID,_),obj_id(ID).
% :- not channel(ID,_),type(ID,_),obj_id(ID).
% :- not field(ID,_),type(ID,_),obj_id(ID).
:- not channel(E,_),aggregate(E,_).
:- not channel(E,_),bin(E,_).
% :- not channel(E,_),zero(E).

% other properties that are not required
0 { field(E,F): field(F) } 1 :- encoding(E).
0 { aggregate(E,A): aggregate_op(A) } 1 :- encoding(E).
0 { bin(E,B): binning(B) } 1 :- encoding(E).
% 0 { zero(E) } 1 :- encoding(E).
% 0 { log(E) } 1 :- encoding(E).

% pick one mark type
{ mark(M) : marktype(M) } = 1.

% stacking
0 { stack(S): stacking(S) } 1.

% transform
0 { transform(S): transform_type(S) } 1.

% sort
0 { sort(E,S): sort_type(S) } 1 :- encoding(E).