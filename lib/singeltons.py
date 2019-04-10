#singeltons and globals
import sys
import time
#import RPi.GPIO as GPIO
#from lib.hx711py3.scale import Scale
#from lib.hx711py3.hx711 import HX711

# choose pins on rpi (BCM5 and BCM6)
#hx = HX711(dout=5, pd_sck=6)

try:
    import piplates.DAQC2plate as DAQC
except ImportError:
    print("error importingh piplates.DAQC2plate")
    os.system("lxterminal -e 'python py23install.py'")
    sys.exit()

W=1000
H=800
#SLICE=33
SLICE=190

ADCHANNELS = 3 #number of analog input channels
FCHANNELS = 1 # numbder of force input channels, 
