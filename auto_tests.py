from galois import *

#prime mod fields
z7 = Zmod(7)

assert (z7[2]+z7[6])==z7[1]
assert (z7[3]-z7[4])==z7[6]
assert (z7[4]*z7[4])==z7[2]
assert (z7[5]/z7[2])==z7[6]
assert is_field(z7)

z2_3 = Zmod(2)**3

assert len(z2_3)==8
assert z2_3[5]==[FFE(1,2),FFE(0,2),FFE(1,2)]

#galois fields
gf8 = GF(8)

assert (gf8[5]+gf8[6])==gf8[3]
assert (gf8[1]-gf8[5])==gf8[4]
assert (gf8[3]*gf8[2])==gf8[7]
assert (gf8[2]/gf8[3])==gf8[3]
assert is_field(gf8)
assert is_group(gf8[1:], addition=multiplication)

gf4 = GF(4)
gf4_2 = gf4**2

assert len(gf4_2)==16
assert gf4_2[7]==[gf4[1], gf4[3]]

#primes
assert get_prime(39)==173

from coding import *

#matricies

#mult
a = Matrix(data=[
        [1,2,3],
        [4,5,6]
    ])
x = Matrix(data=[[9,8,7]]).transpose()
b = a*x
assert b==Matrix(data=[[46,118]]).transpose()

#add, sub
a = Matrix(data=[[5,3,7]]).to_Zmod(11)
b = Matrix(data=[[10,8,6]]).to_Zmod(11)
assert a+b==Matrix(data=[[4,0,2]]).to_Zmod(11)
assert a-b==Matrix(data=[[6,6,1]]).to_Zmod(11)

#solutions to equations
a = [
    [3,7,2],
    [7,3,1],
    [5,6,4]
]
a = Matrix(data=a).to_GF(8)
x = Matrix(data=[[7,5,3]]).transpose().to_GF(8)
b = a*x

aug = a.join_with(b)
solve = aug.get_reduced_echelon().submatrix(0,3,3,1)

assert solve==x


print "All Tests Passed."
