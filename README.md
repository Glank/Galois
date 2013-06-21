CodingTheory
============

Coding Theory math utilities in python.
It can help to do coding theory homework, but I wouldn't trust it for any real-world applications.

For examples of usage, please see test.py


Some impressive stuff (not really):
-----------------------------------

    print Zmod(2)**3

Prints the size 3 vector space of the finite field of two elements. (All binary words of length 3):

    [[Bit(0), Bit(0), Bit(0)], [Bit(0), Bit(0), Bit(1)], [Bit(0), Bit(1), Bit(0)], [Bit(0), Bit(1), Bit(1)], [Bit(1), Bit(0), Bit(0)], [Bit(1), Bit(0), Bit(1)], [Bit(1), Bit(1), Bit(0)], [Bit(1), Bit(1), Bit(1)]]

And,

    from random import choice
    Z7 = Zmod(7)
    A = Matrix(6,9,fill=lambda r, c:choice(Z7))
    print A


Produces some random matrix in the integers mod 7:

    6   3	2	6	5	0	3	5	6
    4	3	3	5	1	5	0	3	5
    6	1	4	3	3	5	0	1	1
    0	6	3	1	5	1	3	6	2
    1	4	3	2	1	4	6	1	3
    5	2	4	1	4	5	5	5	6


And now some simple stuff:
--------------------------

You can create elements in a finite field like this,

    a = FFE(8, 13)
    b = FFE(12, 13)

And then do simple operations with them:

    print a+b
    print a-b
    print a*b
    print b/a

prints:

    7
    9
    5
    8
    
You can also make matricies. By default they are in the real domain:

    A = Matrix(rows,cols)

Creates a simple, empty matrix. Getting and setting values is rather obvious:

    A.set(row,col,value)
    print A.get(row,col)

These operators work with matricies as well (provided that they are of the right dimensions of course):

    C = A*B
    C = A+B
    C = A-B

Transposes a matrix. (A^T):

    A = A.transpose()

Row reduce to reduced echelon form of a matrix A:

    A = A.get_reduced_echelon()

Move the matrix into the finite field of integers mod 11.

    A = A.to_Zmod(11)

There's more to come.
