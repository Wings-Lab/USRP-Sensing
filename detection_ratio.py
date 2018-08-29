import numpy as np

d1 = []
d2 = []

lines = open('1sec_tx.txt', 'r')
for line in lines:
    line = line.strip().split(' ')
    d1.append(line[7])
lines = open('100ms_tx.txt', 'r')
for line in lines:
    line = line.strip().split(' ')
    d2.append(line[7])

count = 0
prev = 0
th = -70
low = 1
for i in d2:
    if float(i) > th and low == 1:
        count += 1
        low = 0
    if float(i) < th:
       low = 1
print count
