import Package
from treelib import Node, Tree
import numpy as np
import pandas as pd
import math


def createTree(list_classes) :
    cpt = 1 
    list_packages = []
    for classe in list(list_classes):
        list_packages.append(Package.Package(classe, [], cpt))
        cpt += 1 
    
    intermediate_list_packages = []
    root_packages = []
    stop = False 
    while list_packages :
        package = list_packages.pop()
        if '.' in package.namePackage :
            packageParentName = package.namePackage.rsplit('.', 1)[0]
            if grandParent(packageParentName, list_packages) : 
                list_packages.insert(0, package)
            else :
                subPackages, indexes = searchSubPackages(packageParentName, list_packages)
                list_packages = np.delete(list_packages, indexes).tolist()
                list_packages.insert(0, Package.Package(packageParentName, [package] + subPackages, cpt))
                cpt += 1
        else :
            root_packages.append(package)
    
    tree = Package.Package('root', root_packages, 0)        
    return tree

def successor(packageName, packageParentName):
    packageParentName = packageParentName + '.'
    if len(packageParentName) < len(packageName) :
        return packageName[:len(packageParentName)] == packageParentName
    else :
        return False

def grandParent(packageParentName, list_packages):
    for package in list_packages :
        if successor(package.namePackage, packageParentName) & (len(packageParentName.split('.')) + 1 < len(package.namePackage.split('.'))) :
            return True
    return False

def searchSubPackages(packageParentName, list_packages):
    subPackages = []
    indexes = []
    for i in range(len(list_packages)) :
        if successor(list_packages[i].namePackage, packageParentName):
            subPackages.append(list_packages[i])
            indexes.append(i)
    return subPackages, indexes

def printTreeItems(tree) :
    print(str(tree.idPackage) + ',' + tree.namePackage)
    if tree.subPackages :
        for subPackage in tree.subPackages :
            printTreeItems(subPackage)

def printTreeDag(tree) :
    if tree.subPackages :
        for subPackage in tree.subPackages :
            print(str(tree.idPackage) + ',' + str(subPackage.idPackage))
            printTreeDag(subPackage)
            
def exportToText(tree, fileDAG, fileItems):
    fileItems.write(str(tree.idPackage) + ',' + tree.namePackage + '\n')
    if tree.subPackages :
        for subPackage in tree.subPackages :
            fileDAG.write(str(tree.idPackage) + ',' + str(subPackage.idPackage) + '\n')
            exportToText(subPackage, fileDAG, fileItems)
            
def createGraphTree(tree, treeVis) :
    if tree.namePackage == 'root' :
        treeVis = Tree()
        treeVis.create_node('Root' + ' : ' + '(' + str(tree.idPackage) + ')' + ' : ' + str(tree.value),'root')
    if tree.subPackages :
        for subPackage in tree.subPackages :
            treeVis.create_node(subPackage.namePackage + ' : ' + '(' + str(subPackage.idPackage) + ')' + ' : ' + str(subPackage.value), subPackage.namePackage, parent=tree.namePackage)
            createGraphTree(subPackage, treeVis)
    return treeVis

def supportAll(tree, df, file) :
    if tree.subPackages :
        s = 0
        for subPackage in tree.subPackages :
            s += supportAll(subPackage, df, file)
        tree.value = s
        file.write(str(tree.idPackage) + "," + str(s) + '\n')
        return s
    else :
        tree.value = round(df[tree.namePackage][df[tree.namePackage] > 0].mean())
        file.write(str(tree.idPackage) + "," + str(round(df[tree.namePackage][df[tree.namePackage] > 0].mean())) + '\n')
        return round(df[tree.namePackage][df[tree.namePackage] > 0].mean())
    
def supportAllZeros(tree, df, file) :
    if tree.subPackages :
        s = 0
        for subPackage in tree.subPackages :
            s += supportAllZeros(subPackage, df, file)
        tree.value = s
        file.write(str(tree.idPackage) + "," + str(s) + '\n')
        return s
    else :
        tree.value = round(df[tree.namePackage].mean())
        file.write(str(tree.idPackage) + "," + str(round(df[tree.namePackage].mean())) + '\n')
        return round(df[tree.namePackage].mean())
    
def supportSnapshot(tree, df, idSnapshot, file, withId):
    if tree.subPackages :
        s = 0
        for subPackage in tree.subPackages :
            s += supportSnapshot(subPackage, df, idSnapshot, file, withId)
        tree.value = s
        if withId :
            file.write(str(idSnapshot) + "," + str(tree.idPackage) + "," + str(s) + '\n')
        else : 
            file.write(str(tree.idPackage) + "," + str(s) + '\n')
        return s
    else :
        tree.value = int(df.iloc[idSnapshot][tree.namePackage])
        if withId :
            file.write(str(idSnapshot) + "," + str(tree.idPackage) + "," + str(int(df.iloc[idSnapshot][tree.namePackage])) + '\n')
        else :
            file.write(str(tree.idPackage) + "," + str(int(df.iloc[idSnapshot][tree.namePackage])) + '\n')
        return int(df.iloc[idSnapshot][tree.namePackage])
    
def supportAllSnapshot(df, fileSnapshots, fileSnapshotNames):
    dictSnapshotNames = {}
    for idSnapshot in range(df.shape[0]):
        fileSnapshotNames.write(str(idSnapshot) + "," + str(df.index[idSnapshot]) + '\n')
        treeSnapshotWithId = createTree(df.columns[:-1])
        treeSnapshotWithId.agregatePackages()
        s = supportSnapshot(treeSnapshotWithId, df, idSnapshot, fileSnapshots, withId = True)
        
def isWeekEndDay(day):
    if day == 'Saturday' or day == 'Sunday' :
        return True
    return False