class Zone:
	def __init__(self,name):
		self.name=name
		self.zones=[]
		self.zonesObj=[]

	def getName(self):
		return self.name

	def getZones(self):
		return self.zones

	def getZonesObj(self):
		return self.zonesObj

	def addZone(self,z):
		self.zones.append(z)

	def addZoneObj(self,z):
		self.zonesObj.append(z)

	def print(self):
		print(self.name)
		for z in self.zones:
			print(z)

