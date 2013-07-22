from galois import *
from coding import *

#17
g = [
	[1, 0, 0, 1, 1, 0],
	[0, 1, 0, 0, 1, 1],
	[0, 0, 1, 1, 0, 1]
]
g = Matrix(data=g).to_GF(2)
c = LinearBlockCode(g)

ws = [0, 0, 1, 0, 0, 1,
	 0, 1, 1, 0, 0, 0,
	 0, 0, 0, 1, 1, 0,
	 1, 0, 0, 0, 0, 1]
ws = [FFE(i,2) for i in ws]

words = c.decode(ws)
print words

#19
print "-"*20
g = [
	[1, 0, 0, 0, 1, 1, 0],
	[0, 1, 0, 0, 1, 0, 1],
	[0, 0, 1, 0, 1, 1, 1],
	[0, 0, 0, 1, 0, 1, 1]
]
g = Matrix(data=g).to_GF(2)
lbc = LinearBlockCode(g)

words = GF(2)**4
code_words = [lbc.encode([w]) for w in xrange(2**4)]
zero = [FFE(0,2)]*7
deltas = [d for d in GF(2)**7 if hamming_distance(d,zero)>=2]

def v_to_s(v):
	return "".join([str(i) for i in v])

out = open("temp.txt", 'w')
for c,code in enumerate(code_words):
	for delta in deltas:
		off = (Matrix(data=[code])+Matrix(data=[delta])).data[0]
		decode = to_base(lbc.decode(off)[0], 2)
		while len(decode) < 4:
		    decode = [FFE(0,2)]+decode
		latex = v_to_s(words[c])
		latex+=" & "+v_to_s(code)
		latex+=" & "+v_to_s(delta)
		latex+=" & "+v_to_s(off)
		latex+=" & "+v_to_s(decode)
		latex+="\\\\\n\\hline\n"
		out.write(latex)
		if words[c]==decode:
			print "ERROR"
out.close()

#29
print "Problem 29"
g = [
	[1, 0, 0, 1, 2],
	[0, 1, 1, 2, 3]
]
g = Matrix(data=g).to_GF(4)
lbc = LinearBlockCode(g)
GF4 = GF(4)
GF4_5 = GF4**5
zero = [GF4[0]]*5
print zero
deltas = [d for d in GF4_5 if hamming_distance(d, zero)==1]
for word in lbc.word_iter():
    for delta in deltas:
        received = lbc.encode([word])
        received = (Matrix(data=[received])+Matrix(data=[delta]))
        received = received.data[0]
        decoded = lbc.decode(received)[0]
        if decoded != word:
            print "ERROR"
print lbc.words


