#!/usr/bin/env python3

from DataPkg.InputData import InputData as InD
from DataPkg.OutputData import OutputData as OutD

ind = InD()

ind.loadCSV("InputData/toy1.csv")

ind.getZones()[1].print()

outd =  OutD()
outd.initialise(ind.getReservations())

for r in outd.getUnassigned():
	r.print()
