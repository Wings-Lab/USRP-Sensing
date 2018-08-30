import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':30})
matplotlib.rcParams['figure.figsize'] = 18, 10

def getData(files):
    data = []
    for f in files: 
        lines = open('usrp_fft/'+f, 'r')
        d1 = []
        for line in lines:
            line = line.strip().split(' ')
            d1.append(line[7])
        data.append(d1)
    return data

def countTx(data):
    th = -70
    counts = []
    for d in data:
        count = 0
        low = 1
        for i in d:
            if float(i) > th and low == 1:
                count += 1
                low = 0
            if float(i) < th:
               low = 1
        counts.append(count)
    return counts

files1 = ['100ms_run1.txt', '100ms_run3.txt', '100ms_run4.txt', '100ms_run5.txt', '100ms_run2.txt']
files2 = ['10ms_run1.txt', '10ms_run3.txt', '10ms_run4.txt', '10ms_run2.txt', '10ms_run5.txt']
files3 = ['1ms_run1.txt', '1ms_run3.txt', '1ms_run4.txt', '1ms_run2.txt', '1ms_run5.txt']
files4 = ['1us_run1.txt', '1us_run3.txt', '1us_run4.txt', '1us_run2.txt', '1us_run5.txt']

data = getData(files1)
counts1 = countTx(data)
data = getData(files2)
counts2 = countTx(data)
data = getData(files3)
counts3 = countTx(data)
data = getData(files4)
counts4 = countTx(data)

print counts1, np.mean(counts1)
print counts2, np.mean(counts2)
print counts3, np.mean(counts3)
print counts4, np.mean(counts4)

tx = [100, np.mean(counts1), np.mean(counts2), np.mean(counts3), np.mean(counts4)]
tx = [i for i in reversed(tx)]
idx = np.arange(len(tx))
width = 0.3

plt.bar(idx, tx, width)

plt.ylim([0, 100])
plt.xlabel('Transmission Length (ms)')
plt.ylabel('Detection Ratio')
plt.xticks(np.arange(len(tx)), [0.001, 1, 10, 100, 1000])

plt.show()
