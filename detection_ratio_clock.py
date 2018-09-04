import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':30})
matplotlib.rcParams['figure.figsize'] = 18, 10

def countTx(d):
    th = -90
    count = 0
    low = 1
    for i in d:
        if float(i) > th and low == 1:
            count += 1
            low = 0
        if float(i) < th:
           low = 1
    return count

clocks = [100, 250, 500, 1000, 1296]
runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

counts = {}

for clock in clocks:
    counts[clock] = []
    for r in runs:
        data = np.loadtxt('clock_exps/'+str(clock)+'_run'+str(r)+'.txt', skiprows=22, usecols=7)
        #plt.plot(data, label=str(clock))
        #plt.legend()
        #plt.show()
        c = countTx(data)
        counts[clock].append(c)

for i in counts:
    #counts[i] = sorted(counts[i])[4:]
    print i, counts[i], np.mean(counts[i])

"""
tx = [100, np.mean(counts1), np.mean(counts2), np.mean(counts3), np.mean(counts4)]
tx = [i for i in reversed(tx)]
idx = np.arange(len(tx))
width = 0.22

tx_iq = [60, 94, 98, 99, 100]

plt.bar(idx, tx, width, label='Online FFT')
plt.bar(idx+width, tx_iq, width, label='Offline FFT')

plt.ylim([0, 100])
plt.xlabel('Transmission Length (ms)')
plt.ylabel('Detection Ratio')
plt.xticks(np.arange(len(tx))+width/2, [0.001, 1, 10, 100, 1000])

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')


plt.savefig('detection_ratio_usrp.pdf')

plt.show()
"""
