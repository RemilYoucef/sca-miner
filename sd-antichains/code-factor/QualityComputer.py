import Dag
import Node
import Pair
import SdNode
import math

import DesignPoint
import MathOperations

class QualityComputer :

    def __init__(self,designPoint) :
        self.designPoint = designPoint


    def computeObservedValues(self, sdNode, snapshot) :
        
        sdNode.xHat = snapshot[sdNode.node.id] + 1
        sdNode.yHat = MathOperations.logBase(self.designPoint.scaleBase, sdNode.xHat)
        sdNode.observedValue = int(math.floor(sdNode.yHat))

    def computeExpectedValues(self, sdNode, model) :

        sdNode.xBar = model.supportMap[sdNode.node].second + 1
        if (sdNode.xBar <= 1) :
            sdNode.xBar = 1
            gV = sdNode.xBar
            if (sdNode.node in model.supportMap.keys()) :
                pair = model.supportMap[sdNode.node]
                pair.second = gV
            else :
                pair = Pair.Pair(None, 0.)
                pair.first = sdNode.node
                pair.second = gV
                model.supportMap[pair.first] = pair
                model.supportList.append(pair)

        sdNode.yBar= MathOperations.logBase(self.designPoint.scaleBase, sdNode.xBar)
