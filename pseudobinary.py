import math
import subprocess
import dimod

def popcount(x):
    return bin(x).count("1")
    
def bitpos(x):
    return sorted([pos+1 for pos, bit in enumerate(bin(x)[:1:-1]) if bit=='1'])

class PBP(object):
    def __init__(self, var=0, coeff=1):
        self.d = dict()
        self.d[1<<(var-1) if var>0 else 0] = coeff

    def __mul__(self, other):
        x = PBP()
        x.d.clear()
        for vars1, coeff1 in self.d.items():
            for vars2, coeff2 in other.d.items():
                p = vars1|vars2
                x.d[p] = x.d.get(p,0) + coeff1*coeff2 
        return x
    
    def __add__(self, other):
        x = PBP()
        x.d = dict(self.d)
        for vars, coeff in other.d.items():
            x.d[vars] = x.d.get(vars,0) + coeff
        return x

    def __eq__(self, other):
        return str(self) == str(other)
        
    def __str__(self):
        if(len(self.d) == 0): return '0'
        
        keys = sorted(self.d.keys(), key=lambda x: (popcount(x),x))
        s = ''
        first = True
        for vars in keys:
            coeff = self.d[vars]
            if not first: s+='+'
            first = False
            
            if coeff!=1 or vars == 0: s += str(coeff) 
            i = 1
            while vars > 0:
                if vars&1: s += 'x%d' % i
                i += 1
                vars //= 2
        return s
    
    def trim(self, threshold=0):
        self.d = {k:v for k,v in self.d.items() if abs(v) > threshold}
        
    def toQuadratic(self):
        #serialize
        txt = ''
        for k,v in self.d.items():
            bit = 0
            bits = list()
            while k>0:
                if k%2: bits.append(bit)
                bit += 1
                k >>= 1
            txt += "\n%d" % len(bits)
            for bit in bits: txt += " %d" % bit
            txt += " %d" % v
        
        #process
        p = subprocess.run(['elc.exe'], input=txt.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if p.returncode != 0:
            raise ValueError(p.stderr.decode().strip())
        out = p.stdout.decode()
        lines = out.strip().split('\r\n')
        
        #deserialize
        f = PBP(0,0)
        for line in lines:
            tokens = line.strip().split(' ')
            
            n = int(tokens[0])
            term = PBP()
            for i in range(n):
                term *= PBP(int(tokens[i+1])+1)
                
            f += term * PBP(0, float(tokens[n+1]))
            
        f.trim()    
        return f
        
    def degree(self):
        return max([popcount(x) for x in self.d])
    
    def varmask(self):
        vs = 0
        for x in self.d: vs |= x
        return vs
        
    def varcount(self):
        return popcount(self.varmask())
        
    def variables(self):
        return bitpos(self.varmask())
        
    def hasvar(self, var):
        return (self.varmask() & (1<<(var-1))) > 0
        
    def toBQM(self):
        if self.degree() > 2: raise ValueError("Degree of polynomial is greater than 2.")
        lin = dict()
        quad = dict()
        const = 0
        
        for v,coeff in self.d.items():
            varlist = bitpos(v)
            if len(varlist) == 0: const = coeff
            elif len(varlist) == 1: lin[varlist[0]] = coeff
            else: quad[tuple(varlist)] = coeff
            
        return dimod.BinaryQuadraticModel(lin, quad, const, dimod.BINARY)

    def substitute(self, var, exp):
        
        if var<1: raise ValueError("Invalid variable to substitute")
        vb = 1<<(var-1)
        
        result = PBP(0,0)
        for v, c in self.d.items():
            if v&vb:
                x = PBP(0,0)
                x.d[v&~vb]=c
                result += x*exp
            else:
                x = PBP(0,0)
                x.d[v] = c
                result += x
               
        result.trim()
        return result
        
    def solvefor(self, var):
        if self.degree() > 1: raise ValueError("Can only solve degree one polynomials")
        if not self.hasvar(var): raise ValueError("Polynomial does not contain variable")
        
        target = 1<<(var-1)
        result = PBP(0,0)
        for v,c in self.d.items():
            if v == target:
                divisor = c
            else:
                result += PBP(v,-c)
                
        if divisor != 1:
            for v,c in result.d.items(): result.d[v] /= divisor
        
        return result
        