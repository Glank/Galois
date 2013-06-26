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

class FFE:
	"""An element of a finite field."""
	
	def __init__(self, i, p):
		self.i = int(i)
		self.p = int(p)

	def __add__(self, other):
		if isinstance(other,FFE):
			assert self.p == other.p
			return FFE((self.i+other.i)%self.p,self.p)
		else:
			return other.__radd__(self)

	def __sub__(self, other):
		if isinstance(other,FFE):
			assert self.p == other.p
			return FFE((self.i-other.i)%self.p,self.p)
		else:
			return other.__rsub__(self)

	def __mul__(self, other):
		if isinstance(other,FFE):
			assert self.p == other.p
			return FFE((self.i*other.i)%self.p,self.p)
		else:
			return other.__rmul__(self)

	def __div__(self, other):
		if isinstance(other,FFE):
			assert self.p == other.p
			return self*other.mul_inv()
		else:
			return other.__rdiv__(self)

	def mul_inv(self):
		assert self.i!=0
		u = self.i
		v = self.p
		x1 = 1
		x2 = 0
		while u!=1:
			q = v/u
			r = v-q*u
			x = x2-q*x1
			v = u
			u = r
			x2 = x1
			x1 = x
		return FFE(x1%self.p,self.p)

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
		return "%d"%self.i

	def __repr__(self):
		return "FFE(%d,%d)"%(self.i,self.p)

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
			return Matrix(self.rows, self.cols, fill=lambda r,c:Bit(self.get(r,c)%2))
		return Matrix(self.rows, self.cols, fill=lambda r,c:FFE(self.get(r,c)%base,base))

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
			row = [x+y for (x,y) in zip(self.get_row(r), other.get_row(r))]
			newData.append(row)
		return Matrix(data=newData)

	def __sub__(self, other):
		assert self.rows == other.rows
		assert self.cols == other.cols
		newData = []
		for r in xrange(self.rows):
			row = [x-y for (x,y) in zip(self.get_row(r), other.get_row(r))]
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
