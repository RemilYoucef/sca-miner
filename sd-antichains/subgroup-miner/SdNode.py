import DesignPoint
import numpy as np
import math
import sys
import MathOperations

class SdNode :
    def __init__(self, designPoint) :
        
        self.node = None
        self.xHat = None# true value
        self.xBar = None# init expected value
        self.yBar = None# init log expected value
        self.yHat = None# log true value
        self.observedValue = None

        self.logProbaOfScalesCondToParent = None #factors
        self.logProbaOfScales = None # sum of factor lines
        self.marginProba = 0
        self.currentMode = 0
        
        self.sumOfMarginals = 0
        self.logMarginals = None
        self.logMuThisToFp = None
        self.logMuFcToThisList = None
        self.logMuFpToThis = None
        self.logMuThisToFcList = None
        self.logProba = -1
        
        self.ic = 0
        self.dl = 0
        self.si = 0 
        self.isObserved = False
        self.temp = None
        
        self.isCoveredWithAntichain = False
        self.updateValueMin = 0
        
    def computeAscendentMessages(self, allSdNodesMap, designPoint) :
        if (type(self.temp) == type(None)) :
            self.temp = np.zeros(designPoint.maxScaleExponent)

        if (type(self.logMuThisToFp) == type(None)) :
            self.logMuThisToFp = np.zeros(designPoint.maxScaleExponent)

        # if this is a leaf then it is 1
        if (len(self.node.directDesc) == 0) :
            self.logMuThisToFp = np.zeros(designPoint.maxScaleExponent)

        else :
            # it is the product of muFcToThis
            firstTime = False
            if (self.logMuFcToThisList == None) :
                self.logMuFcToThisList = []
                firstTime = True

            for i in range(len(self.node.directDesc)) :
                if (self.node.directDesc[i] in allSdNodesMap.keys()) :
                    if (firstTime) :
                        muFcToThis = np.zeros(designPoint.maxScaleExponent)
                    else :
                        muFcToThis = self.logMuFcToThisList[i]

                    childSdn = allSdNodesMap[self.node.directDesc[i]]
                    childSdn.computeAscendentMessages(allSdNodesMap, designPoint)

                    for k in range(designPoint.maxScaleExponent) :
                        muFcToThis[k] = 0
                        maxVal = - sys.float_info.max
                        indexMax = 0
                        for j in range(designPoint.maxScaleExponent) :

                            self.temp[j] = childSdn.getFactorValue(j, k, False) + childSdn.logMuThisToFp[j]
                            if (self.temp[j] > maxVal) :
                                maxVal = self.temp[j]
                                indexMax = j
                        muFcToThis[k] = maxVal
                        if (maxVal != - sys.float_info.max) :
                            tmp2 = 0
                            for j in range(designPoint.maxScaleExponent) :
                                if (j != indexMax) :
                                    tmp2 += math.exp(self.temp[j] - maxVal)
                            tmp2+=1
                            muFcToThis[k] += math.log(tmp2)
                
                if (firstTime) :
                    self.logMuFcToThisList.append(muFcToThis)

            for i in range(designPoint.maxScaleExponent) :
                self.logMuThisToFp[i] = 0
                for j in range(len(self.node.directDesc)) :
                    if (self.node.directDesc[j] in allSdNodesMap.keys()) :
                        self.logMuThisToFp[i] += self.logMuFcToThisList[j][i]

                if (abs(self.logMuThisToFp[i]) == math.inf) :
                    self.logMuThisToFp[i] = - sys.float_info.max                    

    def computeDescendentMessages(self, allSdNodesMap, designPoint) :

        if (type(self.temp) == type(None)):
            self.temp = np.zeros(designPoint.maxScaleExponent)

        if (type(self.logMuFpToThis) == type(None)) :
            self.logMuFpToThis = np.zeros(designPoint.maxScaleExponent)

        if (self.node.directParent == None) :
            # this is the root
            for i in range(designPoint.maxScaleExponent) :
                self.logMuFpToThis[i] = self.getFactorValue(i, 0, True)
                if (abs(self.logMuFpToThis[i]) == math.inf) :
                    self.logMuFpToThis[i] = - sys.float_info.max
                    raise ValueError("infinity")
                    
        else :
            for i in range(designPoint.maxScaleExponent) :
                self.logMuFpToThis[i] = 0
                parent = allSdNodesMap[self.node.directParent]

                maxVal = - sys.float_info.max
                indexMax = 0

                for j in range(designPoint.maxScaleExponent) :
                    self.temp[j] = self.getFactorValue(i, j, False) + parent.logMuThisToFcList[self.node.childIndex][j]
                    if (self.temp[j] > maxVal) :
                        maxVal = self.temp[j]
                        indexMax = j

                self.logMuFpToThis[i] = maxVal

                if (maxVal != - sys.float_info.max) :
                    tmp2 = 0
                    for j in range(designPoint.maxScaleExponent) :
                        if (j != indexMax) :
                            tmp2 += math.exp(self.temp[j] - maxVal)


                    tmp2+=1
                    self.logMuFpToThis[i] += math.log(tmp2)

                if (abs(self.logMuFpToThis[i]) == math.inf) :
                    raise ValueError("infinity")

        firstTime = False
        if (self.logMuThisToFcList == None) :
            self.logMuThisToFcList = []
            firstTime = True

        for i in range(len(self.node.directDesc)) :
            muThisToFc = None
            if (self.node.directDesc[i] in allSdNodesMap.keys()) :
                if (firstTime) :
                    muThisToFc = np.zeros(designPoint.maxScaleExponent)
                else :
                    muThisToFc = self.logMuThisToFcList[i]

                for k in range(designPoint.maxScaleExponent) :
                    muThisToFc[k] = self.logMuFpToThis[k]
                    for j in range(len(self.node.directDesc)) :
                        if (self.node.directDesc[j] in allSdNodesMap.keys()) :
                            if (j != i) :
                                muThisToFc[k] += self.logMuFcToThisList[j][k]

                    if (abs(muThisToFc[k]) == math.inf) :
                        muThisToFc[k] = - sys.float_info.max

            if (firstTime) :
                self.logMuThisToFcList.append(muThisToFc)


        for i in range(len(self.node.directDesc)) :
            childSdn = allSdNodesMap[self.node.directDesc[i]]
            if (childSdn != None) :
                childSdn.computeDescendentMessages(allSdNodesMap, designPoint)


    def computeLogMarginals(self, allSdNodesMap, designPoint) :

        if (type(self.logMarginals) == type(None)) :
            self.logMarginals = np.zeros(designPoint.maxScaleExponent)

        sum = 0
        currentMode = 0
        maxVal = - sys.float_info.max
        indexMax = 0
        for i in range(designPoint.maxScaleExponent) :
            self.logMarginals[i] = self.logMuFpToThis[i]
            for j in range(len(self.node.directDesc)) :
                if (self.node.directDesc[j] in allSdNodesMap.keys()) :
                    self.logMarginals[i] += self.logMuFcToThisList[j][i]


            if (abs(self.logMarginals[i]) == math.inf) :
                self.logMarginals[i] = - sys.float_info.max

            if (self.logMarginals[i] > maxVal) :
                maxVal = self.logMarginals[i]
                indexMax = i

        currentMode = indexMax
        sum = maxVal
        tmp2 = 0
        for i in range(designPoint.maxScaleExponent) :
            if (i != indexMax) :
                tmp2 += math.exp(self.logMarginals[i] - maxVal)


        tmp2+=1
        sum += math.log(tmp2)
        if (sum > 0) :
            print(sum)
            raise ValueError()

        for i in range(designPoint.maxScaleExponent) :
            self.logMarginals[i] -= sum

        self.sumOfMarginals = 1

        
    def computeIc(self, allSdNodesMap, designPoint, listValuesOfSD, typeDL, gammaDl) :
        
        q_20 = round(np.percentile(listValuesOfSD, 20)) 
        tmp = np.sum(np.exp(self.logMarginals)[q_20:])        
        if tmp == 0 :
            self.logProba = -1.2e+10
        else :
            self.logProba = math.log(tmp)
        
        self.ic = - self.logProba / math.log(2)
        
        if typeDL == 'uniform' :
            self.dl = gammaDl * self.node.depth
        
        elif typeDL == 'log' :        
            self.dl = gammaDl * (1 + math.log(self.node.depth))
        
        elif typeDL == 'log weighted' :
            self.dl =  1 + gammaDl * math.log(self.node.depth)
        
        self.si = self.ic / self.dl
        
    
    def updateCoverageAntiChain(self, allSdNodesMap) :
        
        self.isCoveredWithAntichain=True
        continu = True 
        curN = self
        while (continu) :
            for cle, valeur in allSdNodesMap.items():
                if valeur.node.id == curN.node.id :
                    curN = valeur
            if (curN != None and not curN.isCoveredWithAntichain) :
                curN.isCoveredWithAntichain = True

            else :
                continu=False

        for nd in self.node.allDesc :
            if (nd in allSdNodesMap.keys()) :
                allSdNodesMap[nd].isCoveredWithAntichain=True
        
        for nd in self.node.allAsc :
            if (nd in allSdNodesMap.keys()) :
                allSdNodesMap[nd].isCoveredWithAntichain=True
     
    
    def getFactorValue(self, value, parentValue, isRoot) :
        
        if self.isObserved :
            
            tmpRoot = np.exp(self.logProbaOfScales)
            tmpRoot[:self.updateValueMin] = tmpRoot[:self.updateValueMin] * 0.2 / tmpRoot[:self.updateValueMin].sum()
            if tmpRoot[self.updateValueMin:].sum() > 0 :
                tmpRoot[self.updateValueMin:] = tmpRoot[self.updateValueMin:] * 0.8 / tmpRoot[self.updateValueMin:].sum()
            else :
                for i in range(self.updateValueMin, tmpRoot.size):
                    tmpRoot[i] = 0.8 / (tmpRoot.size - self.updateValueMin)
            tmpRoot = np.array([math.log(v) if v > 0 else - sys.float_info.max for v in tmpRoot])   

            tmp = np.exp(self.logProbaOfScalesCondToParent[:, parentValue])
            tmp[:self.updateValueMin] = tmp[:self.updateValueMin] * 0.2 / tmp[:self.updateValueMin].sum()
            if tmp[self.updateValueMin:].sum() > 0 :
                tmp[self.updateValueMin:] = tmp[self.updateValueMin:] * 0.8 / tmp[self.updateValueMin:].sum()
            else :
                for i in range(self.updateValueMin, tmp.size):
                    tmp[i] = 0.8 / (tmp.size - self.updateValueMin)
            tmp = np.array([math.log(v) if v > 0 else - sys.float_info.max for v in tmp])    
                
            if isRoot :
                return tmpRoot[value] 
            else:
                return tmp[value]

        if (isRoot) :
            return self.logProbaOfScales[value]
        else :
            return self.logProbaOfScalesCondToParent[value][parentValue]     

 
    def copy(self) :
        sdn = SdNode.SdNode()
        sdn.self.node = self.node
        sdn.xHat = self.xHat
        sdn.xBar = self.xBar
        sdn.yBar = self.yBar
        sdn.yHat = self.yHat
        sdn.observedValue = self.observedValue
        sdn.marginProba = self.marginProba
        sdn.currentMode = self.currentMode
        sdn.sumOfMarginals = self.sumOfMarginals
        sdn.logMarginals = np.copy(self.logMarginals)
        sdn.logProba = self.logProba
        sdn.ic = self.ic
        sdn.dl = self.dl
        sdn.si = self.si
        sdn.isObserved = self.isObserved
        return sdn

