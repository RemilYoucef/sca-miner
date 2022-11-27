import Pair

class Snapshots:

    def __init__(self, snaphshotsPath, snapshotsNamesPath, dag):
        
        self.nSnapshots = 0
        self.dictSnapshots = {}
        self.dictSnapshotNames = {}
        
        file = open(snapshotsNamesPath, "r")
        for line in file.readlines() :
            elements = line.split(",", 1)
            idSnapshot = int(elements[0])
            nameSnapshot = str(elements[1][:-1])
            self.dictSnapshotNames[idSnapshot] = nameSnapshot
            
        file.close()
        self.nSnapshots = len(self.dictSnapshotNames)
        for idSnapshot in range(self.nSnapshots) :
            self.dictSnapshots[idSnapshot] = {}
        
        file = open(snaphshotsPath, "r")
        for line in file.readlines() :
            elements = line.split(",")
            idSnapshot = int(elements[0])
            idNode = int(elements[1])
            self.dictSnapshots[idSnapshot][idNode] = int(elements[2])

        file.close()



