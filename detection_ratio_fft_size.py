import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':30})
matplotlib.rcParams['figure.figsize'] = 18, 10

def countTx(d):
    th = -80
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
            rep = 120
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
        #plt.plot(data, label=clock, marker='*')
        #plt.show()
        c = countTx(data)
        counts[clock].append(c)

for i in counts:
    print i, counts[i], np.mean(counts[i])

clocks = [32, 64, 128, 256, 512, 1024]
tx = [10, 12, 29, 36, 10, 1]
tx_1 = [10, 12, 29, 36, 10, 1]
idx = np.arange(len(tx))
width = 0.22

plt.bar(idx, tx, width, label='1ms')
plt.bar(idx+width, tx_1, width, label='1s')

#plt.ylim([0, 100])
plt.xlabel('FFT Size')
plt.ylabel('Detection Ratio')
plt.xticks(np.arange(len(tx))+width/2, clocks)

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.legend()

plt.savefig('plots/detection_ratio_fft_size.pdf')

plt.show()
