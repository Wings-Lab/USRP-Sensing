import os
import time
import numpy as np
from subprocess import Popen

srates = ['2M', '4M', '6M', '8M', '16M']

p = Popen(['ssh', 'wings@130.245.75.47', 'cd USRP-Sensing && python transmitter.py'])
