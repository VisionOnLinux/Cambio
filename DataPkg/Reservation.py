

class Reservations:
	def __init__(self, name, z, day, start, dura, p1, p2):
		self.name = name
		self.zone = z
		self.day  = day
		self.start= start
		self.dura = dura
		self.p1   = p1
		self.p2   = p2
		self.cars = []

	def getName(self):
		return self.name

	def getZone(self):
		return self.zone

	def getDay(self):
		return self.day

	def getStart(self):
		return self.start

	def getDuration(self):
		return self.dura

	def getP1(self):
		return self.p1

	def getP2(self):
		return self.p2

	def addCar(self, c):
		self.cars.add(c)