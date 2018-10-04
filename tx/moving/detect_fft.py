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
            rep = 50
        if float(i) < th:
            skip = False
            low = 1
    return count

srates = [1, 2, 3, 4]
counts = []
for srate in srates:
    print srate
    data = np.loadtxt(str(srate)+'.txt', skiprows=22)
    #plt.plot(data, marker='*')
    #plt.show()
    counts.append(countTx(data))

print counts

tx = [48, 42.6, 30.1, 22.6, 8.9]

idx = np.arange(len(tx))
width = 0.28

plt.bar(idx, tx, width)

plt.ylim([0, 100])
plt.xlabel('Distance (m)')
plt.ylabel('Detection Ratio (%)')
plt.xticks(np.arange(len(tx)), ['<1', '5', '10', '15', '20'])

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.savefig('../../plots/tx_moving_vs_detection_ratio_fft.pdf')

plt.show()
