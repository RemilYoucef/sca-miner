import DesignPoint
import numpy as np
import math
import sys
import MathOperations

class SdNode :
    def __init__(self, designPoint):
        self.binomialMaxP = 0.99
        self.node = None
        self.xHat = None# true value
        self.xBar = None# init expected value
        self.yBar = None# init log expected value
        self.yHat = None# log true value
        self.observedValue = None

        self.logProbaOfScalesCondToParent = None #factors
        self.logProbaOfScales = None # sum of factor lines

        self.marginScaleProbaCond = None
        self.marginProba = 0
        self.meanProba = None

        self.nbCallFactorFunction = 0
        self.binomialParam = None
        self.geometricParam = None
        self.temp = None

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

    def computeLogProbas(self, parentSdn, allSdNodesMap, designPoint, curIndex) :
        if (self.temp == None) :
            self.temp = np.zeros(designPoint.maxX)

        if (parentSdn != None) :
            self.binomialParam = self.xBar / parentSdn.xBar
            if (self.binomialParam > self.binomialMaxP) :
                self.binomialParam = self.binomialMaxP


        self.geometricParam = 1. / (1. + self.xBar)
        self.logProbaOfScalesCondToParent = np.zeros((designPoint.maxScaleExponent, designPoint.maxScaleExponent))
        self.meanProba = self.xBar
        self.marginScaleProbaCond = np.zeros(designPoint.maxScaleExponent)

        newIndex = curIndex + 1
        print("curIndex:" + str(newIndex))

        'we first compute probaOfScales'
        minKprim = np.arange(designPoint.maxScaleExponent)
        minKprim = designPoint.scaleBase ** minKprim
        maxKprim = designPoint.scaleBase * minKprim
        minKprim[0] = 0
        self.logProbaOfScales = MathOperations.getLogCdfIntervalGeometric(self.geometricParam, minKprim, maxKprim)
        self.marginProba = np.exp(self.logProbaOfScales[self.logProbaOfScales <= 0]).sum()

        'we second compute probaOfScalesCondToParent'
        if (parentSdn != None) :
            for kprim in range(designPoint.maxScaleExponent) :
                if (kprim == 0) :
                    minKprim = 0
                    maxKprim = designPoint.scaleBase
                else :
                    minKprim = math.pow(designPoint.scaleBase, kprim)
                    maxKprim = minKprim * designPoint.scaleBase
                
                for k in range(kprim):
                    self.logProbaOfScalesCondToParent[kprim][k] = - sys.float_info.max
                
                for k in range(kprim, designPoint.maxScaleExponent) :
                    if (parentSdn.logProbaOfScales[k] > - sys.float_info.max) :
                        if (k == 0) :
                            minK = 0
                            maxK = designPoint.scaleBase
                        else :
                            minK = math.pow(designPoint.scaleBase, k)
                            maxK = minK * designPoint.scaleBase

                        tmp = 0
                        maxLP = - sys.float_info.max
                        indexMax = 0
                        limitJ = int(minK)
                        for j in range(int(minK), int(maxK)) :
                            limitJ = j + 1
                            self.temp[j-int(minK)] = MathOperations.getLogGeometric(parentSdn.geometricParam, j)
                            self.temp[j-int(minK)] += MathOperations.getLogCdfIntervalBinomial(j,self.binomialParam, minKprim, maxKprim,designPoint)

                            if (self.temp[j-int(minK)] > maxLP) :
                                maxLP = self.temp[j-int(minK)]
                                indexMax = j-int(minK)
                        self.temp[indexMax] = self.temp[int(limitJ-minK)-1]
                        self.temp[int(limitJ-minK)-1] = maxLP
                        tmp = self.temp[int(limitJ-minK)-1]
                        
                        
                        if (tmp != -sys.float_info.max or tmp!=0) :
                            tmp2 = 0
                            for y in range(int(limitJ-minK-1)) :
                                if (self.temp[y] == -sys.float_info.max and tmp == -sys.float_info.max) :
                                    tmp2 += 1
                                else :
                                    tmp2+=math.exp(self.temp[y]-tmp)

                            tmp2 += 1 
                            tmp += math.log(tmp2)
                        self.logProbaOfScalesCondToParent[kprim][k] = tmp - parentSdn.logProbaOfScales[k]        
            self.marginScaleProbaCond = np.exp(self.logProbaOfScalesCondToParent).sum(axis = 0) 
        for child in self.node.directDesc :
            if (child in allSdNodesMap.keys()) :
                childSdn = allSdNodesMap[child]
                newIndex = childSdn.computeLogProbas(self, allSdNodesMap, designPoint, newIndex)
        return newIndex

    def copySdNode(self, elt):
        self.xBar = elt['xBar']
        self.yBar = elt['yBar']
        self.xHat = elt['xHat']
        self.yHat = elt['yHat']
        self.meanProba = elt['meanProba']
        self.marginProba = elt['marginProba']
        self.logProbaOfScales = np.array(elt['logProbaOfScales'])
        self.logProbaOfScalesCondToParent = np.array(elt['logProbaOfScalesCondToParent'])
        self.marginScaleProbaCond = np.array(elt['marginScaleProbaCond'])