from absalg import *

p = 3
n = 4

print FFE(5,7)

mod = Polynomial([FFE(e,p) for e in [1]*(n+1)])
Zmodx = Zmod(p)**n
Zmodx = [Polynomial(poly) for poly in Zmodx]
field = [FFE(poly, mod, field=Zmodx) for poly in Zmodx]

for a in field:
	for b in field:
		if b!=field[0]:
			print "#"*10
			print "%r"%b
			print "%r"%b.mul_inv()
			print "%r"%(a*b)
			print "%r"%(a/b)
		if b!=field[0] and (a*b)/b != a:
			print "Error!"
			exit()

x = field[8]/field[6]
print x
x = field[10]/x
print x
x = field[11]/x
print x
print x/x

print "We good."
