import csv


from DataPkg.Car import Car
from DataPkg.Reservation import Reservation as Res
from DataPkg.Zone import Zone


class InputData:
	def __init__ (self):
		self.cars = []
		self.res  = []
		self.zones= []

	def loadCSV(self, fn):
		print(fn)
		with open(fn) as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=';')

			numReq = int(next(csv_reader)[0].split(": ")[1])

			for idx in range(0, numReq):
				line = next(csv_reader)
				print(line)
				