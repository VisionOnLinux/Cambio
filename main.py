#!/usr/bin/env python3

import sys
from DataPkg.InputData import InputData as InD
from DataPkg.OutputData import OutputData as OutD

ind = InD()

ind.loadCSV(sys.argv[1])

#for r in ind.getReservations():
#	r.print()

#
#ind.getZones()[1].print()

outd =  OutD()
outd.initialise(ind)
outd.print()
outd.localSearch()
outd.localSearch()
outd.localSearch()
outd.localSearch()
#
# for r in outd.getUnassigned():
# 	r.print()
