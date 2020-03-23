

from DataPkg.Car import Car
from DataPkg.Zone import Zone
import random


class OutputData:
	def __init__(self):
		self.cost 	   = 0
		self.carZones  = dict()	# {carID: zone, carID: zone}
		self.resCars   = dict() # {res: car, res: car}
		self.unassigned= []     # [res, res]
		self.usedCars  = dict() # {carID: [(t1, d1), (t2, d2)], carID: [(t1, d1), (t2, d2)]}
		random.seed()

	def localSearch(self):
		searchOps=[changeCar,switchCars,changeReservation,switchReservation]
		functionnr=random.randint(0,3)
		searchOps[functionnr]()

	def changeCar(self):
		print('changecar')

	def switchCars(self):
		print('switchcars')

	def changeReservation(self):
		print('changereservation')
	def switchReservation(self):
		print('switchreservation')


	def checkTime(self, i, s, d):
		x = self.usedCars[i]
		if not x:
			self.usedCars[i].append((s,d))
			return 1
		elif x[0][0] >= (s + d):
			self.usedCars[i].insert(0, (s, d))
			return 1
		elif (x[len(x) - 1][0] + x[len(x) - 1][1]) <= s:
			self.usedCars[i].append((s, d))
			return 1
		else:
			for (idx, t) in enumerate(x):
				sx,dx=t
				if idx == (len(x) - 1):
					return 0
				(sy, dy) = x[idx + 1]

				if (s >= (sx + dx) and (s + d) <= sy):
					self.usedCars[i].insert(idx + 1, (s, d))
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
					if zone == z2:
						return 1

		return 0

	def getCost(self):
		for r in self.unassigned:
			self.cost += r.p1
		for r,c in self.resCars.items():
			if self.carZones[c].getName() != r.getZone():
				self.cost += r.p2

		return self.cost

	def getCarZones(self):
		return self.carZones

	def getResCars(self):
		return self.resCars

	def getUnassigned(self):
		return self.unassigned

	def initialise(self, inp):
		for car in inp.getCars():
			self.usedCars[car] = []
			self.carZones[car] = None
		for r in inp.getReservations():
			match = 0
			for c in r.getCarsObj():
				if self.checkTime(c, r.getStart(), r.getDuration()):   	  # Car free?
					if self.carZones[c] is None:
						self.carZones[c] = r.getZoneObj()
						self.resCars[r] = c
						match = 1
						break
					elif self.checkZone(r.getZone(), c, inp.getZones()):  # Car zone ok?
						self.resCars[r] = c
						match = 1
						break
					else:
						continue
				else:
					continue
			if not match:
				self.unassigned.append(r)
		for c,z in self.carZones.items():
			if z is None:
				self.carZones[c] = inp.getZones()[0]

	def print(self):
		print(self.getCost())
		print('+Vehicle assignments')
		for car,zone in self.carZones.items():
			print(car.getName()+';'+zone.getName())
		print('+Assigned requests')
		for req,car in self.resCars.items():
			print(req.getName()+';'+car.getName())
		print('+Unassigned requests')
		for unreq in self.unassigned:
			print(unreq.getName())
