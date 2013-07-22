import random
import math
import operator
import copy
from galois import *

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
        return Matrix(self.rows, self.cols, 
            fill=lambda r,c:FFE(self.get(r,c)%base,base))

    def to_GF(self, n):
        field = GF(n)
        return Matrix(self.rows, self.cols, 
            fill=lambda r,c:field[self.get(r,c)])

    def join_with(self, other):
        assert self.rows == other.rows
        def get(r,c):
            if c<self.cols:
                return self.get(r,c)
            return other.get(r,c-self.cols)
        return Matrix(self.rows,self.cols+other.cols,fill=get)

    def submatrix(self, row, col, rows, cols):
        return Matrix(rows, cols, fill=lambda r,c:self.get(r+row, c+col))

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

class TestChannel:
    def __init__(self, error_rate):
        self.error_rate = error_rate

    def transmit(self, bits):
        buf = []
        for bit in bits:
            assert isinstance(bit,FFE)
            assert bit.p == 2
            if random.random()<self.error_rate:
                bit = bit+FFE(1,2)
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
        G = G.get_reduced_echelon()
        self.G = G
        P = Matrix(G.rows, G.cols-G.rows,
            fill=lambda r,c:G.get(r,c+G.rows)
        )
        self.base = len(G.get(0,0).belongs_to())
        I = Matrix.get_identity(P.cols).to_GF(self.base)
        self.H = (-(P.transpose())).join_with(I)    
        self.words = self.base**G.rows
        Code.__init__(self,1)
        self.code_list = [self.encode([w]) for w in xrange(self.words)]

    def encode(self, words):
        bits = []
        zero = self.G.get(0,0)
        zero = zero-zero
        for word in words:
            w = to_base(word, self.base)
            w = [zero for i in xrange(self.G.rows-len(w))]+w
            w = Matrix(data=[w])
            c = w*self.G
            bits = bits+c.get_row(0)
        return bits

    def get_word_matrix(self, w):
        w = to_base(w, self.base)
        while len(w)<self.G.rows:
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
