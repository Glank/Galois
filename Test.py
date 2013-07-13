from absalg import *

m = 3 

Zmodx3 = Zmod(m)**4
Zmodx3 = [Polynomial(p) for p in Zmodx3]
Zmodx2 = Zmod(m)**3
Zmodx2 = [Polynomial(p) for p in Zmodx2]

for p in Zmodx2:
	print p

#	mod = Polynomial([1,1,1])
#	mod = mod.to_Zmod(m)

for mod in Zmodx3:
	print ""
	zero = mod-mod
	if mod==zero:
		continue
	one = mod/mod
	
	good = True
	unique = []
	for a in Zmodx2:
		if not a%mod in unique:
			unique.append(a)
	for a in unique: 
		wasOne = False
		for b in unique:
			if not (a*b)%mod in unique:
				print "Error:"
				print a
				print b
				print a*b
				print (a*b)%mod
			if (a*b)%mod==one:
				wasOne = True
		if not wasOne and a != zero:
			good = False
		if not a%mod in unique:
			unique.append(a)
	if good:
		def addition(a,b):
			return (a+b)%mod
		def multiplication(a,b):
			return (a*b)%mod
		print mod
		"""print is_field(unique,
			addition,
			multiplication
		)"""
		#unique = [FFE(a,mod) for a in unique]
		#print unique
		print "!!!!!!Good!!!!!!"
		prime = True
		try:
			for d in Zmodx3:
				if d == mod:
					raise Exception()
				if d!=one and d!=zero and mod%d==zero:
					print "-",d
					prime = False
		except:
			pass
		print prime
		print "Size:",len(unique)
	else:
		prime = True
		for d in Zmodx3:
			if d!=zero and d!=mod and mod%d==zero:
				prime = False
		if prime:
			print mod
			print "Wut?"
