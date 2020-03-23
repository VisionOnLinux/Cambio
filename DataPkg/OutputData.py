

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
		searchOps=[self.changeCar]#,self.switchCars,self.changeReservation,self.switchReservation]
		function=random.choice(searchOps)
		function()

	def changeCar(self):
		car,zone=random.choice(list(self.carZones.items()))
		new_zone=random.choice(zone.getZonesObj())
		delete = []
		self.carZones[car]=new_zone
		for r,c in self.resCars.items():
			if c is car:
				if not self.checkZone(r.getZoneObj(),c):
					delete.append(r)
					for i in range(len(self.usedCars[c])):
						if int(self.usedCars[c][i][0]) == int(r.getStart()):
							self.usedCars[c].pop(i)
							break
		for res in delete:
			del self.resCars[res]
			self.unassigned.append(res)
		self.reassign()


	def switchCars(self):
		print('switchcars')

	def changeReservation(self):
		print('changereservation')
	def switchReservation(self):
		print('switchreservation')

	def reassign(self):
		delete = []
		for idx,r in enumerate(self.unassigned):
			#r.print()
			match = 0
			timeslot = 0
			for c in r.getCarsObj():
				timeslot = self.checkTime(c, r.getStart(), r.getDuration())
				if timeslot > 0:   	  # Car free?
					if self.checkZone(r.getZoneObj(), c):  # Car zone ok?
						self.resCars[r] = c
						match = 1
						break
					else:
						continue
				else:
					continue
			if match:
				delete.append(idx)
				i = self.resCars[r]
				s = r.getStart()
				d = r.getDuration()
				if timeslot == 1 :
					self.usedCars[i].append((s,d))
				elif timeslot == 2 :
					self.usedCars[i].insert(0, (s, d))
				elif timeslot == 3 :
					self.usedCars[i].append((s, d))
				else:
					self.usedCars[i].insert(timeslot-3, (s, d))

		for c,i in enumerate(delete):
			self.unassigned.pop(i-c)

	def checkTime(self, i, s, d):
		x = self.usedCars[i]
		if not x:
			#self.usedCars[i].append((s,d))
			return 1
		elif int(x[0][0]) >= (int(s) +int(d)):
			#self.usedCars[i].insert(0, (s, d))
			return 2
		elif (int(x[len(x) - 1][0]) + int(x[len(x) - 1][1])) <= int(s):
			#self.usedCars[i].append((s, d))
			return 3
		else:
			for (idx, t) in enumerate(x):
				sx,dx=t
				sx = int(sx)
				dx = int(dx)
				if idx == (len(x) - 1):
					return 0
				(sy, dy) = x[idx + 1]
				sy = int(sy)
				dy = int(dy)
				if (int(s) >= (sx + dx) and (int(s) +int(d)) <= sy):
					#self.usedCars[i].insert(idx + 1, (s, d))
					return 4+idx
				else:
					return 0

	def checkZone(self, zone, i):
		z = self.carZones[i]
		#print(z,zone)
		if z is zone:
			return 1

		for z1 in z.getZones():
			if zone is z1:
				return 1
		return 0

	def getCost(self):
		self.cost=0
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
			timeslot = 0
			for c in r.getCarsObj():
				timeslot = self.checkTime(c, r.getStart(), r.getDuration())
				if timeslot > 0:   	  # Car free?
					if self.carZones[c] is None:
						self.carZones[c] = r.getZoneObj()
						self.resCars[r] = c
						match = 1
						break
					elif self.checkZone(r.getZoneObj(), c):  # Car zone ok?
						self.resCars[r] = c
						match = 1
						break
					else:
						continue
				else:
					continue
			if not match:
				self.unassigned.append(r)
			else:
				i = self.resCars[r]
				s = r.getStart()
				d = r.getDuration()
				if timeslot == 1 :
					self.usedCars[i].append((s,d))
				elif timeslot == 2 :
					self.usedCars[i].insert(0, (s, d))
				elif timeslot == 3 :
					self.usedCars[i].append((s, d))
				else:
					self.usedCars[i].insert(timeslot-3, (s, d))


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
