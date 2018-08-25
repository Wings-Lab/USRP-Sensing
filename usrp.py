'''
Created on Mar 1, 2016

@author: ayon
'''

import scipy
import pylab
import time
import numpy as np 
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import statistics
import os
import time
from functools import wraps

PROF_DATA = {}

def profile(fn):
    @wraps(fn)
    def with_profiling(*args, **kwargs):
        start_time = time.time()

        ret = fn(*args, **kwargs)

        elapsed_time = time.time() - start_time

        if fn.__name__ not in PROF_DATA:
            PROF_DATA[fn.__name__] = [0, []]
        PROF_DATA[fn.__name__][0] += 1
        PROF_DATA[fn.__name__][1].append(elapsed_time)

        return ret

    return with_profiling

def print_prof_data():
    for fname, data in PROF_DATA.items():
        max_time = max(data[1])
        avg_time = sum(data[1]) / len(data[1])
        print "Function %s called %d times. " % (fname, data[0]),
        print 'Execution time max: %.3f, average: %.3f' % (max_time, avg_time)

def clear_prof_data():
    global PROF_DATA
    PROF_DATA = {}

class Utilities:
    
    def totalpower(self, psd):
        # s = 0.0
        # for p in psd:
        #     s += -10*np.log10(p/10.0) #i know averaging db is wrong here, deliberately doing it
        # return -s/len(psd) #-10*np.log10(s)
        avg_psd_dB =  10*np.log10(np.average(psd)/10.0)
        return avg_psd_dB
    @profile
    def plot_fft(self, reals, imags, timea, sample_rate, fc, NFFT, myfile):
        M = len(reals)/NFFT
        
        # Open a file
        text_file = open(myfile+"_energyfft.txt", "w")

        for i in range(0,int(M)):
            iq_samples = np.array([ (re + 1j*co) for re,co in zip(reals,imags)])[i*NFFT:(i+1)*NFFT]
            x = pylab.psd(iq_samples, NFFT=NFFT, Fs=sample_rate/1e6, Fc=fc, window=mlab.window_hanning)      
            totalpower = self.totalpower(x[0])
            print myfile, i, totalpower
            text_file.write("%s\n" % totalpower)
            text_file.flush()
	    #pylab.show()
	    pylab.close()
            
        text_file.close()        


class USRP_IQ_analysis:
    
    def __init__(self, iqfile, datatype, block_length, block_offset, sample_rate):
        self.iqfile = iqfile
        self.datatype = datatype
        self.sizeof_data = self.datatype.nbytes    # number of bytes per sample in file
        self.block_length = block_length
        self.sample_rate = sample_rate
        self.block_offset = block_offset
        self.binary_offset = self.block_offset*scipy.dtype(self.datatype).itemsize
        
    def read_samples(self):
        hfile = open(self.iqfile, "r")
        hfile.seek(self.binary_offset, os.SEEK_SET)  # seek
        try:
            iq = scipy.fromfile(hfile, dtype=self.datatype, count=self.block_length)
        except MemoryError:
            print "End of File"
        else:
            reals = scipy.array([ (r.real)  for r in iq])
            imags = scipy.array([ (i.imag)  for i in iq])
            time = scipy.array([i*(1/self.sample_rate) for i in range(len(reals))])
        hfile.close()
        return reals,imags,time
             
             
# class RTL_IQ_analysis:
#     
#     def __init__(self, iqfile, datatype, block_length, sample_rate):
#         self.iqfile = iqfile
#         self.datatype = datatype
#         self.sizeof_data = self.datatype.nbytes    # number of bytes per sample in file
#         self.block_length = block_length
#         self.sample_rate = sample_rate
#         
#     def read_samples(self):
#         hfile = open(self.iqfile, "rb")
#         try:
#             iq = scipy.fromfile(hfile, dtype=self.datatype, count=self.block_length)
#         except MemoryError:
#             print("End of File")
#         else:
#             reals = scipy.array([ (r) for index,r in enumerate(iq) if index%4 == 0])
#             imags = scipy.array([ (i) for index,i in enumerate(iq) if index%4 == 1])
#             timea = scipy.array([i*(1/self.sample_rate) for i in range(len(reals))])
#         
#         hfile.close()
#         return reals,imags,timea
    

vals = []
datatype = scipy.complex64
block_length = 10000 #-1
block_offset = 500000 #<---change to random offsets between 0 to (max_no_of_iq_samples - block_length)
#block_offset =
sample_rate = 1e6
fc = 2462
NFFT = 1024
for myfile in ['usrp_far_2462','usrp_nearby_2462','usrp_noise_2462']:
    filename = myfile+".dat"
    print "processing file:"+filename
    usrp = USRP_IQ_analysis(filename, datatype, block_length, block_offset, sample_rate)
    r,i,t = usrp.read_samples()
    utils = Utilities()
    #print r
    vals.append( utils.plot_fft(r,i,t,sample_rate,fc, NFFT, myfile) )

    with open(myfile+"_energyfft.txt","r") as f:
        numbers = []
        for line in f:
            numbers.append(float(line))
        numbers.sort()
    print(statistics.median(map(float, numbers)))
    f.close()
    print_prof_data()
