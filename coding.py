import random
import math
import operator
import copy
from absalg import *

class TestChannel:
	def __init__(self, error_rate):
		self.error_rate = error_rate

	def transmit(self, bits):
		buf = []
		for bit in bits:
			assert isinstance(bit,Bit)
			if random.random()<self.error_rate:
				bit = ~bit
			buf.append(bit)
		return buf

class Code:
	def __init__(self, block_size):
		self.block_size = block_size

	def encode(self, words):
		raise NotImplementedError("Please Implement this method")

	def decode(self, bits):
		raise NotImplementedError("Please Implement this method")

	def get_rand_word(self):
		raise NotImplementedError("Please Implement this method")

class LinearBlockCode(Code):
	def __init__(self, G):
		self.G = G
		G = G.get_reduced_echelon()
		P = Matrix(G.rows, G.cols-G.rows,fill=lambda r,c:G.get(r,c+G.rows))
		I = Matrix.get_identity(P.cols).to_Zmod(G.get(0,0).p)
		self.H = (-(P.transpose())).join_with(I)	
		self.base = G.get(0,0).p
		self.words = self.base**G.rows
		Code.__init__(self,1)
		self.code_list = [self.encode([w]) for w in xrange(self.words)]

	def encode(self, words):
		bits = []
		for word in words:
			w = to_base(word, self.base)
			w = [FFE(0,self.base) for i in xrange(self.G.rows-len(w))]+w
			w = Matrix(data=[w])
			c = w*self.G
			bits = bits+c.get_row(0)
		if self.base == 2:
			bits = [Bit(i.i) for i in bits]
		return bits

	def get_word_matrix(self, w):
		w = to_base(w, self.base)
		while len(w)<self.G.rows:
			if self.base == 2:
				w = [Bit(0)]+w
			else:
				w = [FFE(0,self.base)]+w
		return Matrix(data=[w])

	def decode(self, bits):
		def get_word(w):
			return [bits[w*self.G.rows+i] for i in xrange(self.G.cols)]
		words = len(bits)/self.G.cols
		code_words = [get_word(w) for w in xrange(words)]
		words = []
		for code in code_words:
			min_dist = float("inf")
			min_index = 0
			for i, w in enumerate(self.code_list):
				dist = hamming_distance(w,code)
				if dist < min_dist:
					min_dist = dist
					min_index = i
			words.append(min_index)	
		return words

	def get_random_word(self):
		return random.randint(0,self.words-1)

	def word_iter(self):
		return xrange(self.words)

def run_test(code, channel=TestChannel(0), trials=10000):
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
	results = {
		"total errors":errors,
		"words sent":words_sent,
		"bits sent":bits_sent,
	}
	return results

def hamming_distance(s1, s2):
	assert len(s1) == len(s2)
	return sum(ch1 != ch2 for ch1, ch2 in zip(s1,s2))

def code_weight(code, zero_word, word_iter=None):
	if word_iter is None:
		word_iter = code.word_iter()
	zero = code.encode([zero_word])
	min_weight = float("inf")
	for word in word_iter:
		code_word = code.encode([word])
		weight = hamming_distance(zero, code_word)
		if weight != 0 and weight < min_weight:
			min_weight = weight
	return min_weight
