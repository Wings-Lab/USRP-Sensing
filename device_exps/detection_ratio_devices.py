import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':30})
matplotlib.rcParams['figure.figsize'] = 20, 9

def countTx(d):
    th = -68
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
            rep = 90
        if float(i) < th:
            skip = False
            low = 1
    return count

clocks = ['desktop']
runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

counts = {}

for clock in clocks:
    counts[clock] = []
    for r in runs:
        print clock, r
        data = np.loadtxt(clock+'_run'+str(r)+'.txt', skiprows=1)
        #plt.plot(data, marker='*')
        #plt.show()
        c = countTx(data)
        if c>40:
            counts[clock].append(c)

for i in counts:
    print i, counts[i], np.mean(counts[i])

tx = [72.8, 54, 44, 32, 13]

idx = np.arange(len(tx))
width = 0.22

plt.bar(idx, tx, width, label='Online PSD')
#plt.bar(idx+width, tx_iq, width, label='Offline FFT')

plt.ylim([0, 100])
plt.xlabel('CPU Clock Frequency (MHz)')
plt.ylabel('Detection Ratio')
plt.xticks(np.arange(len(tx))+width/2, ['Desktop', 'Smartphone', 'Odroid', 'RPi3', 'RPi1'])

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.legend()

plt.savefig('../plots/detection_ratio_devices.pdf')

plt.show()
