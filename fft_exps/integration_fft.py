import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':45})
matplotlib.rcParams['figure.figsize'] = 20, 10

fig = plt.figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.12, bottom=0.2, right=0.95)

def countTx(d):
    th = -100
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
            rep = 500
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
        #print clock, r
        data = np.loadtxt('1ms/fft_'+str(clock)+'_'+str(r)+'.txt', skiprows=25)
        #plt.plot(data, label=clock, marker='*')
        #plt.legend()
        #plt.show()
        c = countTx(data)
        counts[clock].append(c)

for i in counts:
    print i, counts[i], np.mean(counts[i])

clocks = [128, 256, 512, 1024, 2048, 4096, 8192]
tx = [23.4, 30.6, 38.2, 14.1, 10.9, 9, 8.2]
tx_1 = [13.4, 46.6, 29.2, 18, 14.9, 13, 10.2]
idx = np.arange(len(tx))
width = 0.22

plt.bar(idx, tx, width, label='RTL-SDR')
plt.bar(idx+width, tx_1, width, label='USRP-B210')

plt.ylim([0, 100])
plt.xlabel('Integration Time (#Samples)')
plt.ylabel('Detection Ratio (%)')
plt.xticks(np.arange(len(tx))+width/2, clocks)

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.legend()

plt.savefig('../plots/detection_ratio_integration.pdf')

plt.show()
