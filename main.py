#!/usr/bin/env python3

import sys
import copy
import random

from multiprocessing import Pool

from DataPkg.InputData import InputData as InD
from DataPkg.OutputData import OutputData as OutD

in_file   = sys.argv[1]
out_file  = sys.argv[2]
time_lim  = sys.argv[3]
rand_seed = sys.argv[4]
threads   = sys.argv[5]

random.seed(rand_seed)

ind = InD()
ind.loadCSV(in_file)

outd = OutD()
outd.initialise(ind)
outd2=copy.deepcopy(outd)

for i in range(10000):
    outd2.localSearch()
    if outd.getCost()>outd2.getCost():
        outd=copy.deepcopy(outd2)
        print('Best',outd2.getCost())
    else:
        outd2=copy.deepcopy(outd)

outd.saveCSV(out_file)