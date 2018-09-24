import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':42})
matplotlib.rcParams['figure.figsize'] = 14, 10

fig = plt.figure()
ax = fig.add_subplot(111)

fig.subplots_adjust(left=0.15, bottom=0.15, right=0.99)

#def countTx(d):
#    th = -70
#    count = 0
#    low = 1
#    for i in d:
#        if float(i) > th and low == 1:
#            count += 1
#            low = 0
#        if float(i) < th:
#           low = 1
#    return count
#
#srates = [512, 2, 4, 8, 16]
#runs = [1, 2, 3, 4, 5]
#counts = {}
#for srate in srates:
#    counts[srate] = []
#    for r in runs:
#        print srate, r
#        data = np.loadtxt('fft/'+str(srate)+'m_run'+str(r)+'.txt', skiprows=22, usecols=7)
#        counts[srate].append(countTx(data))
#
#tx = []
#for i in counts:
#    print i, counts[i], np.mean(counts[i])
#    tx.append(np.mean([i]))

tx = [13.3999999999999999, 45]
tx_iq = [65.2, 93.8]

idx = np.arange(len(tx))
width = 0.28

plt.bar(idx, tx, width, label='Online PSD')
plt.bar(idx+width, tx_iq, width, label='Offline PSD')

plt.ylim([0, 100])
plt.xlabel('Samping Rate (MHz)')
plt.ylabel('Detection Ratio (%)')
plt.xticks(np.arange(len(tx)+width/2), [1, 2])

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.legend()

plt.savefig('../../../plots/sampling_rate_vs_detection_ratio_rtl.pdf')

plt.show()
