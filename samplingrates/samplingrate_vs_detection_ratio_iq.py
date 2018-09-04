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

srates = [512, 2, 4, 8, 16]
runs = [1, 2, 3, 4, 5]
counts = {}
for srate in srates:
    counts[srate] = []
    for r in runs:
        print srate, r
        data = np.loadtxt(str(srate)+'m_run'+str(r)+'.txt', skiprows=22, usecols=7)
        counts[srate].append(countTx(data))

for i in counts:
    print i, counts[i], np.mean(counts[i])

tx = [93.8, 61.8, 34.8, 26.6, 17.4, 12.8]

idx = np.arange(len(tx))
width = 0.28

plt.bar(idx, tx, width)

plt.ylim([0, 100])
plt.xlabel('Samping Rate (MHz)')
plt.ylabel('Detection Ratio (%)')
plt.xticks(np.arange(len(tx)), [1, 2, 4, 6, 8, 16])

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.savefig('sampling_rate_vs_detection_ratio_fft.pdf')

plt.show()
