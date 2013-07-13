from absalg import *
from coding import *

print "Exercise 9.1 - 1"
Ax = [
	[3, 7, 6, 2],
	[4, 5, 3, 2],
	[2, 4, 5, 4]
]
Ax = Matrix(data=Ax)
Ax = Ax.to_Zmod(5)
Ax = Ax.get_reduced_echelon()
print Ax

print "Exercise 9.2 - 1"
p1 = [3, 0, 4, 5]
p2 = [5, 3, 6, 0, 4]
p1 = Polynomial(p1).to_Zmod(7)
p2 = Polynomial(p2).to_Zmod(7)
print p1+p2
print "Exercise 9.2 - 3"
print p1*p2

factors =  factor(9248592)
print factors
print factors[0]*factors[1]

print "Exercise 9.2 - 7"
p = [2, 1, 6, 1, 0, 1]
p = Polynomial(p).to_Zmod(7)
def factor(p):
	zero = Polynomial([FFE(0, 7)])
	factors = [p]
	possibles = Zmod(7)**(p.deg()-1)
	[pos.reverse() for pos in possibles]
	possibles = [Polynomial(pos) for pos in possibles]
	possibles = [pos for pos in possibles if pos.deg()>0]
	for possible in possibles:
		if p%possible==zero:
			factors = [possible]
			p/=possible
			if p.deg()>2:
				factors+= factor(p)
			else:
				factors.append(p)
			break
	return factors
factors = factor(p)
for factor in factors:
	print factor


