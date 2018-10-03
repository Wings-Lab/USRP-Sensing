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
y = [100, 99.7, 99, 77.3, 55.7, 18.1, 9.9, 6.5]

idx = np.arange(len(x))
width = 0.28

plt.bar(idx, y, width)

plt.xticks(np.arange(len(x)), x)

ax = plt.gca()
ax.yaxis.grid(linestyle='dotted')
#plt.ylim([0, 2])

plt.xlabel('Batch Size (Bytes)')
plt.ylabel('Samples Received (%)')

plt.savefig('../plots/netstack_samples_received.pdf')
plt.show()
