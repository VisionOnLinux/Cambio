#!/usr/bin/env python3

import sys
import copy
import time
import random

from multiprocessing import Pool

from DataPkg.InputData import InputData as InD
from DataPkg.OutputData import OutputData as OutD

in_file   = sys.argv[1]
out_file  = sys.argv[2]
time_lim  = int(sys.argv[3])
rand_seed = int(sys.argv[4])
threads   = int(sys.argv[5])

random.seed(rand_seed)

ind = InD()
ind.loadCSV(in_file)

outd = OutD()
outd.initialise(ind)
outd2=copy.deepcopy(outd)

timeout_start = time.time()
idx = 0

while time.time() < timeout_start + time_lim:
    idx += 1
    outd2.localSearch()
    if outd.getCost() > outd2.getCost():
        outd = copy.deepcopy(outd2)
        print('Best', outd2.getCost())
    else:
        outd2 = copy.deepcopy(outd)

outd.saveCSV(out_file)
print("Iter:", idx)