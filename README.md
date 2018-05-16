Galois
======

Galois is a set of math utilities for finite fields and coding theory applications in Python.
The tool is still in development but will be completed by the end of this summer.
This implementation is built for python v2.

For examples of simple usage, please see 
<a href="https://github.com/Glank/Galois/blob/master/examples.py">examples.py</a>.
There are many more advanced examples in that file than are shown below.

Jumping In - A Realistic Example:
---------------------------------

So say you're working in GF(8) and you want to solve a system of equations, specifically:

    3x + 7y + 2z = 5
    7x + 3y +  z = 5
    5x + 6y + 4z = 1

Using Galois with Python, you can create two matricies to represent this equation in the form Ax=b:

    from galois import GF
    from coding import Matrix
    A = Matrix(data=[
            [3,7,2],
            [7,3,1],
            [5,6,4]
        ]).to_GF(8)
    b = Matrix(data=[[5,5,1]]).transpose().to_GF(8)
    
Then you can create an augmented matrix and sovle:

    aug = A.join_with(b)
    solution = aug.get_reduced_echelon().submatrix(0,3,3,1)
    print solution

Where `.submatrix(0,3,3,1)` is the part of the row reduced augmented matrix that is
`0` rows from the top, `3` colums from the left, and is `3x1`.
The program should print:

    GF(8)[7]
    GF(8)[5]
    GF(8)[3]

And now some simple stuff:
--------------------------

You can create elements in a simple prime-modulo finite field like this,

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
    
Or you can create whole Galois fields like this:

    gf25 = GF(25)
    a = gf25[7]
    b = gf25[13]

Which would store the seventh and thirteenth elements of the 25-element finite field to the variables `a` and `b` respectively.
    
You can also make empty matricies if you import them from the `coding` module (included).
By default they are in the real domain:

    A = Matrix(rows,cols)

Creates a simple, empty matrix. Getting and setting values is easy:

    A.set(row,col,value)
    print A.get(row,col)

These simple operators work with matricies as well (provided that they are of the right dimensions of course):

    C = A*B
    C = A+B
    C = A-B

Transposes a matrix. (A^T):

    A = A.transpose()

Row reduce to reduced echelon form of a matrix A:

    A = A.get_reduced_echelon()

Move the matrix into the finite field of integers mod 11.

    A = A.to_Zmod(11)

Or generally to any Galois field `p^n`

    A = A.to_GF(27)

You can create polynomials using any field elements as constants.

    poly = Polynomial([9,2,6,2])
    print poly

prints:

    (9)x^0+(2)x^1+(6)x^2+(2)x^3
    
You can also add, subtract, multiply, and divide polynomials.
