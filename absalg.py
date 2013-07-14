import math
import operator
import copy

def to_base(number, base):
	assert number>=0
	assert base>1
	ret = []
	i = 0
	while number > 0:
		digit = number%base
		ret = [FFE(digit, base)]+ret
		number/=base
	if len(ret) == 0:
		ret = [FFE(0, base)]
	if base==2:
		ret = [Bit(i.i) for i in ret]
	return ret

_primes = [2,3]
def is_prime(n):
	i = 0
	sqrt = math.sqrt(n)
	while get_prime(i)<=sqrt:
		if n%get_prime(i)==0:
			return False
		i+=1
	return True
def next_prime(p):
	i = p+1
	while not is_prime(i):
		i+=1
	return i
def get_prime(n):
	global _primes
	if n < len(_primes):
		return _primes[n]
	while n >= len(_primes):
		_primes.append(next_prime(_primes[-1]))
	return _primes[n]
def factor(n):
	i = 0
	factors = []
	while n!=1:
		while n%get_prime(i)==0:
			factors.append(get_prime(i))
			n/=get_prime(i)
		i+=1
	return factors

def addition(a,b):
	return a+b
def multiplication(a,b):
	return a*b

def is_group(elems, addition=addition):
	"""A proof by contradiction that the set 'elems' is not a Group
	under 'addition'."""
	#To prove by contradiction that there is an additive identity,
	#we will assume that the opposite is true. 
	zero = None
	#The following is a proof by cases that an additive identity exists
	#and that addition is a closure.
	#Let 'a' be an element in 'elems' and
	for a in elems:
		#assume that a = 0.
		isZero = True
		#Let 'b' be an element in 'elems'.
		for b in elems:
			#If 'a+b=0' then
			if not addition(a,b) in elems:
				#'elems' is not a group under addition.
				return False
			#For all 'c' in the set 'elems',
			for c in elems:
				#Let...
				#sum1 = (a+b)+c
				#sum2 = a+(b+c)
				sum1 = addition(addition(a,b),c)
				sum2 = addition(a,addition(b,c))
				#Addition is not associative if 'sum1' does not
				#equal 'sum2'
				if sum1 != sum2:
					#so 'elems' is not a group under addition.
					return False
			#If a+b does not equal b then...
			if addition(a,b)!=b or addition(b,a)!=b:
				#a is not equal to zero
				isZero = False
		#
		if isZero:
			zero = a
	#has zero element
	if zero is None:
		return False
	#has subtraction
	for a in elems:
		hasInverse = False
		for b in elems:
			if addition(a,b)==zero and addition(b,a)==zero:
				hasInverse = True
		if not hasInverse:
			return False
	#passed every test
	return True

def is_ring(elems, addition=addition, multiplication=multiplication):
	#is also a group under addition
	if not is_group(elems, addition):
		return False, "Is Not group"
	for a in elems:
		for b in elems:
			#addition is communicative
			if addition(a,b)!=addition(b,a):
				return False, "Addition is not communicative"
			#multiplication is closed
			if not multiplication(a,b) in elems:
				return False, "Multiplication isn't a closure."
			for c in elems:
				#multiplication is associative
				prod1 = multiplication(multiplication(a,b),c)
				prod2 = multiplication(a,multiplication(b,c))
				if prod1!=prod2:
					return False, "Multiplication is not associative"
				#distribution works
				result1 = multiplication(a,addition(b,c))
				left = multiplication(a,b)
				right = multiplication(a,c)
				result2 = addition(left,right)
				if result1!=result2:
					return False, "Distribution doesn't work"
				result1 = multiplication(addition(b,c),a)
				left = multiplication(b,a)
				right = multiplication(c,a)
				result2 = addition(left,right)
				if result1!=result2:
					return False, "Distribution doesn't work"
	return True

def is_field(elems, addition=addition, multiplication=multiplication):
	#is also a ring
	if not is_ring(elems, addition, multiplication):
		return False, "Is Not Ring"
	# check that multiplication is communative
	# and get zero
	zero = None
	for a in elems:
		isZero = True
		for b in elems:
			if multiplication(a,b)!=multiplication(b,a):
				return False, "Multiplication is not communative"
			if addition(a,b)!=b:
				isZero = False
			if addition(b,a)!=b:
				isZero = False
		if isZero:
			zero = a
	# check that there is a multiplicative identity
	one = None
	for a in elems:
		#by cases
		isOne = True
		for b in elems:
			if b is not zero:
				if multiplication(a,b)!=b or multiplication(b,a)!=b:
					isOne = False
		if isOne:
			one = a
	if one is None:
		return False, "No multiplicative identity"
	#the element is a field
	return True
		
