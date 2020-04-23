

from DataPkg.Car import Car
from DataPkg.Zone import Zone
import random
import csv


class OutputData:
	"""Holds the contents for the search algorithm and has methods to do specific types of searches."""

	def __init__(self):
		"""
		Initialise all internal lists and dictionaries to have empty elements.

		Structures of all dictionaries and lists:
			carZones: 	{carID: zone, carID: zone}
			resCars:	{res: car, res: car}
			unassigned:	[res, res]
			usedCars:	{carID: [(t1, d1), (t2, d2)], carID: [(t1, d1), (t2, d2)]}
		"""
		self.cost 	   = 0		# The cost of this solution
		self.carZones  = dict()	# Define for every car a zone
		self.resCars   = dict() # Connect all reservations to a specific car
		self.unassigned= []     # All reservations that have no solution
		self.usedCars  = dict() # Keep a timetable for all cars 

	def localSearch(self):
		"""
		Execute local search on the data.

		Shuffles all reservations linked to cars and than
		picks a random function from the list to apply to the data.
		"""

		l = list(self.resCars.items())	# Convert the dictionary to a list
		random.shuffle(l)				# Shuffle the list at random
		self.resCars   = dict(l)		# Convert the list back to a dictionary
		searchOps 	   = [				# A list of the different functions that can be picked
			self.changeManyCars,
			self.changeCar,
			self.changeReservation
		]
		searchFunction = random.choice(searchOps)	# Pick a function from the list at random
		searchFunction()				# Execute the function on the data

	def changeManyCars(self):
		"""
		Pick a number of cars from the list and shuffle their zones around
		
		This is quite a big jump for local search, but it prevents local minimum.
		The function takes 70% of all cars from the list and shuffles their zones 
		half the number of cars were picked.
		"""
		amountCars     = int(len(self.carZones) * 0.7)	# Get the amount of 70% of cars
		amountShuffles = int(amountCars // 2)			# Divide it by 2 for the amount of shuffles
		delete = []		# A list to keep track of all the reservations that need to be removed from the resCars list
		zones  = []		# A list to keep all the zones from the cars in while shuffling
		cars   = random.sample(list(self.carZones),amountCars)	# Sample 70% of the cars from the list
		for c in cars:	# Get all zones from the cars and clear the usage table
			zones.append(self.carZones[c])
			self.usedCars[c] = []
		for res,car in self.resCars.items():	# Find all reservations connected to those cars to be removed
			if car in cars:
				delete.append(res)
				self.unassigned.append(res)
		for d in delete:						# Remove the reservations from the list
			del self.resCars[d]

		for _ in range(amountShuffles):			# Shuffle all zones
			random.shuffle(zones)
		for idx in range(amountCars):			# Reconnect the cars and the shuffled zones
			self.carZones[cars[idx]] = zones[idx]
		self.reassign()	# Try to reassign as much of the unassigned reservations as possible

	def changeCar(self):
		"""
		Switch a car to a neighbouring zone

		Pick a random car and switch it to a random connected neighbouring zone
		"""
		car,zone = random.choice(list(self.carZones.items()))	# Pick a random car from the list
		new_zone = random.choice(zone.getZonesObj())			# Pick a random neighbour zone from the previous zone of the car
		delete   = []	# A list to keep track of all the reservations that need to be removed from the resCars list 
		self.carZones[car] = new_zone		# Apply the new zone to the selected car
		for r,c in self.resCars.items():	# For all reservations that used this car, ...
			if c is car:
				if not self.checkZone(r.getZoneObj(),c):	# Check if the zone is not to far for the reservation
					delete.append(r)						# If not, remove the reservation
					for i in range(len(self.usedCars[c])):	# Find the used timeslot of the reservation and clear it
						if int(self.usedCars[c][i][0]) == int(r.getStart()):
							self.usedCars[c].pop(i)
							break
		for res in delete:			# Remove the reservations from the list
			del self.resCars[res]
			self.unassigned.append(res)
		self.reassign()	# Try to reassign as much of the unassigned reservations as possible

	def changeReservation(self):
		res,car   = None,None
		chosenCar = None
		delete    = []
		while True:
			res,car  = random.choice(list(self.resCars.items()))
			carCount = res.getCarsObj()
			if len(carCount) > 1:
				while True:
					chosenCar = random.choice(carCount)
					if chosenCar is not car:
						self.resCars[res] = chosenCar
						break
				break
		if not self.checkZone(res.getZoneObj(),chosenCar):
			matchingZone = 0
			for z in res.getZoneObj().getZonesObj():
				if (self.checkZone(z,chosenCar)):
					self.carZones[chosenCar] = z
					matchingZone = 1
					break
			if not matchingZone:
				self.carZones[chosenCar] = res.getZoneObj()

		for r,c in self.resCars.items():
			if c is chosenCar:
				if not self.checkZone(r.getZoneObj(),c):
					delete.append(r)
					for i in range(len(self.usedCars[c])):
						if int(self.usedCars[c][i][0]) == int(r.getStart()):
							self.usedCars[c].pop(i)
							break
		for resDel in delete:
			del self.resCars[resDel]
			self.unassigned.append(resDel)

		delete    = []
		deletepop = []
		timeslot  = self.checkTime(chosenCar,res.getStart(),res.getDuration())
		if timeslot > 0:
			self.addTimeslot(timeslot, res, chosenCar)
		else:
			s2 = int(res.getStart())
			d2 = int(res.getDuration())
			for i in range(len(self.usedCars[chosenCar])):
				s1 = int(self.usedCars[chosenCar][i][0])
				d1 = int(self.usedCars[chosenCar][i][1])
				if (((s1 < s2) and (s1 + d1 >= s2)) or ((s1 > s2) and (s1 <= s2 + d2))):
					deletepop.append(i)
					for r,c in self.resCars.items():
						if c is chosenCar and int(r.getStart()) == s1 :
							delete.append(r)
			for res in delete:
				del self.resCars[res]
				self.unassigned.append(res)
			for c,i in enumerate(deletepop):
				self.usedCars[chosenCar].pop(i-c)

			timeslot = self.checkTime(chosenCar,res.getStart(),res.getDuration())
			if timeslot > 0:
				self.addTimeslot(timeslot, res, chosenCar)
		self.reassign()

	def reassign(self):
		delete = []
		random.shuffle(self.unassigned)
		for idx,r in enumerate(self.unassigned):
			match    = 0
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
				self.addTimeslot(timeslot, r, i)

		for c,i in enumerate(delete):
			self.unassigned.pop(i-c)

	def checkTime(self, i, s, d):
		x    = self.usedCars[i]
		s    = int(s)
		d    = int(d)
		last = len(x) - 1
		if not x:										return 1
		elif int(x[0][0]) >= (s + d):					return 2
		elif (int(x[last][0]) + int(x[last][1])) <= s:	return 3
		else:
			for idx, (sx, dx) in enumerate(x):
				if idx == last:			return 0
				(sy, dy) = x[idx + 1]
				sx = int(sx)
				dx = int(dx)
				sy = int(sy)
				dy = int(dy)
				if (s >= (sx + dx) and (s + d) <= sy):	return 4 + idx
			return 0

	def addTimeslot(self, ts, res, car):
		s = res.getStart()
		d = res.getDuration()
		if ts   == 1 :
			self.usedCars[car].append((s,d))
		elif ts == 2 :
			self.usedCars[car].insert(0, (s, d))
		elif ts == 3 :
			self.usedCars[car].append((s, d))
		else:
			self.usedCars[car].insert(ts - 3, (s, d))

	def checkZone(self, zone, i):
		z = self.carZones[i]
		if z is zone:		return 1
		for z1 in z.getZones():
			if zone is z1:	return 1
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
			match    = 0
			timeslot = 0
			for c in r.getCarsObj():
				timeslot = self.checkTime(c, r.getStart(), r.getDuration())
				if timeslot > 0:   	  # Car free?
					if self.carZones[c] is None:
						self.carZones[c] = r.getZoneObj()
						self.resCars[r]  = c
						match = 1
						break
					elif self.checkZone(r.getZoneObj(), c):  # Car zone ok?
						self.resCars[r] = c
						match = 1
						break
					else:
						continue
			if not match:
				self.unassigned.append(r)
			else:
				i = self.resCars[r]
				self.addTimeslot(timeslot, r, i)

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

	def saveCSV(self,pathName):
		with open(pathName,'w') as file:
			writer = csv.writer(file)
			writer.writerow([self.getCost()])
			writer.writerow(['+Vehicle assignments'])
			for car,zone in self.carZones.items():
				writer.writerow([car.getName()+';'+zone.getName()])
			writer.writerow(['+Assigned requests'])
			for req,car in self.resCars.items():
				writer.writerow([req.getName()+';'+car.getName()])
			writer.writerow(['+Unassigned requests'])
			for unreq in self.unassigned:
				writer.writerow([unreq.getName()])
