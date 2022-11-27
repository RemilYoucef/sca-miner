class Node :
    def __init__(self):
        self.index = None
        self.id = None
        self.name = None
        self.directDesc = []
        self.allDesc = None
        self.allAsc = None
        self.directParent = None
        self.childIndex = -1
        self.depth = -1
    
    def updateDepth(self, value):
        self.depth = value
        for node in self.directDesc :
            node.updateDepth(value + 1)
    
    def computeAllDesc(self, overallSize):
        if (self.allDesc != None) :
            return self.allDesc
        self.allDesc = []
        for node in self.directDesc :
            self.allDesc.append(node)
            self.allDesc += node.computeAllDesc(overallSize)
        return self.allDesc

    def computeAllAsc(self, overallSize):
        if (self.allAsc!=None) :
            return self.allAsc
        self.allAsc=[]
        if (self.directParent!=None) :
            self.allAsc.append(self.directParent)
            self.allAsc += self.directParent.computeAllAsc(overallSize)
        return self.allAsc


    def setChildrenIndices(self) :
        for i in range(len(self.directDesc)) :
            self.directDesc[i].childIndex = i

        for i in range(len(self.directDesc)):
            self.directDesc[i].setChildrenIndices()
    
    def getName(self):
        return self.name
        

        
    