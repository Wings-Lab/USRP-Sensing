cpufreq-set -f 1296000
sleep 1
/usr/share/gnuradio/examples/uhd/usrp_spectrum_sense.py 915.3M 916.3M -s 1M --fft-size 256 > usrp_1_1296.txt
