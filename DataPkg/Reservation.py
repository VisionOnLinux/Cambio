

class Reservation:
	def __init__(self, name, z, day, start, dura, p1, p2):
		self.name = name
		self.zone = z
		self.zoneObj = None
		self.day  = day
		self.start= start
		self.dura = dura
		self.p1   = p1
		self.p2   = p2
		self.cars = []
		self.carsObj = []

	def getName(self):
		return self.name

	def getZone(self):
		return self.zone

	def getZoneObj(self):
		return self.zoneObj

	def setZone(self, z):
		self.zoneObj = z

	def getDay(self):
		return self.day

	def getStart(self):
		return int(self.start)+(int(self.getDay())*(60*24))

	def getDuration(self):
		return self.dura

	def getP1(self):
		return self.p1

	def getP2(self):
		return self.p2

	def addCar(self, c):
		self.cars.append(c)

	def addCarObj(self, c):
		self.carsObj.append(c)

	def getCars(self):
		return self.cars

	def getCarsObj(self):
		return self.carsObj

	def print(self):
		print(self.name)
		print(self.zoneObj.getName())
		print(self.day)
		print(self.start)
		print(self.dura)
		print(self.p1)
		print(self.p2)

		for c in self.carsObj:
			print(c.getName())
