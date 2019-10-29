from lib.globals import *
import time

class daqcButton:
    lastState = False
    bit = 0
    
    def __init__(self, bit):
        self.bit = bit
        self.lightOff()
        
    def wasPressed(self):
        state = DAQC.getDINbit(0,self.bit)
        if (self.lastState != state):
            self.lastState = state
            return not state
        else:
            return False
        
    def lightOn(self):
        DAQC.setDOUTbit(0,self.bit)

    def lightOff(self):
        DAQC.clrDOUTbit(0,self.bit)

        
    