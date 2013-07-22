from galois import *
from coding import *

print "9.1 - 1"
A = [
    [3, 7, 6],
    [4, 5, 3],
    [2, 4, 5]
]
b = [
    [2],
    [2],
    [4]
]
A = [[i%5 for i in row] for row in A]
A = Matrix(data=A).to_GF(5)
b = Matrix(data=b).to_GF(5)
aug = A.join_with(b)
print aug
aug = aug.get_reduced_echelon()
print ""
print aug
print ""
x = aug.submatrix(0,3,3,1)
print x
print ""
print A*x


print "9.1 - 4"
field = GF(13)
print get_latex_table(field, addition)
print get_latex_table(field, multiplication)


print "9.1 - 7"
for i in xrange(10):
    print i*5%10


print "9.2 - 1"
a = Polynomial([3,0,4,5]).to_GF(7)
b = Polynomial([5,3,6,0,4]).to_GF(7)
print a+b


print "9.2 - 4"
a = Polynomial([i%7 for i in [7,6,0,8,10]]).to_GF(7)
b = Polynomial([i%7 for i in [9,8,6,0,7]]).to_GF(7)
print a*b


print "9.2 - 7"
GF7x = [Polynomial(p) for p in GF(7)**5]
factors = []



poly = Polynomial([2,1,6,1,0,1]).to_GF(7)
zero = poly-poly
one = poly/poly
for i,x in enumerate(GF7x):
    if x.deg()<=1:
        continue
    while poly%x==zero:
        factors.append(x)
        poly = poly/x
    if poly==one:
        break
if poly!=one:
    factors.append(poly)
print "Factors:"
prod = one
for fac in factors:
    print fac
    prod = prod*fac
print "Product:"
print prod


print "9.3 - 1"
def my_format(elem, field):
    return elem.i.to_latex() 
field = GF(4)
print get_latex_table(field, addition, formatting=my_format)
print get_latex_table(field, multiplication, formatting=my_format)


print "9.3 - 4"
field = GF(4)
latex = "\\begin{tabular}{c|c|c|c|c|c|c|c}\n"
latex+= "a & b & c & a+b & ac & bc & (a+b)c & ac+bc\\\\\n"
for i,a in enumerate(field):
    for j,b in enumerate(field):
        for k,c in enumerate(field):
            latex+= "\\hline\n"
            latex+= a.i.to_latex()
            latex+= " & "
            latex+= b.i.to_latex()
            latex+= " & "
            latex+= c.i.to_latex()
            latex+= " & "
            latex+= (a+b).i.to_latex()
            latex+= " & "
            latex+= (a*c).i.to_latex()
            latex+= " & "
            latex+= (b*c).i.to_latex()
            latex+= " & "
            latex+= ((a+b)*c).i.to_latex()
            latex+= " & "
            latex+= (a*c+b*c).i.to_latex()
            latex+= "\\\\\n"
latex+="\\end{tabular}"
print latex


print "9.4 - 4"
A = [
    [3, 13],
    [14, 5]
]
A = Matrix(data=A).to_GF(16)
b = Matrix(data=[[7,9]]).transpose().to_GF(16)
aug = A.join_with(b)
print aug
aug = aug.get_reduced_echelon()
print ""
print aug
print ""
x = aug.submatrix(0,2,2,1)
print x
print ""
print A*x

print "9.4 - 7"
GF2x = [Polynomial(p) for p in GF(2)**4]
factors = []
poly = Polynomial([1,1,0,0,0,1]).to_GF(2)
zero = poly-poly
one = poly/poly
for i,x in enumerate(GF2x):
    if x.deg()<=1:
        continue
    while poly%x==zero:
        factors.append(x)
        poly = poly/x
    if poly==one:
        break
if poly!=one:
    factors.append(poly)
print "Factors:"
prod = one
for fac in factors:
    print fac.to_latex()
    prod = prod*fac
print "Product:"
print prod


print "9.5 - 1"
Zmodx = Zmod(5)
deg2 = [Polynomial(p) for p in Zmodx**3]
deg2 = [p for p in deg2 if p.deg()==2]
deg1 = [Polynomial(p) for p in Zmodx**2]
deg1 = [p for p in deg1 if p.deg()==1]
irs = []
for p in deg2:
    if not is_reducable(p, deg1):
        irs.append("$"+p.to_latex()+"$")
table = []
for i in xrange(10):
    table.append(irs[:4])
    irs = irs[4:]
table = [" & ".join(row) for row in table]
table = "\\\\\n\\hline\n".join(table)
print table


print "9.5 - 7"
GF27x = GF(27)
lst = []
for poly in GF27x[1:]:
    if ord(poly)==26:
        lst.append("$"+poly.i.to_latex()+"$")
table = []
for i in xrange(3):
    table.append(lst[:4])
    lst = lst[4:]
table = [" & ".join(row) for row in table]
table = "\\\\\n\\hline\n".join(table)
print table


print "9.5 - 10"
print "a"
field = GF(3)
print get_latex_table(field, addition)
print get_latex_table(field, multiplication)

print "b"
Zmodx = Zmod(3)
deg2 = [Polynomial(p) for p in Zmodx**3]
deg2 = [p for p in deg2 if p.deg()==2]
deg1 = [Polynomial(p) for p in Zmodx**2]
deg1 = [p for p in deg1 if p.deg()==1]
irs = []
for p in deg2:
    if not is_reducable(p, deg1):
        irs.append("$"+p.to_latex()+"$")
print len(irs)
table = []
for i in xrange(2):
    table.append(irs[:3])
    irs = irs[3:]
table = [" & ".join(row) for row in table]
table = "\\\\\n\\hline\n".join(table)
print table

print "c"
GF3x = [Polynomial(p) for p in GF(3)**9]
factors = []
poly = Polynomial([0,1]+[0]*7+[1]).to_GF(3)
print poly
zero = poly-poly
one = poly/poly
for i,x in enumerate(GF3x):
    if x.deg()<=1:
        continue
    while poly%x==zero:
        factors.append(x)
        poly = poly/x
    if poly==one:
        break
if poly!=one:
    factors.append(poly)
print "Factors:"
prod = one
for fac in factors:
    print fac.to_latex()
    prod = prod*fac
print "Product:"
print prod


print "9.6 - 1"
field = GF(13)
for d in [d for d in xrange(2,13) if 12%d==0]:
    print "Divisor:",d
    p = phi(d)
    print "phi(%d)=%d"%(d,p)
    count = 0
    for e in field[1:]:
        if ord(e)==d:
            count+=1
            print e
    print count==p
