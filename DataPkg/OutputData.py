

from DataPkg.Car import Car
from DataPkg.Zone import Zone


class OutputData:
	def __init__(self):
		self.cost 	   = 0
		self.carZones  = []
		self.resCars   = []
		self.unassigned= []

	def getCost(self):
		return self.cost

	def getCarZones(self):
		return self.carZones

	def getResCars(self):
		return self.resCars

	def getUnassigned(self):
		return self.unassigned

	def initialise(self, res):
		for r in res:
			self.unassigned.append(r)