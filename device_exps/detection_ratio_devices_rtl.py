import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':50})
matplotlib.rcParams['figure.figsize'] = 20, 12

fig = plt.figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.12, bottom=0.2, right=0.95)

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

tx = [95.8, 36, 31, 15]
tx_iq = [99.5, 95.1, 85.3, 70.6]

idx = np.arange(len(tx))
width = 0.22

plt.bar(idx, tx, width, label='Online PSD')
plt.bar(idx+width, tx_iq, width, label='Offline PSD')

plt.ylim([0, 119])
plt.xlabel('Devices')
plt.ylabel('Detection Ratio (%)')
plt.xticks(np.arange(len(tx))+width/2, ['Desktop', 'Odroid-C2', 'RPi3', 'RPi1'])

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.legend(ncol=2, fontsize=40)

plt.savefig('../plots/detection_ratio_devices_rtl.pdf')

plt.show()
