import SdNodeWritable
import json

class SubDagWritable:
    
    def __init__(self, designPoint, subdag):
        
        self.metadata = designPoint
        self.sdNodes = []
        
        for sdnode in subdag.sdnodes :
            wsn = SdNodeWritable.SdNodeWritable()
            wsn.id = sdnode.node.id
            wsn.name = sdnode.node.name
            wsn.xBar = sdnode.xBar
            wsn.xHat = sdnode.xHat
            wsn.yHat = sdnode.yHat
            wsn.yBar = sdnode.yBar
            wsn.meanProba = sdnode.meanProba
            wsn.logProbaOfScalesCondToParent = sdnode.logProbaOfScalesCondToParent
            wsn.logProbaOfScales = sdnode.logProbaOfScales
            wsn.marginScaleProbaCond = sdnode.marginScaleProbaCond
            wsn.marginProba = sdnode.marginProba
            self.sdNodes.append(wsn)
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)