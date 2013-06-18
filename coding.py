import random
import math
import operator
import copy

class TestChannel:
	def __init__(self, error_rate):
		self.error_rate = error_rate

	def transmit(self, bits):
		buf = []
		for bit in bits:
			assert isinstance(obj,Bit)
			if random.random()<self.error_rate:
				bit = ~bit
			buf.append(bit)
		return buf

class Code:
	def __init__(self, words, block_size):
		self.words = words
		self.block_size = block_size

	def encode(self, words):
		raise NotImplementedError("Please Implement this method")

	def decode(self, bits):
		raise NotImplementedError("Please Implement this method")

	def get_rand_word(self):
		return random.choice(words)

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
			return FFE((self.i/other.i)%self.p,self.p)
		else:
			return other.__rdiv__(self)

	def __pow__(self, other):
		return FFE((self.i**int(other))%self.p,self.p)
	
	def __neg__(self):
		return FFE(self.p-self.i,self.p)

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
		return __not__(self)

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
					row = [fill() for c in xrange(cols)]
				else:
					row = [fill for c in xrange(cols)]
				self.data.append(row)

	def get(self,r,c):
		return self.data[r][c]

	def set(self,r,c,value):
		self.data[r][c] = value

	def get_row(self,r):
		return self.data[r]

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
		rows = ["\t".join([str(value) for value in row]) for row in self.data]
		return "\n".join(rows)

def approximate_rates(code, channel=TestChannel(0), trials=10000):
	errors = 0.0
	words_sent = 0.0
	bits_sent = 0.0
	for i in xrange(trials):
		w_in = [code.get_random_word() for i in xrange(code.block_size)]
		b_in = code.encode(w_in)
		b_out = channel.transmit(b_in)
		w_out = code.decode(b_out)
		for j in xrange(len(w_in)):
			if w_in[j] != w_out[j]:
				errors+= 1
		words_sent+= len(w_in)
		bits_sent+= len(b_in)
	rates = {
		"encoding":words_sent/bits_sent,
		"transmission":(words_sent-errors)/bits_sent,
		"error":errors/words_sent,
	}
	return rates

def hamming_distance(s1, s2):
	assert len(s1) == len(s2)
	return sum(ch1 != ch2 for ch1, ch2 in zip(s1,s2))
