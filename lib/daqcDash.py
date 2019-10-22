from tkinter import *
from lib.globals import *
from lib.daqcAdc import daqcADC
#from lib.daqcDin import daqcDIN
from lib.daqcForce import daqcForce

class daqcDASH:
    def __init__(self,frame,addr):
        self.a2d=list(range(ADCHANNELS))
        #self.din=list(range(8))  
        self.force=list(range(8))
        
        self.addr=addr
        self.root=frame
        self.a2d=list(range(ADCHANNELS))
        #self.din=list(range(8))  
        self.force=list(range(8))
        for i in range(0,ADCHANNELS):
            section='ADC'+str(i)
            label = config.get(section, 'label', fallback=section)
            scale = config.getfloat(section,'scale',fallback=1.0)
            offset = config.getfloat(section,'offset',fallback=0.0)
            range_min = config.getfloat(section,'range_min',fallback=-12.0)
            range_max = config.getfloat(section,'range_max',fallback=12.0)
            self.a2d[i] = daqcADC(self.root,
                                  self.addr,
                                  i,
                                  SCALE=scale,
                                  RANGE_MIN=range_min,
                                  RANGE_MAX=range_max,
                                  LABEL=label,
                                  OFFSET=offset)
            #self.din[i]=daqcDIN(self.root,self.addr,i)      
        #onlye one force channel
        self.force=list(range(8))
        print(config.getfloat('F1','scale',fallback=1))
        label = config.get('F1','label',fallback='F1')
        scale = config.getfloat('F1','scale',fallback=1.0)
        range_min = config.getfloat('F1','range_min',fallback=-12.0)
        range_max = config.getfloat('F1','range_max',fallback=12.0)
        self.force[0]=daqcForce(self.root,SCALE=scale,RANGE_MIN=range_min,RANGE_MAX=range_max,LABEL=label)
    
    def tare(self):
        self.force[0].tare()
        for i in range(0,ADCHANNELS):
            self.a2d[i].tare()
        return

    def a2dsample(self):
        vals=[]
        for i in range(0,ADCHANNELS):
            vals.append(self.a2d[i].sample())
        return vals

    def a2dupdate(self):
        for i in range(0,ADCHANNELS):
            self.a2d[i].update()

    '''
    def dinupdate(self):
        vals=['','','','','','','','']
        for i in range(0,8):          
            vals[i]=self.din[i].update()
        return vals
    '''

    def forcesample(self):
        return [self.force[0].sample()]

    def forceupdate(self):
        #for i in range(1):
        self.force[0].update()

    def a2dGetLabels(self):
        labels = []
        for i in range(0,ADCHANNELS):
            labels.append(self.a2d[i].getLabel())
        return labels  
        
    '''
    def dinGetLabels(self):
        vals=['','','','','','','','']
        for i in range(0,8):    
            vals[i]=self.din[i].getLabel()
        return vals
    '''

    def forceGetLabels(self):
        return [self.force[0].getLabel()]   

    def a2dSetLabels(self,labels):
        self.vals=labels
        for i in range(0,ADCHANNELS):
            self.a2d[i].setLabel(self.vals[i])
        return   
        
    '''
    def dinSetLabels(self,labels):
        self.vals=labels
        for i in range(0,8):    
            self.din[i].setLabel(self.vals[i])
        return
    '''

    def forceSetLabels(self,labels):
        self.vals=labels
        #for i in range(0,8):    
        self.force[0].setLabel(self.vals[0])
        return   

    def a2dSetStates(self,states):
        self.vals=states
        for i in range(0,ADCHANNELS):
            self.a2d[i].setState(self.vals[i])
        return   
        
    '''
    def dinSetStates(self,states):
        self.vals=states
        for i in range(0,8):    
            self.din[i].setState(self.vals[i])
        return
    '''

    def forceSetStates(self,states):
        self.vals=states
        #for i in range(0,8):    
        self.force[0].setState(self.vals[0])
        return    
