CodingTheory
============

Coding Theory math utilities in python.
Will help to do any coding theory homework.

For examples of usage, please see test.py


Some impressive stuff (not really):

    print "(Z_2)^3:"
    print Zmod(2)**3

Prints the size 3 vector space of the finite field of two elements. (All binary words of length 3):

    [[Bit(0), Bit(0), Bit(0)], [Bit(0), Bit(0), Bit(1)], [Bit(0), Bit(1), Bit(0)], [Bit(0), Bit(1), Bit(1)], [Bit(1), Bit(0), Bit(0)], [Bit(1), Bit(0), Bit(1)], [Bit(1), Bit(1), Bit(0)], [Bit(1), Bit(1), Bit(1)]]

And,

    from random import choice
    Z7 = Zmod(7)
    A = Matrix(6,9,fill=lambda r, c:choice(Z7))
    print A


Produces some random matrix in the integers mod 7:

    6 3	2	6	5	0	3	5	6
    4	3	3	5	1	5	0	3	5
    6	1	4	3	3	5	0	1	1
    0	6	3	1	5	1	3	6	2
    1	4	3	2	1	4	6	1	3
    5	2	4	1	4	5	5	5	6


And now some simple stuff:

    A.transpose()

Transposes a matrix. (A^T)

    A*B
    A+B

These operators work with matricies as well (provided that they are of the right dimensions of course)

    A.get_reduced_echelon()

Returns the row reduced echelon form of a matrix A.

    A.to_Zmod(11)

Gets a matrix in the finite field of integers mod 11.

More to come.
