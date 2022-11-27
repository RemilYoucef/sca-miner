import SubgroupMiner
import numpy as np
import copy
import math

class HierarchiesQF:
    
    def __init__(self, subgroupMiner, typeDL, alphaSg, betaSelectors, gammaDl):
        
        self.subgroupMiner = subgroupMiner
        self.typeDL = typeDL
        self.alphaSg = alphaSg
        self.betaSelectors = betaSelectors
        self.gammaDl = gammaDl
        self.antichains = []
        
    def calculate_constant_statistics(self, data, target):
        """ calculate_constant_statistics
            This function is called once for every execution,
            it should do any preparation that is necessary prior to an execution.
        """
        pass

    def calculate_statistics(self, subgroup, target, data, statistics = None):
        """ calculates necessary statistics
            this statistics object is passed on to the evaluate
            and optimistic_estimate functions
        """
        pass

    def evaluate(self, subgroup, target, data, statistics_or_data = None):
        """ return the quality calculated from the statistics """
        indicesListMiners = list(np.where(subgroup.covers(data))[0])
        if (len(indicesListMiners) == 0) or  (len(indicesListMiners) == 1):
            return 0
        else :
            subgroupMinerCopy = copy.deepcopy(self.subgroupMiner)
            antichain = subgroupMinerCopy.getNotNecMaximalAntichains(indicesListMiners, self.typeDL, self.gammaDl)
            antichain.si = antichain.si / (self.alphaSg * len(indicesListMiners) + self.betaSelectors * len(subgroup))
            
            antichainIds = []
            antichainNames = []
            for sdnode in antichain.sdnodes :
                antichainIds.append(sdnode.node.id)
                antichainNames.append(sdnode.node.name)
            self.antichains.append((indicesListMiners, antichainIds, antichainNames, subgroup, antichain.si))
            return antichain.si        

    def optimistic_estimate(self, subgroup, statistics=None):
        """ returns optimistic estimate
            if one is available return it otherwise infinity"""
        pass