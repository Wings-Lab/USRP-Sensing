import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':40})
matplotlib.rcParams['figure.figsize'] = 20, 10

fig = plt.figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.12, bottom=0.2, right=0.95)

s = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

ms = [30, 39, 58, 61, 63, 86, 88, 95, 98, 98]
us = [18, 32, 38, 54, 58, 76, 82, 87, 91, 96]

plt.plot(s, ms, linewidth=10, marker='s', markersize=28, markeredgecolor='black', label='1ms')
plt.plot(s, us, linewidth=10, marker='o', markersize=28, markeredgecolor='black', label='1us')

plt.ylabel('Detection Ratio (%)')
plt.xlabel('Number of Sensors')

plt.ylim([0, 100])

plt.grid(True, linestyle='--')

plt.legend()

plt.savefig('../../plots/fusion_static.pdf')

plt.show()

