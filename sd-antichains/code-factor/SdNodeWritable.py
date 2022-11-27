class SdNodeWritable :
    
    def __init__(self):
        self.id = None
        self.name = None
        
        self.xHat = None
        self.xBar = None
        self.yBar = None
        self.yHat = None
        
        self.meanProba = 0
        self.marginProba = 0
        self.logProbaOfScales = None
        self.logProbaOfScalesCondToParent = None 
        
        self.marginScaleProbaCond = None
            