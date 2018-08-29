import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size':30})
matplotlib.rcParams['figure.figsize'] = 18, 10

f = plt.figure()

def cdf(data, Colour, Label):
    global f
    data_size=len(data)

    # Set bins edges
    data_set=sorted(set(data))
    bins=np.append(data_set, data_set[-1]+1)

    # Use the histogram function to bin the data
    counts, bin_edges = np.histogram(data, bins=bins, density=False)

    counts=counts.astype(float)/data_size

    # Find the cdf
    cdf = np.cumsum(counts)

    # Plot the cdf
    plt.plot(bin_edges[0:-1], cdf, color=Colour, linewidth=5, label=Label)
    plt.ylim((0,1))
    plt.ylabel("CDF")
    plt.xlabel("Power")
    #plt.grid(True)
    plt.legend(loc='lower right')
    f.savefig("noise-cdf.pdf")


data = np.loadtxt('1.dat')
data2 = np.loadtxt('2.dat')
data3 = np.loadtxt('4.dat')
data4 = np.loadtxt('8.dat')
data5 = np.loadtxt('16.dat')
data6 = np.loadtxt('32.dat')
cdf(data, 'b', '1')
cdf(data2, 'r', '2')
cdf(data3, 'g', '4')
cdf(data4, 'c', '8')
cdf(data5, 'm', '16')
cdf(data6, 'y', '32')
plt.show()
