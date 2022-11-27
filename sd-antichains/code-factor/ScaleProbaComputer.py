import Dag
import Node
import SdNode
import SubDag

class ScaleProbaComputer :

    def __init__(self, dag, model, qualComputer) :
        self.dag = dag
        self.model = model
        self.snapshot = None
        self.qualComputer = qualComputer
        self.allSdNodes = []
        self.allSdNodesMap = {}

    def buildAllSdNodesWithExpectedValues(self) :

        for node in self.dag.allNodes :
            if (node in self.model.supportMap.keys()) :
                sdnode = SdNode.SdNode(self.qualComputer.designPoint)
                sdnode.node = node
                self.qualComputer.computeExpectedValues(sdnode, self.model)
                self.allSdNodes.append(sdnode)
                self.allSdNodesMap[node] = sdnode
    
    def fillSdNodesWithObservedValues(self, snapshot):
        self.snapshot = snapshot
        for node in self.dag.allNodes :
            self.qualComputer.computeObservedValues(self.allSdNodesMap[node], snapshot)
    

    def computeAllProbas(self) :
        subdag = SubDag.SubDag()
        subdag.sdnodes = self.allSdNodes
        rootSdn = self.allSdNodesMap[self.dag.root]
        rootSdn.computeLogProbas(None, self.allSdNodesMap, self.qualComputer.designPoint,0)
        return subdag

    def rebuildAllSdNodes(self, listSdNodes) :
        for node in self.dag.allNodes :
            if (node in self.model.supportMap.keys() ) :
                sdnode = SdNode.SdNode(self.qualComputer.designPoint)
                sdnode.node = node
                
                for elt in listSdNodes :
                    if int(elt['id']) == node.id :
                        break
                sdnode.copySdNode(elt)
                self.allSdNodes.append(sdnode)
                self.allSdNodesMap[node] =  sdnode