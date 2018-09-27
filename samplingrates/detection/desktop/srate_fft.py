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

srates = [4]
runs = [1, 2, 3]
counts = {}
for srate in srates:
    counts[srate] = []
    for r in runs:
        print srate, r
        data = np.loadtxt('desktop_'+str(srate)+'m_run'+str(r)+'.txt', skiprows=1, comments='2018')
        plt.plot(data, marker='*')
        plt.show()
        counts[srate].append(countTx(data))

#tx = []
for i in counts:
    print i, counts[i], np.mean(counts[i])
#    tx.append(np.mean([i]))
#
#tx = [np.mean(counts[512]), 45, np.mean(counts[2]), np.mean(counts[4]), 25, np.mean(counts[8]), np.mean(counts[16])]
#
#idx = np.arange(len(tx))
#width = 0.28
#
#plt.bar(idx, tx, width)
#
#plt.ylim([0, 100])
#plt.xlabel('Samping Rate (MHz)')
#plt.ylabel('Detection Ratio (%)')
#plt.xticks(np.arange(len(tx)), [0.5, 1, 2, 4, 6, 8, 16])
#
#ax = plt.gca()
#ax.yaxis.grid(linestyle='dotted')
#
#plt.savefig('sampling_rate_vs_detection_ratio_fft.pdf')
#
#plt.show()
