import Pair

class Model:
    def __init__(self, supportPath, dag, name):
        self.name = name
        self.supportList = [] #'list of pairs(node, value)
        self.supportMap = {} #'node -> (node, value)'
        self.dag = dag
        self.overalNbNodesInDag = len(dag.allNodes)
        
        file = open(supportPath, "r")
        for line in file.readlines() :
            elements = line.split(",")
            node = dag.nodesMap[int(elements[0])]
            pair = Pair.Pair(node, float(elements[1]))
            self.supportList.append(pair)
            self.supportMap[node] = pair
            
        file.close()

