from absalg import *

def is_prime(i, numbers):
	for j in xrange(1, i):
		if numbers[j]%numbers[i]==numbers[0]:
			return False
	return True

#p^n#
p = 3
n = 3
Zmodx = Zmod(p)**(n+1)
Zmodx = [Polynomial(poly) for poly in Zmodx]
primes = (Zmodx[i] for i in xrange(len(Zmodx)) if is_prime(i, Zmodx))
mod = None
for prime in primes:
	if prime.deg() == n:
		mod = prime
if mod is None:
	print "Error"

Zmodx = Zmod(p)**n
Zmodx = [Polynomial(poly) for poly in Zmodx]
Zmodx = [FFE(poly, mod) for poly in Zmodx]
for poly in Zmodx:
	print poly
print len(Zmodx)


mod = Polynomial([FFE(e, p) for e in [1]*(n+1)])
Zmodx = Zmod(p)**n
Zmodx = [Polynomial(poly) for poly in Zmodx]
Zmodx = [FFE(poly, mod) for poly in Zmodx]
print Zmodx

print is_field(Zmodx)
