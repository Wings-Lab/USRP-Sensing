cpufreq-set -f 10000000
sleep 1
/usr/share/gnuradio/examples/uhd/usrp_spectrum_sense.py 915.3M 916.3M -s 1M > 100_run6.txt
