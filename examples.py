from coding import *
from galois import *
from random import choice,randint

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

A = Matrix(6,9,fill=lambda r, c:choice(Z7))
B = Matrix(9,2,fill=lambda r, c:choice(Z7))

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

print "-A:"
print -A

raw_input()
print "### Linear Block Codes ###"

#make base 10 data set
data = [
    [1,0,0,1,2],
    [0,1,1,2,3]
]
#make matrix in GF(4)
G = Matrix(data=data).to_GF(4)

print "G:"
print G

code = LinearBlockCode(G)

print "H:"
print code.H

w = code.get_random_word()

print "w:"
print w
print Matrix(data=[to_base(w,4)])

c = Matrix(data=[code.encode([w])])

print "c:"
print c

print "c*H^T:"
print c*(code.H.transpose())

e = [0,0,0,0,0]
e[randint(0,4)]=randint(1,3)
e = Matrix(data=[e]).to_GF(4)

print "e:"
print e

print "c+e:"
print c+e

print "(c+e)*H^T"
print (c+e)*(code.H.transpose())

print "decode(c+e)"
print code.decode(c.get_row(0))[0]

#make base 10 data set
data = [
    [1,0,0,0,0,1,1],
    [0,1,0,0,1,0,1],
    [0,0,1,0,1,1,0],
    [0,0,0,1,1,1,1]
]
#make matrix in Zmod2
G = Matrix(data=data).to_Zmod(2)

print "G:"
print G

code = LinearBlockCode(G)

print "H:"
print code.H

w = code.get_random_word()

print "w:"
print w
print Matrix(data=[to_base(w,2)])

c = Matrix(data=[code.encode([w])])

print "c:"
print c

print "c*H^T:"
print c*(code.H.transpose())

e = Matrix(data=[[0,0,0,0,0,0,0]]).to_Zmod(2)
e.set(0,randint(0,6),FFE(1,2))

print "e:"
print e

print "c+e:"
print c+e

print "(c+e)*H^T"
print (c+e)*(code.H.transpose())

print "decode(c+e)"
print code.decode(c.get_row(0))[0]

print "test results of a 10% error rate chanel:"
rates = run_test(code, channel=TestChannel(.1))
for rate in rates:
    print "\t%s: %f"%(rate,rates[rate])

print "test results of a 25% error rate chanel:"
rates = run_test(code, channel=TestChannel(.25))
for rate in rates:
    print "\t%s: %f"%(rate,rates[rate])

print "test results of a 40% error rate chanel:"
rates = run_test(code, channel=TestChannel(.4))
for rate in rates:
    print "\t%s: %f"%(rate,rates[rate])

raw_input()
print "### Primes ###"
for n in xrange(1,11):
    print "The %d0,000th prime is: %d"%(n,get_prime(n*10000-1))