class FFE:
	"""An element of a finite field."""
	
	def __init__(self, i, p, field=None, mulinv=None):
		self.i = i
		self.p = p
		self.mulinv = mulinv
		self.field = field

	def __add__(self, other):
		if isinstance(other,FFE):
			assert self.p == other.p
			return FFE((self.i+other.i)%self.p,self.p,field=self.field)
		else:
			return other.__radd__(self)

	def __sub__(self, other):
		if isinstance(other,FFE):
			assert self.p == other.p
			return FFE((self.i-other.i)%self.p,self.p,field=self.field)
		else:
			return other.__rsub__(self)

	def __mul__(self, other):
		if isinstance(other,FFE):
			assert self.p == other.p
			return FFE((self.i*other.i)%self.p,self.p,field=self.field)
		else:
			return other.__rmul__(self)

	def __div__(self, other):
		if isinstance(other,FFE):
			assert self.p == other.p
			return self*other.mul_inv()
		else:
			return other.__rdiv__(self)

	def mul_inv(self):
		if self.mulinv is not None:
			return self.mulinv
		if self.field is not None and self.mulinv is None:
			zero = self.i-self.i
			one = self.p/self.p
			for e in self.field:
				if e!=zero and (e*self.i)%self.p==one:
					self.mulinv = FFE(e,self.p,
						field=self.field,mulinv=self
					)
			return self.mulinv
		zero = self.i-self.i
		assert self.i!=zero
		one = self.i/self.i
		u = self.i
		v = self.p
		x1 = one
		x2 = zero
		while u!=one:
			print "u:",u
			print "v:",v
			q = v//u
			r = v-q*u
			x = x2-q*x1
			v = u
			u = r
			x2 = x1
			x1 = x
		self.mulinv = FFE(x1%self.p,self.p,mulinv=self)
		return self.mulinv

	def __pow__(self, other):
		return FFE((self.i**int(other))%self.p,self.p)
	
	def __neg__(self):
		return FFE((self.p-self.i)%self.p,self.p)

	def __eq__(self, other):
		assert self.p == other.p
		return self.i == other.i

	def __ne__(self, other):
		assert self.p == other.p
		return self.i != other.i

	def __str__(self):
		return "%s"%str(self.i)

	def __repr__(self):
		return "FFE(%s,%s)"%(str(self.i),str(self.p))

	def __nonzero__(self):
		return self.i!=0

	def __int__(self):
		return self.i

	def __float__(self):
		return float(self.i)

	def __complex__(self):
		return complex(self.i)

	def __long__(self):
		return long(self.i)
	
	def __oct__(self):
		return oct(self.i)

	def __hex__(self):
		return hex(self.i)

class Bit(FFE):
	def __init__(self, i):
		i = 1 if i else 0
		FFE.__init__(self, i, 2)

	def __not__(self):
		return Bit((self.i+1)%2)

	def __invert__(self):
		return self.__not__()

	def __repr__(self):
		return "Bit(%d)"%self.i

