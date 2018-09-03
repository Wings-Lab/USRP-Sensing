import os
import numpy as np
import matplotlib.pyplot as plt

def countTx(d):
    th = -70
    count = 0
    low = 1
    for i in d:
        if float(i) > th and low == 1:
            count += 1
            low = 0
        if float(i) < th:
           low = 1
    return count

srates = [2, 6, 16]
runs = [1, 2, 3]
counts = {}
for srate in srates:
    counts[srate] = []
    for r in runs:
        data = np.loadtxt('usrp_iq/'+str(srate)+'m_run'+str(r)+'_fft.txt')
        counts[srate].append(countTx(data))

for i in counts:
    print i, counts[i], np.mean(counts[i])
