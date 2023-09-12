#const num=3.
#const n=num*num.

% Make the sudoku board a 2D array
fixed(1,2,7). fixed(1,6,6). fixed(1,8,1).
fixed(2,3,6). fixed(2,4,3). fixed(2,7,9).
fixed(3,1,1). fixed(3,5,8). fixed(3,9,3).
fixed(4,1,9). fixed(4,4,5). fixed(4,8,3).
fixed(5,3,7). fixed(5,5,2). fixed(5,7,1).
fixed(6,2,3). fixed(6,6,9). fixed(6,9,4).
fixed(7,1,8). fixed(7,5,3). fixed(7,9,6).
fixed(8,3,9). fixed(8,6,5). fixed(8,7,3).
fixed(9,2,4). fixed(9,4,8). fixed(9,8,2).

% Ορισμός των συναρτήσεων
% In cell (I,J) the value is X
1{value(I,J,X): X=1..n}1 :- I=1..n, J=1..n.

% A cell is in the same box as another cell if they are in the same nxn square
sameBox(I1,J1,I2,J2) :- I1=1..n, J1=1..n, I2=1..n, J2=1..n, (I1-1)/num=(I2-1)/num, (J1-1)/num=(J2-1)/num.

% Γενικοί Περιορισμοί
% A box must not have the same value twice
:- sameBox(I1,J1,I2,J2), value(I1,J1,X), value(I2,J2,X), I1!=I2, J1!=J2.
% A row must not have the same value twice
:- value(I,J1,X), value(I,J2,X), J1!=J2.
% A column must not have the same value twice
:- value(I1,J,X), value(I2,J,X), I1!=I2.

% Περιορισμοί για το πρόβλημα
% The value of a cell is fixed
:- value(I,J,X1), fixed(I,J,X2), X1!=X2.

% Εκτύπωση της λύσης
#show value/3.