import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':30})
matplotlib.rcParams['figure.figsize'] = 18, 10

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

tx_l = ['100ms', '10ms', '1ms', '1us']

counts = {}
for f in tx_l:
    counts[f] = []
    for r in [1, 2, 3, 4, 5]:
        data = np.loadtxt('usrp_iq/'+f+'_run'+str(r)+'_fft.txt')
        counts[f].append(countTx(data))
for count in counts:
    print count, counts[count], np.mean(counts[count])
