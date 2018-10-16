import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':50})
matplotlib.rcParams['figure.figsize'] = 18, 10

fig = plt.figure()
ax = fig.add_subplot(111)

fig.subplots_adjust(left=0.18, bottom=0.15, right=0.95)

x = [1, 2]
y = [i*8 for i in x]

ux = [1, 2, 4, 8, 16, 24, 32]
uy = [i*12 for i in ux]

#uy = [i*2 for i in uy]

idx = np.arange(len(ux))
width = 0.28

plt.bar(np.arange(len(x)), y, width, label='RTL-SDR')
plt.bar(idx+width, uy, width, label='USRP')

plt.xticks(np.arange(len(ux))+width/2, ux)

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.xlabel('Sample Rate (MHz)')
plt.ylabel('Data Rate (Mbps)')

plt.legend()

plt.savefig('../../plots/datarateversussamplingrate.pdf')
plt.show()
