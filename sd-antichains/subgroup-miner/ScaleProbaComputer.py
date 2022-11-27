import Dag
import Node
import SdNode
import SubDag

class ScaleProbaComputer :

    def __init__(self, dag, model, snapshot, qualComputer) :
        self.dag = dag
        self.model = model
        self.snapshot = snapshot 
        self.qualComputer = qualComputer
        self.allSdNodes = []
        self.allSdNodesMap = {}

    def buildAllSdNodes(self) :

        for node in self.dag.allNodes :
            if (node in self.model.supportMap.keys()) :
                sdnode = SdNode.SdNode()
                sdnode.node = node
                self.qualComputer.computeExpectedValues(sdnode, self.model)
                self.qualComputer.computeObservedValues(sdnode, self.snapshot)
                self.allSdNodes.append(sdnode)
                self.allSdNodesMap[node] = sdnode

    def computeAllProbas(self) :
        subdag = SubDag.SubDag()
        subdag.sdnodes = self.allSdNodes
        rootSdn = self.allSdNodesMap[self.dag.root]
        rootSdn.computeLogProbas(None, self.allSdNodesMap, self.qualComputer.designPoint,0)
        return subdag
