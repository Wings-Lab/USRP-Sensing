import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':40})
matplotlib.rcParams['figure.figsize'] = 18, 10

x = [1, 2, 4]
y = [4, 8, 16]

ux = [1, 2, 4, 8, 16, 24, 32]
uy = [4, 8, 16, 32, 64, 96, 128]

uy = [i*2 for i in uy]

idx = np.arange(len(ux))
width = 0.28

plt.bar(idx, uy, width, label='USRP')
plt.bar(np.arange(len(x))+width, y, width, label='RTL-SDR')

plt.xticks(np.arange(len(ux))+width/2, ux)

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')

plt.xlabel('Sample Rate (MHz)')
plt.ylabel('Data Rate (Mbps)')

plt.legend()

plt.savefig('../plots/datarateversussamplingrate.pdf')
plt.show()
