import os
import pylab
import scipy
import statistics
import numpy as np
import matplotlib.mlab as mlab
from matplotlib import cm

class utilities:
    def __init__(self):
        self.total_i = 0
    def total_power(self, psd):
        avg_psd_db = 10*np.log10(np.average(psd)/10.0)
        return avg_psd_db

    def plot_fft(self, reals, imags, time, sample_rate, fc, nfft, tfile):
        m = len(reals)/nfft
        dfs = []
        for i in range(0, int(m)):
            iqs = np.array([(re+1j*co) for re, co in zip(reals, imags)])[i*nfft:(i+1)*nfft]
            x = pylab.psd(iqs, NFFT=nfft, Fs=sample_rate/1e6, Fc=fc, window=mlab.window_hanning)
            total_power = self.total_power(x[0])
            y = list(10*np.log10(x[0]))
            dfs.append(y)
            self.total_i += 1
            #print(myfile, self.total_i, total_power)
            tfile.write("%s\t"%(self.total_i))
            tfile.write("%s\n"%total_power)
            tfile.flush()
            pylab.close()
        #print(dfs)
        #xy = pylab.imshow(dfs,interpolation='sinc', cmap=cm.afmhot)
        #pylab.savefig("heatmap.pdf")
        #temp = open("temp_file.txt","w")
        #temp.write("%s\n"%dfs)

class usrp_iq_analysis:
    def __init__(self, iqfile, sample_rate, block_length, binary_offset):
        self.iqfile = iqfile
        self.sample_rate = sample_rate
        self.block_length = block_length
        self.binary_offset = binary_offset

    def read_samples(self, hfile, binary_offset):
        hfile.seek(binary_offset, os.SEEK_SET)  #why?
        try:
            iqs = scipy.fromfile(hfile, dtype=scipy.complex64, count=self.block_length)
        except MemoryError:
            print("Memory Error")
        else:
            reals = scipy.array([(r.real) for r in iqs])
            imags = scipy.array([(i.imag) for i in iqs])
            time = scipy.array([i*(1/self.sample_rate) for i in range(len(reals))])
        #print(len(reals))
        return reals, imags, time

vals = []
nfft = 1024
fc = 2437
sample_rate = 6e6
bl = [100000]
runs = [100000, 200000, 300000, 400000, 500000]
for myfile in ['sensing-2437.dat']:
    for block_length in bl:
        for run in runs:
            block_offset = 1000
            binary_offset = block_offset*scipy.dtype(scipy.complex64).itemsize
            hfile = open(myfile, "r")
            old_file_position = hfile.tell()
            hfile.seek(0, os.SEEK_END)
            size = hfile.tell()
            hfile.seek(old_file_position, os.SEEK_SET)
            iqa = usrp_iq_analysis(myfile, sample_rate, block_length, binary_offset)
            print(size)
            size -= binary_offset
            utils = utilities()
            tfile = open(myfile+str(block_length)+"fft"+str(run)+".txt","w")
            while size > 0:
                r, i, t = iqa.read_samples(hfile, binary_offset)
                vals.append(utils.plot_fft(r,i,t,sample_rate,fc,nfft,tfile))
                block_offset += run
                binary_offset = block_offset*scipy.dtype(scipy.complex64).itemsize
                size -= binary_offset
                print(size)
            hfile.close()
            tfile.close()
