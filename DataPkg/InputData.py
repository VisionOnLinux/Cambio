import csv


from DataPkg.Car import Car
from DataPkg.Reservation import Reservation as Res
from DataPkg.Zone import Zone


class InputData:
	def __init__ (self):
		self.cars = []
		self.res  = []
		self.zones= []
		self.days = 0

	def loadCSV(self, fn):
		print(fn)
		with open(fn) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=';')

			while True:
				line = next(csv_reader)[0]
				num  = int(line.split(": ")[1])
				name = line.split(": ")[0]

				if name != "+Days":
					for idx in range(0, num):
						line = next(csv_reader)
						if name == "+Requests":
							req = Res(line[0], line[1], line[2], line[3], line[4], line[6], line[7])
							for car in line[5].split(","):
								req.addCar(car)

							self.res.append(req)
						elif name == "+Zones":
							zone = Zone(line[0])
							for z in line[1].split(","):
								zone.addZone(z)

							self.zones.append(zone)
						elif name == "+Vehicles":
							car = Car(line[0])
							self.cars.append(car)
				else:
					self.days = num
					break

	def getCars(self):
		return self.cars

	def getReservations(self):
		return self.res

	def getZones(self):
		return self.zones

	def getDays(self):
		return self.days