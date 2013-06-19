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

class LinearBlockCode(Code):
	def __init__(self, G):
		self.G = G
		words = (i for i in xrange(G.get(0,0).p**G.rows))
		Code.__init__(self,words,G.rows)

	def __encode__(self, words):
		for word in words:
			pass ##TODO

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
