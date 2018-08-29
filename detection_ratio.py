import numpy as np

d1 = []
d2 = []

lines = open('1sec_tx.txt', 'r')
for line in lines:
    line = line.strip().split(' ')
    d1.append(line[7])
lines = open('10ms_tx.txt', 'r')
for line in lines:
    line = line.strip().split(' ')
    d2.append(line[7])

count = 0
prev = 0
for i in d1:
    if float(i) > -80:
        count += 1
        prev = i
print count
