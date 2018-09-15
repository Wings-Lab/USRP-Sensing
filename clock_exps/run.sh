cpufreq-set -f 1536000
sleep 1
/usr/share/gnuradio/examples/uhd/usrp_spectrum_sense.py 915.3M 916.3M -s 1M > 1536_run1.txt
