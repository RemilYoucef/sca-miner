import Dag
import Node
import SdNode
import SubDag
import copy
import math
import MathOperations
import HierarchyMiner
import numpy as np

class SubgroupMiner :

    def __init__(self, minerSD, dictSdNodesCorresp):
        self.hierarchyMiners = []
        self.dictSdNodesCorresp = dictSdNodesCorresp
        for miner in minerSD :
            self.hierarchyMiners.append(HierarchyMiner.HierarchyMiner(miner))
        
        for hierarchyMiner in self.hierarchyMiners :
            hierarchyMiner.propagateMessages()
            hierarchyMiner.makeNodeObserved(0)
            
    def updateSdNodesValues(self, antichainIds, indicesListMiners) :
        mapSdNodes = dict()
        for nodeId in antichainIds :
            listValuesOfSD = []
            for ind in indicesListMiners : 
                sdnode = self.hierarchyMiners[ind].getSdNode(nodeId, self.dictSdNodesCorresp)
                listValuesOfSD.append(sdnode.observedValue)
            listValuesOfSD = sorted(listValuesOfSD)
            mapSdNodes[nodeId] = round(np.percentile(listValuesOfSD, 20))
            
        for ind in indicesListMiners :
            for k, sdn in enumerate(self.hierarchyMiners[ind].allSdNodes) :
                if sdn.node.id in antichainIds :
                    sdn.isObserved = True
                    sdn.updateValueMin = max(sdn.updateValueMin, mapSdNodes[sdn.node.id])
            
            self.hierarchyMiners[ind].propagateMessages()
    
    def propagateMessages(self, indicesListMiners) :
        for ind in indicesListMiners :
            self.hierarchyMiners[ind].propagateMessages()
            
    def makeNodeObserved(self, indicesListMiners, nodeId) : 
        for ind in indicesListMiners :
            self.hierarchyMiners[ind].makeNodeObserved(nodeId)
            
    def computeIcSdNodes(self, indicesListMiners, typeDL, gammaDl):
        for sdn in self.hierarchyMiners[0].allSdNodes:
            listValuesOfSD = []
            for ind in indicesListMiners : 
                sdnode = self.hierarchyMiners[ind].getSdNode(sdn.node.id, self.dictSdNodesCorresp)
                listValuesOfSD.append(sdnode.observedValue)
            listValuesOfSD = sorted(listValuesOfSD)
            
            for ind in indicesListMiners : 
                sdnode = self.hierarchyMiners[ind].getSdNode(sdn.node.id, self.dictSdNodesCorresp)
                sdnode.computeIc(self.hierarchyMiners[ind].allSdNodesMap, self.hierarchyMiners[ind].qualComputer.designPoint, listValuesOfSD, typeDL, gammaDl)

    def getNotNecMaximalAntichains(self, indicesListMiners, typeDL, gammaDl):
        
        self.computeIcSdNodes(indicesListMiners, typeDL, gammaDl)
        allNodes = [hierarchyMiner.allSdNodes.copy()[1:] for hierarchyMiner in self.hierarchyMiners]
        sd = self.getNotNecMaximalAntichain(allNodes.copy(), indicesListMiners)
        return sd

    def getNotNecMaximalAntichain(self, listRemainingSdNodes, indicesListMiners) :
        
        sd = SubDag.SubDag()
        continu = True

        while (continu) :
            if (len(listRemainingSdNodes[indicesListMiners[0]]) == 0) :
                continu = False
            else :
                appendit = True
                bestSdNode = None
                bestIndex = -1
                bestSi = sd.si
                i = 0
                while (i < len(listRemainingSdNodes[indicesListMiners[0]])) :
                    sdn = listRemainingSdNodes[indicesListMiners[0]][i]
                    if (sdn.isCoveredWithAntichain) :
                        for ind in indicesListMiners :
                            del listRemainingSdNodes[ind][i]
                    else :
                        icSdn = 0
                        newSiNotBelong = (sd.ic / (sd.dl + sdn.dl-math.log2(1-self.hierarchyMiners[0].qualComputer.designPoint.belongToAntichain)))
                        for indice in indicesListMiners :
                            icSdn += self.hierarchyMiners[indice].getSdNode(sdn.node.id, self.dictSdNodesCorresp).ic
                        newSiBelong = (sd.ic + icSdn) / (sd.dl + sdn.dl-math.log2(self.hierarchyMiners[0].qualComputer.designPoint.belongToAntichain) + math.log2(self.hierarchyMiners[0].qualComputer.designPoint.maxScaleExponent))

                        if (not sdn.isObserved and (self.hierarchyMiners[0].qualComputer.designPoint.maxPatternSize == -1 or self.hierarchyMiners[0].qualComputer.designPoint.maxPatternSize > len(sd.sdnodes))) :
                            if (bestIndex == -1 or newSiBelong > bestSi) :
                                bestSi = newSiBelong
                                bestIc = icSdn
                                bestIndex = i
                                bestSdNode = sdn
                                appendit = True

                        if (newSiNotBelong > bestSi) :
                            bestSi = newSiNotBelong
                            bestIndex = i
                            bestSdNode = sdn
                            appendit = False

                        i+=1

                if (bestIndex == -1) :
                    continu = False
                else :
                    if (appendit) :
                        sd.sdnodes.append(bestSdNode)
                        sd.ic += bestIc
                        sd.dl += (bestSdNode.dl - math.log2(self.hierarchyMiners[0].qualComputer.designPoint.belongToAntichain) + math.log2(self.hierarchyMiners[0].qualComputer.designPoint.maxScaleExponent)) 
                        sd.si = sd.ic / sd.dl

                    else :
                        sd.dl += (bestSdNode.dl-math.log2(1-self.hierarchyMiners[0].qualComputer.designPoint.belongToAntichain))
                        sd.si = sd.ic / sd.dl

                    for ind in indicesListMiners :
                        del listRemainingSdNodes[ind][bestIndex]
                    
                    for indice in indicesListMiners :
                        self.hierarchyMiners[indice].getSdNode(bestSdNode.node.id, self.dictSdNodesCorresp).updateCoverageAntiChain(self.hierarchyMiners[indice].allSdNodesMap)
                        
        return sd

    def getNotNecMaximalAntichainCopy(self, listRemainingSdNodes, indicesListMiners) :
        sd = SubDag.SubDag()
        continu = True

        while (continu) :
            if (len(listRemainingSdNodes[indicesListMiners[0]]) == 0) :
                continu = False
            else :
                appendit = True
                bestSdNode = None
                bestIndex = -1
                bestSi = sd.si
                i = 0
                while (i < len(listRemainingSdNodes[indicesListMiners[0]])) :
                    sdn = listRemainingSdNodes[indicesListMiners[0]][i]
                    if (sdn.isCoveredWithAntichain) :
                        for ind in indicesListMiners :
                            del listRemainingSdNodes[ind][i]
                    else :
                        icSdn = 0
                        if len(sd.sdnodes) == 0 :
                            newSiNotBelong = 0
                        else :
                            newSiNotBelong = sd.ic / sd.dl
                        for indice in indicesListMiners :
                            icSdn += self.hierarchyMiners[indice].getSdNode(sdn.node.id, self.dictSdNodesCorresp).ic
                        newSiBelong = (sd.ic + icSdn) / (sd.dl + sdn.dl)
                        
                        if (not sdn.isObserved and (self.hierarchyMiners[0].qualComputer.designPoint.maxPatternSize == -1 or self.hierarchyMiners[0].qualComputer.designPoint.maxPatternSize > len(sd.sdnodes))) :
                            if (bestIndex == -1 or newSiBelong > bestSi) :
                                bestSi = newSiBelong
                                bestIc = icSdn
                                bestIndex = i
                                bestSdNode = sdn
                                appendit = True
                            
                        if (newSiNotBelong > bestSi) :
                            bestSi = newSiNotBelong
                            bestIndex = i
                            bestSdNode = sdn
                            appendit = False

                        i+=1

                if (bestIndex == -1) :
                    continu = False
                else :
                    if (appendit) :
                        sd.sdnodes.append(bestSdNode)
                        sd.ic += bestIc
                        sd.dl += bestSdNode.dl 
                        sd.si = sd.ic / sd.dl

                    else :
                        sd.dl += bestSdNode.dl
                        sd.si = sd.ic / sd.dl

                    for ind in indicesListMiners :
                        del listRemainingSdNodes[ind][bestIndex]
                    
                    for indice in indicesListMiners :
                        self.hierarchyMiners[indice].getSdNode(bestSdNode.node.id, self.dictSdNodesCorresp).updateCoverageAntiChain(self.hierarchyMiners[indice].allSdNodesMap)
                        
        return sd
    
