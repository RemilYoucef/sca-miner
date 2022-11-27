class Package (object):
    
    def __init__(self, namePackage, subPackages, idPackage):
        self.namePackage = namePackage
        self.subPackages = subPackages 
        self.idPackage = idPackage
        self._value = None
    
    'In case where the package have only one sub-packages'
    def agregatePackages(self):
        if len(self.subPackages) == 0 :
            return self
        elif len(self.subPackages) == 1 :
            return self.subPackages[0].agregatePackages()
        else :
            for i in range(len(self.subPackages)) :
                self.subPackages[i] = self.subPackages[i].agregatePackages()
            return self
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, x) :
        self._value = x 