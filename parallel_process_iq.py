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
import os
import time
from functools import wraps
from joblib import Parallel, delayed
import multiprocessing as mp

PROF_DATA = {}

def Run_fft_one_instance(r,i,t,sample_rate,fc, NFFT, myfile):
	# tfile = open(myfile[:-4]+'_fft.txt', 'a')
	powers = utils.plot_fft(r,i,t,sample_rate,fc, NFFT)
	# print(t[0])
	return powers

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
		#print "Function %s called %d times. " % (fname, data[0]),
		#print 'Execution time max: %.3f, average: %.3f' % (max_time, avg_time)

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
		#avg_psd_dB =  10*np.log10(np.sum(psd)/10.0)
		return avg_psd_dB
	@profile
	def plot_fft(self, reals, imags, timea, sample_rate, fc, NFFT):
		M = len(reals)/NFFT
		my_array =[]
		for i in range(0,int(M)):
			iq_samples = np.array([ (re + 1j*co) for re,co in zip(reals,imags)])[i*NFFT:(i+1)*NFFT]
			x = pylab.psd(iq_samples, NFFT=NFFT, Fs=sample_rate/1e6, Fc=fc, window=mlab.window_hanning)
			totalpower = self.totalpower(x[0])
			my_array.append(totalpower)
			#print i, totalpower
			# myfile.write("%s\n" % totalpower)
			# myfile.flush()
		pylab.close()
		return my_array
class USRP_IQ_analysis:
	
	def __init__(self, iqfile, datatype, block_length, block_offset, sample_rate, binary_offset):
		self.iqfile = iqfile
		self.datatype = datatype
		self.sizeof_data = self.datatype.nbytes    # number of bytes per sample in file
		self.block_length = block_length
		self.sample_rate = sample_rate
		self.block_offset = block_offset
		self.binary_offset = binary_offset #self.block_offset*scipy.dtype(self.datatype).itemsize
		
	def read_samples(self, hfile, binary_offset):
		hfile.seek(binary_offset, os.SEEK_SET)  # seek
		try:
			iq = scipy.fromfile(hfile, dtype=self.datatype, count=self.block_length)
		except MemoryError:
			print "End of File"
		else:
			reals = scipy.array([ (r.real)  for r in iq])
			imags = scipy.array([ (i.imag)  for i in iq])
			time = scipy.array([i*(1/self.sample_rate) for i in range(len(reals))])
		return reals,imags,time
			 
vals = []
datatype = scipy.complex64
sample_rate = 1e6
fc = 915.8e6
NFFT = 256
block_length = 100000

for myfile in ['4m_run1.dat', '4m_run2.dat', '4m_run3.dat', '4m_run4.dat', '4m_run5.dat']:
	print myfile
	block_offset = 100
	binary_offset = block_offset*scipy.dtype(scipy.complex64).itemsize
	hfile = open(myfile, "r")
	old_file_position = hfile.tell()
	hfile.seek(0, os.SEEK_END)
	size = hfile.tell()
	hfile.seek(old_file_position, os.SEEK_SET)
	usrp = USRP_IQ_analysis(myfile, datatype, block_length, block_offset, sample_rate, binary_offset)
	print size
	size -= binary_offset
	utils = Utilities()
	# print('-------->', size/(block_length*scipy.dtype(scipy.complex64).itemsize))
	IQ_data = []
	t_count = 0
	while size > 0:
		r,i,t = usrp.read_samples(hfile, binary_offset)
		IQ_data.append([r,i,t])
		# vals.append( utils.plot_fft(r,i,t,sample_rate,fc, NFFT, tfile))
		block_offset += block_length
		binary_offset = block_offset*scipy.dtype(scipy.complex64).itemsize
		size -= block_length*scipy.dtype(scipy.complex64).itemsize
		t_count = t_count+1
		# print size
	hfile.close()

	towrite = []
	# print('------------->', len(IQ_data))
	print("starting multiprocessing")
	towrite= Parallel(n_jobs = mp.cpu_count()-8 )(delayed(Run_fft_one_instance)(i[0],i[1],i[2],sample_rate,fc, NFFT, myfile) for i in IQ_data)
	tfile = open(myfile[:-4]+'_fft.txt', 'a')
	for  i in towrite:
		for j in i:
			tfile.write("%s\n"%str(j))
	tfile.close()