class Polynomial:
	def __init__(self, coefficients):
		assert len(coefficients)>0
		self.coefficients = coefficients
		self._trim_()

	def _zero_(self):
		return self.coefficients[0]-self.coefficients[0]

	def _trim_(self):
		zero = self._zero_()
		while self.deg() > 0 and self.coefficients[-1]==zero:
			self.coefficients.pop()
		
	def to_Zmod(self, mod):
		coefficients = self.coefficients
		if mod != 2:
			return Polynomial([FFE(c%mod,mod) for c in coefficients])
		return Polynomial([Bit(c%2) for c in coefficients])

	def deg(self):
		return len(self.coefficients)-1

	def __neg__(self):
		return Polynomial([-c for c in self.coefficients])

	def __add__(self, other):
		result = []
		zero = self._zero_()
		for i in xrange(max(self.deg(), other.deg())+1):
			coef = zero
			if i <= self.deg():
				coef = coef+self.coefficients[i]
			if i <= other.deg():
				coef = coef+other.coefficients[i]
			result.append(coef)
		return Polynomial(result)

	def __sub__(self, other):
		return self+(-other)

	def __mul__(self, other):
		results = []
		for a in self.coefficients:
			results.append([])
			for b in other.coefficients:
				results[-1].append(a*b)
		result = results.pop(0)
		zero = self._zero_()
		for coresult in results:
			result.append(zero)
			for i in xrange(len(coresult)):
				result[-i-1]+= coresult[-i-1]
		return Polynomial(result)

	def __pow__(self, i):
		assert i>=1
		result = copy.deepcopy(self)
		for j in xrange(i-1):
			result = result*self
		return result

	def __str__(self):
		ret = ""
		for i in xrange(self.deg()+1):
			if i!=0:
				ret+="+"
			ret += "(%s)x^%d"%(str(self.coefficients[i]),i)
		return ret

	def __divmod__(self, other):
		remainder = copy.deepcopy(self)	
		zero = self._zero_()
		p_zero = Polynomial([zero])
		one = other.coefficients[-1]/other.coefficients[-1]
		if other==Polynomial([one]):
			return (self, Polynomial([zero]))
		x = Polynomial([zero, one])
		quotient = Polynomial([zero])
		while remainder != p_zero and remainder.deg()>=other.deg():
			r_lead = remainder.coefficients[-1]
			o_lead = other.coefficients[-1]
			q_part = Polynomial([r_lead/o_lead])
			q_deg = remainder.deg()-other.deg()
			if q_deg > 0:
				q_part*= x**q_deg
			r_sub = other*q_part
			remainder-=r_sub
			quotient+=q_part
		return (quotient, remainder)

	def __mod__(self, other):
		return divmod(self, other)[1]

	def __eq__(self, other):
		if self.deg() != other.deg():
			return False
		for s_c, o_c in zip(self.coefficients, other.coefficients):
			if s_c != o_c:
				return False
		return True

	def __ne__(self, other):
		return not self==other

	def __div__(self, other):
		div, mod = divmod(self, other)
		assert mod == Polynomial([self._zero_()])
		return div

	def __floordiv__(self, other):
		return divmod(self, other)[0]

	def __repr__(self):
		return str(self)

