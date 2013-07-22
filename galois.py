import math
import operator
import copy

def to_base(number, base):
    assert number>=0
    assert base>1
    field = GF(base)
    ret = []
    i = 0
    while number > 0:
        digit = number%base
        ret = [field[digit]]+ret
        number/=base
    if len(ret) == 0:
        ret = [field[0]]
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
def phi(n):
    factors = set(factor(n))
    prod = n
    for f in factors:
        prod = prod-prod/f
    return prod

def addition(a,b):
    return a+b
def multiplication(a,b):
    return a*b
def default_format(elem, field):
    return str(field.index(elem))
def str_format(elem, field):
    return str(elem)
def repr_format(elem, field):
    return repr(elem)

def get_latex_table(field, operation, formatting=default_format):
    latex = "\\begin{tabular}{c|"+"c"*len(field)+"}\n"
    latex+= "? & " + " & ".join([formatting(e,field) for e in field])
    latex+= "\\\\\n\\hline\n"
    rows = []
    for a in field:
        rows.append([])
        for b in field:
            rows[-1].append(operation(a,b))
    rows = [[field[i]]+row for i,row in enumerate(rows)]
    rows = [[formatting(e,field) for e in row] for row in rows]
    rows = [" & ".join(row) for row in rows]
    latex+= "\\\\\n".join(rows)
    latex+= "\n\\end{tabular}"
    return latex

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
    
    def __init__(self, i, p, field=None, mulinv=None, parent=None):
        self.i = i
        self.p = p
        self.mulinv = mulinv
        self.field = field #the field which contains i
        self.parent = parent #such as GF(8)

    def belongs_to(self):
        if self.parent is not None:
            return self.parent
        else:
            return GF(self.p)

    def __add__(self, other):
        if isinstance(other,FFE):
            assert self.p == other.p
            return FFE((self.i+other.i)%self.p,self.p,field=self.field,parent=self.parent)
        else:
            return other.__radd__(self)

    def __sub__(self, other):
        if isinstance(other,FFE):
            assert self.p == other.p
            return FFE((self.i-other.i)%self.p,self.p,field=self.field,parent=self.parent)
        else:
            return other.__rsub__(self)

    def __mul__(self, other):
        if isinstance(other,FFE):
            assert self.p == other.p
            return FFE((self.i*other.i)%self.p,self.p,field=self.field,parent=self.parent)
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
        if self.field is None and self.parent is not None:
            one = FFE(self.p/self.p,self.p)
            for e in self.parent:
                if e*self==one:
                    self.mulinv = e
                    e.mulinv = self
                    return e
        if self.field is not None and self.mulinv is None:
            zero = self.i-self.i
            one = self.p/self.p
            for e in self.field:
                if e!=zero and (e*self.i)%self.p==one:
                    self.mulinv = FFE(e,self.p,
                        field=self.field,mulinv=self,
                        parent=self.parent
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
            q = v//u
            r = v-q*u
            x = x2-q*x1
            v = u
            u = r
            x2 = x1
            x1 = x
        self.mulinv = FFE(x1%self.p,self.p,mulinv=self,parent=self.parent)
        return self.mulinv

    def __pow__(self, i):
        return self.__smart_pow__(i)[0]

    def __smart_pow__(self, i, temp=None):
        assert i>=1
        if temp is None:
            temp = {1:copy.deepcopy(self)}
        if i in temp:
           return temp[i], temp
        else:
            half = i//2
            half_ = half+i%2
            left, temp = self.__smart_pow__(half, temp=temp)
            temp[half]=left
            right, temp = self.__smart_pow__(half_, temp=temp) 
            temp[half_]=right
            return left*right, temp

    def __ord__(self):
        one = self/self
        i = 1
        result, temp = self.__smart_pow__(i)
        while result != one:
            i+=1
            result, temp = self.__smart_pow__(i,temp)
        return i
    
    def __neg__(self):
        return FFE((self.p-self.i)%self.p,self.p,field=self.field,parent=self.parent)

    def __eq__(self, other):
        assert self.p == other.p
        return self.i == other.i

    def __ne__(self, other):
        assert self.p == other.p
        return self.i != other.i

    def __str__(self):
        if self.parent is not None and isinstance(self.parent,GF):
            return "GF(%d)[%d]"%(len(self.parent),self.parent.index(self))
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

backup_ord = ord
def ord(obj):
    if hasattr(obj, '__ord__'):
        return obj.__ord__()
    else:
        return backup_ord(obj)

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
        return Polynomial([FFE(c%mod,mod) for c in coefficients])

    def to_GF(self, n):
        field = GF(n)
        coefficients = self.coefficients
        return Polynomial([field[c] for c in coefficients])

    def to_latex(self):
        zero = self-self
        if self==zero:
            return "0"
        coefs = [str(c) for c in self.coefficients]
        latex = ""
        for i,c in reversed(list(enumerate(coefs))):
            if c!="0":
                if latex:
                    latex+="+"
                if i==0:
                    latex+=c
                elif i==1:
                    latex+=(c if c!="1" else "")+"x"
                else:
                    latex+=(c if c!="1" else "")+"x^{%d}"%i
        return latex

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
        return self.__smart_pow__(i)[0]

    def __smart_pow__(self, i, temp=None):
        assert i>=1
        if temp is None:
            temp = {1:copy.deepcopy(self)}
        if i in temp:
           return temp[i], temp
        else:
            half = i//2
            half_ = half+i%2
            left, temp = self.__smart_pow__(half, temp=temp)
            temp[half]=left
            right, temp = self.__smart_pow__(half_, temp=temp) 
            temp[half_]=right
            return left*right, temp

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

class Zmod(list):
    def __init__(self, p):
        list.__init__(self)
        self.n = p
        for i in xrange(p):
            self.append(FFE(i,p))

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

def is_reducable(poly, divisors):
    zero = poly-poly
    for m in divisors:
        if m.deg()>0 and poly%m==zero:
            return True,m
    return False

class GF(Zmod):
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
            Zmodx = [Polynomial(list(reversed(x))) for x in Zmodx]
            i = p**len(factors)
            mod = Polynomial(list(reversed(to_base(i, p))))
            while is_reducable(mod, Zmodx):
                i+=1
                mod = Polynomial(list(reversed(to_base(i,p))))
                assert mod.deg() == len(factors)
            for i,p in enumerate(Zmodx):
                self.append(FFE(p,mod,parent=self))
