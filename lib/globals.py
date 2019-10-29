#singeltons and globals
import sys
import time

import configparser
config = configparser.ConfigParser()
config.read('/home/pi/TensilePi/config.ini') # Uggly hardcoded path
print(config.sections())

try:
    import piplates.DAQC2plate as DAQC
except ImportError:
    print("error importingh piplates.DAQC2plate")
    os.system("lxterminal -e 'python py23install.py'")
    sys.exit()

W = config.getint('GUI', 'W', fallback=1000)
H = config.getint('GUI', 'H', fallback=800)

ADCHANNELS = config.getint('ADC', 'channels', fallback=3)
FCHANNELS = config.getint('Force', 'channels', fallback=1)
