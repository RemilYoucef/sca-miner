import pysubgroup as ps
import numpy as np
import copy
import SdNode

class Target:


    def __init__(self, subgroupMiner, typeDL, gammaDl):
        self.target_variable = "indiceListSnapshots"
        self.subgroupMiner = subgroupMiner
        self.typeDL = typeDL
        self.gammaDl = gammaDl
        
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
        
        subgroupMinerCopy = copy.deepcopy(self.subgroupMiner)
        antichain = subgroupMinerCopy.getNotNecMaximalAntichains(list(np.where(cover_arr)[0]), self.typeDL, self.gammaDl)
        antichainIds = []
        antichainNames = []
        for sdnode in antichain.sdnodes :
            antichainIds.append(sdnode.node.id)
            antichainNames.append(sdnode.node.name)
        
        statistics["patternIds"] = antichainIds
        statistics["patternNames"] = antichainNames
        
        return statistics
