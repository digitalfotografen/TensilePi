#singeltons and globals
import sys
import time
import RPi.GPIO as GPIO
from lib.hx711py3.scale import Scale
from lib.hx711py3.hx711 import HX711

# choose pins on rpi (BCM5 and BCM6)
hx = HX711(dout=5, pd_sck=6)

import piplates.DAQC2plate as DAQC

W=800
H=600
SLICE=33
#SLICE=35
