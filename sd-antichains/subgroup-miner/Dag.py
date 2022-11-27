import Node

class Dag:
    def __init__(self, itemNamesPath, dagPath):
        
        root = None
        self.allNodes = []
        self.leaves = []
        self.nodesMap = {} 
        
        'itemNames'
        file = open(itemNamesPath, "r")
        cpt = 0

        for line in file.readlines() : 
            elements = line.split(",")
            node = Node.Node()
            node.id = int(elements[0])
            node.name = elements[1][:-1]
            node.index = cpt
            self.nodesMap[node.id] = node
            self.allNodes.append(node)
            if (cpt == 0) :
                self.root = node
            cpt += 1
        file.close()
        
        'Dag Builder'
        file = open(dagPath, "r")
        cpt = 0
        for line in file.readlines() :
            cpt += 1
            if (cpt > 1) :
                elements = line.split(",")
                parent = self.nodesMap[int(elements[0])]
                child = self.nodesMap[int(elements[1])]
                parent.directDesc.append(child)
                child.directParent = parent
        file.close ()

        for node in self.allNodes:
            if len(node.directDesc) == 0 :
                self.leaves.append(node)

        self.computeAllDesc() #'Fill AllDesc of Node'
        self.computeAllAsc()  #'Fill AllAsc of Node'
        self.setChildrenIndices()


    def computeAllDesc(self) :
        self.root.computeAllDesc(len(self.allNodes))

    def computeAllAsc(self) :
        for node in self.leaves :
            node.computeAllAsc(len(self.allNodes))

    def setChildrenIndices(self) :
        self.root.setChildrenIndices()