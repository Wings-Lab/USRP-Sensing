import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':40})
matplotlib.rcParams['figure.figsize'] = 20, 10


fig = plt.figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.1, bottom=0.15, right=0.99)

x = ['32K', '64K', '128K', '256K', '512K', '1M', '2M', '4M']
y = [0.24, 0.48, 0.92, 1.37, 1.86, 0.95, 0.77, 0.67]

y = [i*3 for i in y]

idx = np.arange(len(x))
width = 0.28

plt.bar(idx, y, width)

plt.xticks(np.arange(len(x)), x)

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')
plt.ylim([0, 6])

plt.xlabel('Batch Size (Bytes)')
plt.ylabel('Data Rate (Mbps)')

plt.savefig('../plots/netstack_datarate.pdf')
plt.show()
