from pseudobinary import PBP

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
        x = PBP(0,-1) + PBP(1) + PBP(2)
        y = PBP() + PBP(2,-1)
        assert x.solvefor(1) == y