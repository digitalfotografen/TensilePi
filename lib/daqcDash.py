from tkinter import *
from lib.singeltons import *
from lib.daqcAdc import daqcADC
#from lib.daqcDin import daqcDIN
from lib.daqcForce import daqcForce

class daqcDASH:
    def __init__(self,frame,addr):
        self.a2d=list(range(ADCHANNELS))
        #self.din=list(range(8))  
        self.force=list(range(8))
        
        def deSelect():
            for i in range(0,ADCHANNELS):
                self.a2d[i].deSelect()
                #self.din[i].deSelect()
                #self.force[i].deSelect()
                
        def selectAll():
            for i in range(0,ADCHANNELS):
                self.a2d[i].Select()
                #self.din[i].Select()
                #self.force[i].Select()
            
        self.addr=addr
        self.root=frame
        
        BG='#888FFF888'
        off=0
        self.mFrame=Frame(self.root,bg=BG,bd=0,relief="ridge")
        self.mFrame.place(x=0,y=off,width=W,height=SLICE+10)   
        self.button1=Button(self.mFrame, text='Clear All', command=deSelect)
        self.button1.grid(row=0, column=0, padx=4,pady=5)
        self.button2=Button(self.mFrame, text='Select All', command=selectAll)  
        self.button2.grid(row=0, column=1, padx=4,pady=5)
        
        self.a2d=list(range(ADCHANNELS))
        #self.din=list(range(8))  
        self.force=list(range(8))
        for i in range(0,ADCHANNELS):
            self.a2d[i]=daqcADC(self.root,self.addr,i)
            #self.din[i]=daqcDIN(self.root,self.addr,i)      
        #onlye one force channel
        self.force=list(range(8))
        self.force[0]=daqcForce(self.root, SCALE=600/9.81)
    
    def a2dsample(self):
        vals=['','','','','','','','']
        for i in range(0,ADCHANNELS):
            vals[i]=self.a2d[i].sample()
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
        vals=['','','','','','','','']
        #for i in range(1):
        vals[0]=self.force[0].sample()
        return vals

    def forceupdate(self):
        #for i in range(1):
        self.force[0].update()

    def a2dDescriptors(self):
        vals=['','','','','','','','']
        for i in range(0,ADCHANNELS):
            vals[i]=self.a2d[i].descriptors()
        return vals   
        
    '''
    def dinDescriptors(self):
        vals=['','','','','','','','']
        for i in range(0,8):    
            vals[i]=self.din[i].descriptors()
        return vals
    '''
        
    def forceDescriptors(self):
        vals=['','','','','','','','']
        #for i in range(0,8):    
        vals[0]=self.force[0].descriptors()
        return vals   
        
    def a2dGetLabels(self):
        vals=['','','','','','','','']
        for i in range(0,ADCHANNELS):
            vals[i]=self.a2d[i].getLabel()
        return vals   
        
    '''
    def dinGetLabels(self):
        vals=['','','','','','','','']
        for i in range(0,8):    
            vals[i]=self.din[i].getLabel()
        return vals
    '''

    def forceGetLabels(self):
        vals=['','','','','','','','']
        #for i in range(0,8):    
        vals[0]=self.force[0].getLabel()
        return vals   

    def a2dGetStates(self):
        vals=['','','','','','','','']
        for i in range(0,ADCHANNELS):
            vals[i]=self.a2d[i].getState()
        return vals   
        
    '''
    def dinGetStates(self):
        vals=['','','','','','','','']
        for i in range(0,8):    
            vals[i]=self.din[i].getState()
        return vals
    '''

    def forceGetStates(self):
        vals=['','','','','','','','']
        #for i in range(0,8):    
        vals[0]=self.force[0].getState()
        return vals     

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
