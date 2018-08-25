import os
import pylab
import scipy
import statistics
import numpy as np
import matplotlib.mlab as mlab
from matplotlib import cm

class utilities:
    def total_power(self, psd):
        avg_psd_db = 10*np.log10(np.average(psd)/10.0)
        return avg_psd_db

    def plot_fft(self, reals, imags, time, sample_rate, fc, nfft, myfile):
        m = len(reals)/nfft
        print(m)
        dfs = []
        tfile = open(myfile+"fft.txt","w")
        for i in range(0, int(m)):
            iqs = np.array([(re+1j*co) for re, co in zip(reals, imags)])[i*nfft:(i+1)*nfft]
            x = pylab.psd(iqs, NFFT=nfft, Fs=sample_rate/1e6, Fc=fc, window=mlab.window_hanning)
            total_power = self.total_power(x[0])
            y = list(10*np.log10(x[0]))
            dfs.append(y)
            #print(myfile, i, total_power)
            tfile.write("%s\n" % total_power)
            tfile.flush()
            pylab.close()
        #print(dfs)
        xy = pylab.imshow(dfs,interpolation='sinc', cmap=cm.afmhot)
        pylab.savefig("heatmap.pdf")
        temp = open("temp_file.txt","w")
        temp.write("%s\n"%dfs)
        tfile.close()

class usrp_iq_analysis:
    def __init__(self, iqfile, sample_rate, block_length, binary_offset):
        self.iqfile = iqfile
        self.sample_rate = sample_rate
        self.block_length = block_length
        self.binary_offset = binary_offset

    def read_samples(self):
        hfile = open(self.iqfile, "r")
        hfile.seek(self.binary_offset, os.SEEK_SET)  #why?
        try:
            iqs = scipy.fromfile(hfile, dtype=scipy.complex64, count=self.block_length)
            print(len(iqs))
        except MemoryError:
            print("Memory Error")
        else:
            reals = scipy.array([(r.real) for r in iqs])
            imags = scipy.array([(i.imag) for i in iqs])
            time = scipy.array([i*(1/self.sample_rate) for i in range(len(reals))])
        hfile.close()
        return reals, imags, time

vals = []
nfft = 1024
fc = 2.437e9
sample_rate = 8e6
block_length = 20000 #why?
block_offset = 500000 #why?
binary_offset = block_offset*scipy.dtype(scipy.complex64).itemsize #why?
for myfile in ['sensing-2437.dat']:
    iqa = usrp_iq_analysis(myfile, sample_rate, block_length, binary_offset)
    r, i, t = iqa.read_samples()
    utils = utilities()
    vals.append(utils.plot_fft(r,i,t,sample_rate,fc,nfft,myfile))
    with open(myfile+"fft.txt", "r") as f:
        numbers = []
        for line in f:
            numbers.append(float(line))
        numbers.sort()
    print(statistics.median(map(float, numbers)))
    f.close()
