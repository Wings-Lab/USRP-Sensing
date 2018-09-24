import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':30})
matplotlib.rcParams['figure.figsize'] = 18, 10

def countTx(d):
    th = -3
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
            rep = 150
        if float(i) < th:
            skip = False
            low = 1
    return count


#def countTx(d):
#    th = -10
#    count = 0
#    low = 1
#    for i in d:
#        if float(i) > th and low == 1:
#            print i
#            count += 1
#            low = 0
#        if float(i) < th:
#           low = 1
#    return count

srates = [16]
runs = [2, 3, 4, 5]
counts = {}
for srate in srates:
    counts[srate] = []
    for r in runs:
        data = np.loadtxt(str(srate)+'m_run'+str(r)+'_fft.txt', usecols=1)
        #plt.plot(data, marker='*')
        #plt.show()
        counts[srate].append(countTx(data))

for i in counts:
    print i, counts[i], np.mean(counts[i])
