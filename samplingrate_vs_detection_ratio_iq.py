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

srates = [2, 4, 6, 8, 16]
runs = [1, 2, 3, 4, 5]
counts = {}
for srate in srates:
    counts[srate] = []
    for r in runs:
        data = np.loadtxt('usrp_iq/'+str(srate)+'m_run'+str(r)+'_fft.txt')
        counts[srate].append(countTx(data))

for i in counts:
    print i, counts[i], np.mean(counts[i])

tx = [93.8, 61.8, 34.8, 26.6, 17.4, 12.8]

idx = np.arange(len(tx))
width = 0.28

plt.bar(idx, tx, width)

plt.ylim([0, 100])
plt.xlabel('Transmission Length (ms)')
plt.ylabel('Detection Ratio')
plt.xticks(np.arange(len(tx)), [1, 2, 4, 6, 8, 16])

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.savefig('plots/sampling_rate_vs_detection_ratio.pdf')

plt.show()
