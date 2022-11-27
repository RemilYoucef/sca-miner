import math

class DesignPoint :
    def __init__(self, maxX):
        self.scaleBase = 2. # > 1
        self.normalizeRoot = True
        self.maxX = maxX
        self.maxScaleExponent = int(math.ceil(math.log(self.maxX,self.scaleBase)))
        self.maxX= int(math.pow(self.scaleBase, self.maxScaleExponent))
        
        self.choiceNodeChild = 0.2
        self.belongToAntichain = 1.0E-100
        self.accountForValueInDL = True
        self.minXHat = 2
        self.maxPatternSize = 5
        self.nbMaxPatterns = 10
        
        
    
    