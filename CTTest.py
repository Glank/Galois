from coding import *
from absalg import *
from random import choice

print "### Finite Fields ###"

print "Z_7:"
Z7 = Zmod(7)
print Z7

for z in Z7:
	if z.i == 0:
		continue
	print "%s*%s"%(str(z),str(z.mul_inv()))
	print z*z.mul_inv()

print "(Z_2)^3:"
Z2 = Zmod(2)
print Z2**3

raw_input()
print "### Matricies ###"

A = Matrix(6,9,fill=lambda:choice(Z7))
B = Matrix(9,2,fill=lambda:choice(Z7))

print "A:"
print A

print "A^T:"
print Matrix.transpose(A)

print "(A^T)^T:"
print A.transpose().transpose()

print "B:"
print B

print "(A*B)^T:"
print (A*B).transpose()

print "B^T*A^T:"
print B.transpose()*A.transpose()

print "A reduced echelon:"
print A.get_reduced_echelon()



