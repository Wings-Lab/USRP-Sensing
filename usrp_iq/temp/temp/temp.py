import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':30})
matplotlib.rcParams['figure.figsize'] = 18, 10

data1 = np.loadtxt('10ms_run1_fft_temp3.txt')
data5 = np.loadtxt('10ms_run1_fft_temp4.txt')
data2 = np.loadtxt('temp2.txt')
data3 = np.loadtxt('temp3.txt')
data4 = np.loadtxt('temp4.txt')

plt.plot(data1, marker='*', label='mine-4096')
#plt.plot(data2, marker='^', label='yours-8192')
#plt.plot(data3, marker='o', label='yours-4096')
#plt.plot(data4, marker='o', label='yours-200000-4096')
plt.plot(data5, marker='o', label='yours')

plt.legend()

plt.show()
