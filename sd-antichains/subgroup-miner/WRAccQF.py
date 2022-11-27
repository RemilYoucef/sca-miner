import numpy as np
import copy
import math

class WRAccQF:
    
    def __init__(self, dict_nodes, maxPatternSize):
        
        self.dict_nodes = dict_nodes
        self.patterns = []
        self.maxPatternSize = maxPatternSize
        
    def calculate_constant_statistics(self, data, target):
        """ calculate_constant_statistics
            This function is called once for every execution,
            it should do any preparation that is necessary prior to an execution.
        """
        pass

    def calculate_statistics(self, subgroup, target, data, statistics=None):
        """ calculates necessary statistics
            this statistics object is passed on to the evaluate
            and optimistic_estimate functions
        """
        pass

    def evaluate(self, subgroup, target, data, statistics_or_data=None):
        """ return the quality calculated from the statistics """
        indiceListSnapshots = list(np.where(subgroup.covers(data))[0])
        if (len(indiceListSnapshots) == 0) or (len(indiceListSnapshots) == 1):
            return 0
        else :
            listNodes = list(self.dict_nodes.items())[1:]
            pattern, quality = self.getBestPattern_v2(listNodes, indiceListSnapshots)
            
            patternIds = []
            patternNames = []
            for node in pattern :
                patternIds.append(node['id'])
                patternNames.append(node['name'])
            self.patterns.append((indiceListSnapshots, patternIds, patternNames, subgroup, quality))
            return quality * math.sqrt(len(indiceListSnapshots))        

    def getBestPattern_v1(self, listNodes, indiceListSnapshots):
    
        quality = 0
        pattern = []
        
        while (len(pattern) < self.maxPatternSize) : 
            best_node = -1
            best_quality = 0
            i = 0
            while (i < len(listNodes)) :
                quality_node  = (np.mean(np.array(listNodes[i][1]['xHats'])[indiceListSnapshots])) - listNodes[i][1]['xBar']
                if quality_node > best_quality :
                    best_quality = quality_node
                    best_node = i
                i += 1
            
            quality += best_quality
            node = {}
            node['id'] = listNodes[best_node][1]['id']
            node['name'] = listNodes[best_node][1]['name']
            pattern.append(node)
            del listNodes[best_node]
            
        return pattern, quality          

    def getBestPattern_v2(self, listNodes, indiceListSnapshots):
        continu = True
        quality = 0
        pattern = []

        while (continu) :
            appendit = False
            bestNode = -1
            bestQuality = quality
            i = 0
            while (i < len(listNodes)) :
                qualityNode = (np.mean(np.array(listNodes[i][1]['xHats'])[indiceListSnapshots])) - listNodes[i][1]['xBar']
                newQuality = (math.sqrt(len(pattern)) * quality + qualityNode) / math.sqrt(len(pattern) + 1)
                if newQuality > bestQuality :
                    bestQuality = newQuality
                    bestNode = i
                    appendit = True
                i += 1

            if appendit :
                node = {}
                node['id'] = listNodes[bestNode][1]['id']
                node['name'] = listNodes[bestNode][1]['name']
                pattern.append(node)
                quality = bestQuality
                del listNodes[bestNode]

            else :
                continu = False

            if len(pattern) == self.maxPatternSize :
                continu = False

        return pattern, quality

    
    def optimistic_estimate(self, subgroup, statistics=None):
        """ returns optimistic estimate
            if one is available return it otherwise infinity"""
        pass