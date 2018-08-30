import os
import numpy as np

data = []

files = ['100ms_run1.txt', '100ms_run3.txt', '100ms_run4.txt', '100ms_run5.txt', '100ms_run2.txt']
#files = ['10ms_run1.txt', '10ms_run3.txt', '10ms_run4.txt', '10ms_run2.txt', '10ms_run5.txt']

for f in files: 
    lines = open('usrp_fft/'+f, 'r')
    d1 = []
    for line in lines:
        line = line.strip().split(' ')
        d1.append(line[7])
    data.append(d1)

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
print counts, np.mean(counts)
