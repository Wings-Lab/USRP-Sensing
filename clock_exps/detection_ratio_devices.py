import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':30})
matplotlib.rcParams['figure.figsize'] = 20, 9

def countTx(d):
    th = -70
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
            rep = 105
        if float(i) < th:
            skip = False
            low = 1
    return count

#clocks = [100, 250, 500, 1000, 1250, 1536]
clocks = [100, 500, 1296]
#clocks = [100, 250, 500, 1000, 1296]
#runs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
runs = [1, 2, 3, 4, 5]

counts = {}

for clock in clocks:
    counts[clock] = []
    for r in runs:
        print clock, r
        #data = np.loadtxt('clock_exps/tx_100/'+str(clock)+'_run'+str(r)+'.txt', skiprows=22, usecols=7)
        data = np.loadtxt('usrp_clock_exps/usrp_'+str(r)+'_'+str(clock)+'.txt', skiprows=25)
        #plt.plot(data, marker='*')
        #plt.show()
        c = countTx(data)
        if c > 5:
            counts[clock].append(c)

for i in counts:
    print i, counts[i], np.mean(counts[i])

tx = [40, 54, 57, 58, 63, 67]

idx = np.arange(len(tx))
width = 0.22

plt.bar(idx, tx, width, label='Online PSD')
#plt.bar(idx+width, tx_iq, width, label='Offline FFT')

plt.ylim([0, 100])
plt.xlabel('CPU Clock Frequency (MHz)')
plt.ylabel('Detection Ratio')
plt.xticks(np.arange(len(tx))+width/2, ['Desktop', 'Smartphone', 'Odroid', 'RPi3', 'RPi0', 'FPGA'])

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.legend()

plt.savefig('plots/detection_ratio_devices.pdf')

plt.show()
