import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':45})
matplotlib.rcParams['figure.figsize'] = 16, 10

fig = plt.figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.15, bottom=0.2, right=0.95)

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

tx = [48.7, 44.6, 38.1, 27.6, 15.9, 4.8, 1.8]
tx_iq = [39, 30.6, 18.1, 10.6, 2.9, 0.8, 0]

idx = np.arange(len(tx))
width = 0.28

#plt.bar(idx, tx, width)
plt.plot(tx_iq, linewidth=10, marker='o', markersize='28', markeredgecolor='black', label='RTL-SDR')
plt.plot(tx, linewidth=10, marker='s', markersize='28', markeredgecolor='black', label='USRP-B210')

plt.ylim([0, 100])
plt.xlabel('Gain')
plt.ylabel('Detection Ratio (%)')
#plt.xticks(np.arange(len(tx)), ['<1', '5', '10', '15', '20', '25', '30'])
plt.xticks(np.arange(len(tx)), ['>600', '500', '400', '300', '200', '100', '50'], fontsize=40)

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.legend()

plt.savefig('../../plots/tx_moving_vs_detection_ratio_fft.pdf')

plt.show()
