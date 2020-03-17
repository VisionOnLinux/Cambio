

from DataPkg.Car import Car
from DataPkg.Zone import Zone


class OutputData:
	def __init__(self):
		self.cost 	   = 0
		self.carZones  = []	# {carID: zone, carID: zone}
		self.resCars   = [] # {res: car, res: car}
		self.unassigned= [] # [res, res]
		self.usedCars  = [] # {carID: [(t1, d1), (t2, d2)], carID: [(t1, d1), (t2, d2)]}

	def checkTime(self, i, s, d):
		x = self.usedCars[i]
		if x[0][0] >= (s + d):
			self.usedCars[i].insert(0, (s, d))
			return 1
		elif (x[len(x) - 1][0] + x[len(x) - 1][1]) <= s:
			self.usedCars.append((s, d))
			return 1
		else:
			for (idx, sx, dx) in enumerate(x):
				if idx == (len(x) - 1):
					return 0
				(sy, dy) = x[idx + 1]

				if (s >= (sx + dx) and (s + d) <= sy):
					self.usedCars.insert(idx + 1, (s, d))
					return 1
				else:
					return 0

	def checkZone(self, zone, i, zones):
		z = self.carZones[i]
		if z == zone:
			return 1
		for z1 in zones:
			if z == z1.getName():
				for z2 in z1.getZones():
					if zone == z2.getName():
						return 1

		return 0

	def getCost(self):
		for r in unassigned:
			self.cost += r.p1

		for r in resCars:
			if carZones[r[0]] != r[1].getZone():
				self.cost += r.p2

		return self.cost

	def getCarZones(self):
		return self.carZones

	def getResCars(self):
		return self.resCars

	def getUnassigned(self):
		return self.unassigned

	def initialise(self, inp):
		for r in inp.getReservations():
			for c in range(len(r.getCars())):
				if self.checkTime(c, r.getStart(), r.getDuration()):   			# Car free?
					if (self.carZones[c] == None):
						self.carZones[c] = r.getZone()
						self.resCars.append([c, res])
					elif self.checkZone(r.getZone(), c, inp.getZones()):   # Car zone ok?





			self.unassigned.append(r)