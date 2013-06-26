from absalg import *
from coding import *

print "problem 3"

G = [
	[1,0,0,0,1,1,0],
	[0,1,0,0,1,0,1],
	[0,0,1,0,1,1,1],
	[0,0,0,1,0,1,1]
]
G = Matrix(data=G).to_Zmod(2)

code = LinearBlockCode(G)

for w in xrange(code.words):
	print "%s ->\t%s"%(
		str(code.get_word_matrix(w)),
		Matrix(data=[code.encode([w])]))

def decode(c, code):
	c = [Bit(b) for b in c]
	w = code.decode(c)[0]
	w = to_base(w,2)
	w = [int(b) for b in w]
	while len(w)<4:
		w = [0]+w
	return w

print decode([0,0,0,0,1,1,0],code)
print decode([1,1,1,0,1,0,0],code)

print "problem 5"

G = [
	[1,0,0,1,1,0],
	[0,1,0,1,0,1],
	[0,0,1,1,1,1]
]
G = Matrix(data=G).to_Zmod(2)

code = LinearBlockCode(G)

for w in xrange(code.words):
	print "%s ->\t%s"%(
		str(code.get_word_matrix(w)),
		Matrix(data=[code.encode([w])])
	)

print "problem 12"

G = [
	[1, 0, 1, 1],
	[0, 1, 2, 1]
]
G = Matrix(data=G).to_Zmod(3)

code = LinearBlockCode(G)

for w in xrange(code.words):
	print "%s \n&\implies\n %s\\\\"%(
		code.get_word_matrix(w).to_latex(),
		Matrix(data=[code.encode([w])]).to_latex()
	)

print "H="

print code.H.transpose().to_latex()

received = [1,2,0,1]
received = [FFE(r,3) for r in received]
word = code.decode(received)[0]
print to_base(word,3)
code_word = code.encode([word])
print code_word

print "problem 13"

A = [
	[1, 1, 1],
	[1, 0, 1],
	[1, 1, 0],
	[0, 1, 1]
]
A = Matrix(data=A)

I = Matrix.get_identity(4)

G = I.join_with(A).to_Zmod(2)

print "G="
print G

code = LinearBlockCode(G)

for w in xrange(code.words):
	print "%s \n&\implies\n %s\\\\"%(
		code.get_word_matrix(w).to_latex(),
		Matrix(data=[code.encode([w])]).to_latex()
	)

print "H="
print code.H.transpose().to_latex()
print "weight:"
print code_weight(code, 0) 
