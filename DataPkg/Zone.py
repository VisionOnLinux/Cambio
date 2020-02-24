class Zone:
    def __init__(self,name):
        self.name=name
        self.zones=[]

    def getName(self):
        return self.name

    def getZones(self):
        return self.zones

    def addZone(self,z):
        self.zones.add(z)
