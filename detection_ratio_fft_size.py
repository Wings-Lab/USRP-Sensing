import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':30})
matplotlib.rcParams['figure.figsize'] = 18, 10

def countTx(d):
    th = -60
    count = 0
    low = 1
    skip = False
    rep = 0
    for i in d:
        if skip and rep > 0:
            rep -= 1
            continue
        if float(i) > th and low == 1:
            count += 1
            low = 0
            skip = True
            rep = 125
        if float(i) < th:
            skip = False
            low = 1
    return count

clocks = [64, 128, 256, 512, 1024]
runs = [1, 2, 3, 4, 5]

counts = {}

for clock in clocks:
    counts[clock] = []
    for r in runs:
        print clock, r
        data = np.loadtxt('fft_exps/fft_'+str(clock)+'_'+str(r)+'.txt', skiprows=25)
        #plt.plot(data, marker='*')
        #plt.show()
        c = countTx(data)
        counts[clock].append(c)

for i in counts:
    print i, counts[i], np.mean(counts[i])
