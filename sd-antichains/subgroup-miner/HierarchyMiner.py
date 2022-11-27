import Dag
import Node
import SdNode
import SubDag
import copy
import math
import MathOperations

class HierarchyMiner :

    def __init__(self, miner) :
        
        self.dag = miner.dag
        self.model = miner.model
        self.snapshot = miner.snapshot
        self.allSdNodes = miner.allSdNodes
        self.allSdNodesMap = miner.allSdNodesMap
        self.qualComputer = miner.qualComputer


    def propagateMessages(self) :

        rootSdn = self.allSdNodesMap[self.dag.root]
        rootSdn.computeAscendentMessages(self.allSdNodesMap, self.qualComputer.designPoint)
        rootSdn.computeDescendentMessages(self.allSdNodesMap, self.qualComputer.designPoint)
        for sdn in self.allSdNodes :
            sdn.computeLogMarginals(self.allSdNodesMap, self.qualComputer.designPoint)


    def makeNodeObserved(self, nodeId) :
        node = self.dag.nodesMap[nodeId]
        sdn = self.allSdNodesMap[node]
        sdn.isObserved = True
        
    def getSdNode(self, idNode, dictSdNodesCorresp):
        return self.allSdNodes[dictSdNodesCorresp[idNode]]
