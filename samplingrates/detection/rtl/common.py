import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':50})
matplotlib.rcParams['figure.figsize'] = 12, 12.2

fig = plt.figure()
ax = fig.add_subplot(111)

fig.subplots_adjust(left=0.18, bottom=0.15, right=0.99)

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

tx = [23.3999999999999999, 35.3]
tx_iq = [75.2, 93.8]

idx = np.arange(len(tx))
width = 0.12

plt.bar(idx, tx, width, label='Online PSD')
plt.bar(idx+width, tx_iq, width, label='Offline PSD')

plt.ylim([0, 100])
plt.xlabel('Samping Rate (MHz)')
plt.ylabel('Detection Ratio (%)')
plt.xticks(np.arange(len(tx))+width/2, [1, 2])

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.legend(fontsize=45, loc='upper center')

plt.savefig('../../../plots/sampling_rate_vs_detection_ratio_rtl.pdf')

plt.show()
