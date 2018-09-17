from pseudobinary import PBP
import dimod

class TestClass(object):
    def test_substitute(self):
        x = PBP() + PBP(1,2) + PBP(2,4) + PBP(2,1)*PBP(3,3)
        y = PBP(0,5) + PBP(4,2)
        z = PBP(0,21) + PBP(1,2) + PBP(3,15) + PBP(4,8) + PBP(3,6)*PBP(4)
        assert z == x.substitute(2,y)
        
    def test_str(self):
        x = PBP() + PBP(100) + PBP(3) + PBP(1)*PBP(2)*PBP(3) + PBP(1)*PBP(2)
        assert str(x) == '1+x3+x100+x1x2+x1x2x3'
        
    def test_varcount(self):
        x = PBP() + PBP(1) + PBP(4) + PBP(1)*PBP(4) + PBP(1)*PBP(4)*PBP(9)
        assert x.varcount() == 3
        
    def test_variables(self):
        x = PBP() + PBP(1) + PBP(4) + PBP(1)*PBP(4) + PBP(1)*PBP(4)*PBP(9)
        assert x.variables() == [1,4,9]
        
    def test_solvefor(self):
        x = PBP(0,-1) + PBP(13) + PBP(14)
        y = PBP() + PBP(14,-1)
        z = x.solvefor(13)
        print(z)
        print(y)
        assert  z == y
        
    def test_toquadratic(self):
        x = PBP(1,-1) + PBP(2, -1) + PBP(3, -1) + PBP(1, 2)*PBP(2) + PBP(1, 2)*PBP(3) + PBP(2, 2)*PBP(3) + PBP(1, 6)*PBP(2)*PBP(3)
        y = PBP(1,-1.) + PBP(2,-1.) + PBP(1,8.)*PBP(2) + PBP(3,-1.) + PBP(1,8.)*PBP(3) + PBP(2,8.)*PBP(3) + PBP(4,6.) + PBP(1,-6.)*PBP(4) + PBP(2,-6.)*PBP(4) + PBP(3,-6.)*PBP(4)
        print(x.toQuadratic())
        print(y)
        assert y == x.toQuadratic()
        
    def test_tobqm(self):
        x = PBP(1,-1.) + PBP(2,-1.) + PBP(1,8.)*PBP(2) + PBP(3,-1.) + PBP(1,8.)*PBP(3) + PBP(2,8.)*PBP(3) + PBP(4,6.) + PBP(1,-6.)*PBP(4) + PBP(2,-6.)*PBP(4) + PBP(3,-6.)*PBP(4)
        lin = {4: 6.0, 1: -1.0, 2: -1.0, 3: -1.0}
        quad = {(1, 4): -6.0, (2, 4): -6.0, (3, 4): -6.0, (1, 2): 8.0, (1, 3): 8.0, (2, 3): 8.0}
        y = dimod.BinaryQuadraticModel(lin, quad, 0, dimod.BINARY)
        assert x.toBQM() == y

    def test_degree1(self):
        x = PBP(0,0)
        x.trim()
        assert x.degree() == 0
        
    def test_degree2(self):
        x = PBP(15)*PBP(2)
        x.trim()
        assert x.degree() == 2
            
    def test_iszero(self):
        x = PBP(0,0)
        assert x.iszero()
        x.d.clear()
        assert x.iszero()
        
    def test_const(self):
        x = PBP(0,3)
        assert x.const() == 3
        x.d.clear()
        assert x.const() == 0
        
    def test_coeff(self):
        x = PBP(5,3)
        assert x.coeff(5) == 3
        x.d.clear()
        assert x.coeff(4) == 0