class Matrix:
	def __init__(self, rows=1, cols=1, data=[], fill=None):
		self.rows = rows
		self.cols = cols
		if data:
			self.data = data
			self.rows = len(data)
			self.cols = len(data[0])
		else:
			self.data = []
			for r in xrange(rows):
				if hasattr(fill,'__call__'):
					row = [fill(r,c) for c in xrange(cols)]
				else:
					row = [fill for c in xrange(cols)]
				self.data.append(row)

	@staticmethod
	def get_identity(size):
		data = []
		for r in xrange(size):
			data.append([])
			for c in xrange(size):
				data[r].append(1 if r == c else 0)
		return Matrix(data=data)
	
	def to_Zmod(self, base):
		if base == 2:
			return Matrix(self.rows, self.cols, 
				fill=lambda r,c:Bit(self.get(r,c)%2))
		return Matrix(self.rows, self.cols, 
			fill=lambda r,c:FFE(self.get(r,c)%base,base))

	def join_with(self, other):
		assert self.rows == other.rows
		def get(r,c):
			if c<self.cols:
				return self.get(r,c)
			return other.get(r,c-self.cols)
		return Matrix(self.rows,self.cols+other.cols,fill=get)

	def get(self,r,c):
		return self.data[r][c]

	def set(self,r,c,value):
		self.data[r][c] = value

	def get_row(self,r):
		return self.data[r]
	
	def set_row(self,r,row):
		self[r] = row

	def __add__(self, other):
		assert self.rows == other.rows
		assert self.cols == other.cols
		newData = []
		for r in xrange(self.rows):
			row = [x+y for (x,y) in 
				zip(self.get_row(r), other.get_row(r))]
			newData.append(row)
		return Matrix(data=newData)

	def __sub__(self, other):
		assert self.rows == other.rows
		assert self.cols == other.cols
		newData = []
		for r in xrange(self.rows):
			row = [x-y for (x,y) in 
				zip(self.get_row(r), other.get_row(r))]
			newData.append(row)
		return Matrix(data=newData)
	
	def __mul__(self, other):
		if isinstance(other, Matrix):
			assert self.cols == other.rows
			zero = self.get(0,0)
			zero = zero-zero
			data = []
			for i in xrange(self.rows):
				data.append([])
				for j in xrange(other.cols):
					data[i].append(zero)
					for k in xrange(self.cols):
						data[i][j]+=self.get(i,k)*other.get(k,j)
			return Matrix(data=data)
		else:
			data = []
			for r in xrange(self.rows):
				data.append([])
				for c in xrange(self.cols):
					data[r].append(self.data[r][c]*other)
			return Matrix(data=data)
	
	def __rmul__(self, other):
		return self.__mul__(other)

	def __pow__(self, other):
		p = int(other)
		assert p>=1
		assert self.rows == self.cols
		result = copy.deepcopy(self)
		for i in xrange(p-1):
			result*=self
		return result

	def __neg__(self):
		data = []
		for r in xrange(self.rows):
			data.append([])
			for c in xrange(self.cols):
				 data[r].append(-self.get(r,c))
		return Matrix(data=data)

	def __eq__(self, other):
		if self.rows != other.rows:
			return False
		if self.cols != other.cols:
			return False
		for r in xrange(self.rows):
			for c in xrange(self.cols):
				if self.get(r,c) != other.get(r,c):
					return False
		return True

	def __ne__(self, other):
		return not self == other

	def __str__(self):
		def join_row(row):
			return "\t".join([str(value) for value in row])
		rows = [join_row(row) for row in self.data]
		return "\n".join(rows)

	def to_latex(self):
		def join_row(row):
			return " & ".join([str(value) for value in row])
		rows = [join_row(row) for row in self.data]
		ret = "\\\\\n".join(rows)
		ret = "\\left[\\begin{tabular}{"+"c"*self.cols+"}\n"+ret
		ret = ret+"\\end{tabular}\\right]"
		return ret

	def transpose(self):
		data = []
		for c in xrange(self.cols):
			data.append([])
			for r in xrange(self.rows):
				data[c].append(self.get(r,c))
		return Matrix(data=data)

	def get_reduced_echelon(self):
		m = copy.deepcopy(self)	
		def get_pivot(matrix, r, c):
			for i in xrange(r, matrix.rows):
				v = matrix.get(i,c)
				if v != v-v:
					return i
			return None
		def swap_rows(matrix, r1, r2):
			row = matrix.data[r1]
			matrix.data[r1]=matrix.data[r2]
			matrix.data[r2]=row
		def div_row(matrix, row, value):
			matrix.data[row] = [v/value for v in matrix.data[row]]
		def get_row_mult(matrix, row, mult):
			return [v*mult for v in matrix.data[row]]	
		def row_add(matrix, row, add):
			for i in xrange(len(add)):
				matrix.data[row][i] = matrix.data[row][i]+add[i]
		r = 0
		for c in xrange(m.cols):
			pivot = get_pivot(m, r, c)
			if pivot is not None:
				swap_rows(m, r, pivot)
				pivot = r
				div_row(m, r, m.get(r,c))
				for i in xrange(m.rows):
					if i == r:
						continue
					add = get_row_mult(m, r, -m.get(i,c))
					row_add(m,i,add)
				r+=1
			if r>=m.rows:
				break
		return m

class Zmod(list):
	def __init__(self, p):
		list.__init__(self)
		self.n = p
		for i in xrange(p):
			self.append(FFE(i,p) if p!=2 else Bit(i))

	def __pow__(self, n):
		assert n>=1
		perms = [[i] for i in self]
		for i in xrange(1,n):
			new_perms = []
			for perm in perms:
				for new in self:
					new_perms.append(perm+[new])
			perms = new_perms
		return perms

class GF(list):
	def __init__(self, n):
		list.__init__(self)
		self.n = n
		factors = factor(n)
		p = factors[0]
		for f in factors:
			assert f == p
		if len(factors)==1:
			Zmod.__init__(self, p)
		else:
			Zmodx = Zmod(p)**(len(factors))
			Zmodx = [Polynomial(p) for p in Zmodx]
			mod = Polynomial([1]*(len(factors)+1))
			for p in Zmodx:
				self.append(FFE(p,mod))
