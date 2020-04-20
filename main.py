#!/usr/bin/env python3

import sys
import copy
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
outd2=copy.deepcopy(outd)
for _ in range(10000):
    #print('.',end='',flush=True)
    #outd2=copy.deepcopy(outd)
    #outd2.print()
    outd2.localSearch()
    #outd2.print()
    #print('Cost',outd2.getCost())
    if outd.getCost()>outd2.getCost():
        outd=copy.deepcopy(outd2)
        print('Best',outd2.getCost())
    else:
        outd2=copy.deepcopy(outd)
#outd2.print()
#outd2.localSearch()
#outd2.print()
#outd2.localSearch()
outd.print()
#outd2.localSearch()
#outd2.print()

#
# for r in outd.getUnassigned():
# 	r.print()
