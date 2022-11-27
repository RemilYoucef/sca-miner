import pysubgroup as ps
import numpy as np
import copy
import math 

class TargetWRAcc:


    def __init__(self, dict_nodes, maxPatternSize):
        self.target_variable = "indiceListSnapshots"
        self.dict_nodes = dict_nodes
        self.maxPatternSize = maxPatternSize
        
    def __repr__(self):
        return "T: " + str(self.target_variable)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __lt__(self, other):
        return str(self) < str(other)

    def get_attributes(self):
        return [self.target_variable]

    def get_base_statistics(self, subgroup, data):
        cover_arr, size_sg = ps.get_cover_array_and_size(subgroup, len(data), data)
        all_target_values = data[self.target_variable]
        sg_target_values = all_target_values[cover_arr]
        instances_dataset = len(data)
        instances_subgroup = size_sg
        mean_sg = np.mean(sg_target_values)
        mean_dataset = np.mean(all_target_values)
        return (instances_dataset, mean_dataset, instances_subgroup, mean_sg)

    def calculate_statistics(self, subgroup, data, cached_statistics=None):
        statistics = {}
        
        cover_arr, _ = ps.get_cover_array_and_size(subgroup, len(data), data)
        statistics["indiceListSnapshots"] = list(np.where(cover_arr)[0])
        statistics['lenSubgroup'] = len(list(np.where(cover_arr)[0]))
        listNodes = list(self.dict_nodes.items())[1:]
        pattern, quality = self.getBestPattern_v2(listNodes, list(np.where(cover_arr)[0]))

        patternIds = []
        patternNames = []
        for node in pattern :
            patternIds.append(node['id'])
            patternNames.append(node['name'])
        
        statistics["patternIds"] = patternIds
        statistics["patternNames"] = patternNames
        
        return statistics
    
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