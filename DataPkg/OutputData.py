

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
		The function takes 30% of all cars from the list and shuffles their zones
		half the number of cars were picked.
		"""
		amountCars     = int(len(self.carZones) * 0.3)	# Get the amount of 70% of cars
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
		"""
		Change the car from a specific reservation.

		Pick a random reservation and select a random car from all possible cars for this reservation.
		Check all reservations who became invallid and remove them.
		Try to reassign as much unassigned reservations as possible.
		"""
		res,car   = None,None 	# Save the reservation we're changing with it's previous car
		chosenCar = None 		# Save the new car we are going to assign to the reservation
		delete    = []			# Keep a list of reservations which need to be deleted
		while True:				# Search for a reservation with more than 1 possible car
			res,car  = random.choice(list(self.resCars.items()))
			carCount = res.getCarsObj()
			if len(carCount) > 1:
				while True:		# Search for another car for this reservation which is not the previous car
					chosenCar = random.choice(carCount)
					if chosenCar is not car:
						self.resCars[res] = chosenCar
						break
				break
		for i in range(len(self.usedCars[car])):			# Find the used timeslot of the reservation for the old car and remove it
			if int(self.usedCars[car][i][0]) == int(res.getStart()):
				self.usedCars[car].pop(i)
				break
		if not self.checkZone(res.getZoneObj(),chosenCar):	# If the car is in the wrong zone, ...
			matchingZone = 0
			for z in res.getZoneObj().getZonesObj():		# Search for neighbouring zones which will work with the reservation
				if (self.checkZone(z,chosenCar)):
					self.carZones[chosenCar] = z 			# Change the zone of the car
					matchingZone = 1
					break
			if not matchingZone:							# If their are no neighbouring matching zones, ...
				self.carZones[chosenCar] = res.getZoneObj() # change the car to the zone of the reservation

		for r,c in self.resCars.items():	# Check for all reservations who use this car if they are still feasible
			if c is chosenCar:
				if not self.checkZone(r.getZoneObj(),c):
					delete.append(r)		# Otherwise, add them to the delete list
					for i in range(len(self.usedCars[c])):	# And remove their timeslot from the car
						if int(self.usedCars[c][i][0]) == int(r.getStart()):
							self.usedCars[c].pop(i)
							break
		for resDel in delete:				# Remove the reservations from the list
			del self.resCars[resDel]
			self.unassigned.append(resDel)	# Add the removed reservations to the unassigned list

		delete    = []	# Empty the list of cars to delete
		deletepop = []	# Create a new list of timeslot to delete from the car
		timeslot  = self.checkTime(chosenCar,res.getStart(),res.getDuration())	# Check if the reservation fits in the schedule of the car
		if timeslot > 0:		# If so, add it to the schedule
			self.addTimeslot(timeslot, res, chosenCar)
		else:					# If not, remove all conflicting reservations
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
			for res in delete:								# Remove the reservations from the list
				del self.resCars[res]
				self.unassigned.append(res)
			for c,i in enumerate(deletepop):				# Remove conflicting timeslots
				self.usedCars[chosenCar].pop(i-c)

			timeslot = self.checkTime(chosenCar,res.getStart(),res.getDuration())	# If no further conflicts ...
			if timeslot > 0:
				self.addTimeslot(timeslot, res, chosenCar)	# Add the reservation in the schedule
		self.reassign() # Try to reassign as much of the unassigned reservations as possible

	def reassign(self):
		"""
		Reassign as many reservations as possible who were previously unassigned
		"""
		delete = []			# Empty the list of reservations to delete
		random.shuffle(self.unassigned)	# Shuffle the unassigned reservations to make sure we're not always starting with the same one
		for idx,r in enumerate(self.unassigned):	# For all unassigned reservations ...
			match    = 0	# Found a matching car?
			timeslot = 0	# Is there a possible timeslot? If so, where is it?
			for c in r.getCarsObj():	# Check all possible cars for this reservation
				timeslot = self.checkTime(c, r.getStart(), r.getDuration())	# Is there a usable timeslot in this cars schedule?
				if timeslot > 0:
					if self.checkZone(r.getZoneObj(), c): 	# Is the assigned zone okay for the reservation
						self.resCars[r] = c 				# If yes, match found. This car will be assigned to the reservation
						match = 1
						break
					else:
						continue
				else:
					continue
			if match:					# If there was a car found ...
				delete.append(idx)		# Delete the reservation from the unassigned
				i = self.resCars[r]
				self.addTimeslot(timeslot, r, i)	# Add the timeslot to the schedule of the car

		for c,i in enumerate(delete):	# Remove all matched reservations
			self.unassigned.pop(i-c)

	def checkTime(self, i, s, d):
		"""
		Check if there is a usable timeslot in the schedule of the car.

		i: Car to check schedule from
		s: Start of check time
		d: Duration of timeslot

		Return values:
		0:  There is no space in the schedule
		1:  The schedule is empty or the reservation is after all other reservations, so it can be added to the end of the list
		2:  The reservation is before all other reservations, so add it to the beginning of the list
		>3: The reservation is in between 2 other timeslots at index: return value - 4
		"""
		x    = self.usedCars[i]
		s    = int(s)
		d    = int(d)
		last = len(x) - 1
		if not x:										return 1
		elif int(x[0][0]) >= (s + d):					return 2
		elif (int(x[last][0]) + int(x[last][1])) <= s:	return 1
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
		"""
		Add a reservation to the schedule of a specific car.

		ts:  Timeslot (See return of checkTime())
		res: The reservation
		car: The car
		"""
		s = res.getStart()		# Get start time from the reservation
		d = res.getDuration()	# Get the duration from the reservation
		if ts == 1:		self.usedCars[car].append((s, d))			# Append the timeslot to the end of the list
		elif ts == 2:	self.usedCars[car].insert(0, (s, d))		# Insert the timeslot at the beginning of the list
		else:			self.usedCars[car].insert(ts - 3, (s, d))	# Insert the timeslot at a specific place in the list

	def checkZone(self, zone, i):
		"""
		Check if a car is in a zone or a neighbouring zone.

		zone:	The zone to check
		i: 		The car to check

		Return values:
		1: A match is found, the car is in the same or a neighbouring zone
		0: No match is found
		"""
		z = self.carZones[i]	# Get the zone in which the car is located
		if z is zone:		return 1	# If the zone is the same, it's okay
		for z1 in z.getZones():			# Else check all neighbouring zones
			if zone is z1:	return 1	# If the zone is a neighbour it's also okay
		return 0						# Otherwise there is no match

	def getCost(self):
		"""
		Calculate the cost of this solution.

		Depending if a reservation is connected to a car in it's own zone or a neighbouring zone
		or if it isn't assigned a car, the cost will be calculated.

		Return value:
		The cost of the solution
		"""
		self.cost = 0	# Set the cost to 0 so we can add to it
		for r in self.unassigned:	# For all unassigned reservations ...
			self.cost += r.p1		# Add the P1 cost to the total cost
		for r,c in self.resCars.items():	# For all reservations which are in a neighbouring zone ...
			if self.carZones[c].getName() != r.getZone():
				self.cost += r.p2			# Add the P2 cost to the total cost

		return self.cost

	def getCarZones(self):
		return self.carZones

	def getResCars(self):
		return self.resCars

	def getUnassigned(self):
		return self.unassigned

	def initialise(self, inp):
		"""
		Create a initial solution using the input data.

		This function creates an initial solution to start local search on.

		inp: The input file loaded in the InputData class
		"""
		for car in inp.getCars():		# For all available cars in the input ...
			self.usedCars[car] = []		# Create an empty schedule
			self.carZones[car] = None 	# And add an element to the carZones list
		for r in inp.getReservations():	# For all reservations ...
			match    = 0	# Found a matching car?
			timeslot = 0	# What timeslot can it be added?
			for c in r.getCarsObj():	# Check all possible cars until there is a match
				timeslot = self.checkTime(c, r.getStart(), r.getDuration())
				if timeslot > 0: 		# Is the car free?
					if self.carZones[c] is None:	# If the car hasn't been assigned to anything yet
						self.carZones[c] = r.getZoneObj()	# Assign it to the zone of the reservation
						self.resCars[r]  = c 				# And link it to the reservation.
						match = 1	# There is a match for this reservation
						break		# Look no further
					elif self.checkZone(r.getZoneObj(), c):	# If the car is assigned already, check if the zone matches with the zone of the reservation
						self.resCars[r] = c 	# If the zone matches, link the reservation and the car
						match = 1				# There is a match
						break					# Look no further
					else:
						continue
			if not match:					# If there is no match found ...
				self.unassigned.append(r)	# Add the reservation to the unassigned list
			else:
				i = self.resCars[r]			# If there is a match, add the reservation to the schedule of the car
				self.addTimeslot(timeslot, r, i)

		for c,z in self.carZones.items():	# Assign all unused cars to the first zone
			if z is None:
				self.carZones[c] = inp.getZones()[0]

	def print(self):
		"""
		Print the solution to the terminal.
		"""
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
		"""
		Write the solution to a csv file.
		"""
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
