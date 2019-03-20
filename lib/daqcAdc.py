from tkinter import *
from lib.singeltons import *
from collections import deque
global hx

class daqcADC:
    last = 0.0;
    
    def __init__(self,root,addr,channel):
        self.addr=addr
        self.root=root
        self.chan=channel
        self.last = 0.0
        self.var=IntVar()   #This is the select button for each channel
        self.var.set(1)
        self.val=DoubleVar()
        self.val.set(DAQC.getADC(self.addr,self.chan))
        self.valstring=StringVar()
        self.valstring.set(str(self.val.get()))
        off=H-2-ADCHANNELS*SLICE+self.chan*SLICE
        BG='#DDDFFFFFF'
        self.CWidth=int(.75*W+20)
        self.a2df=Frame(self.root,bg=BG,bd=0,relief="ridge")
        self.a2df.place(x=0,y=off,width=W,height=SLICE)
        self.a2dc=Checkbutton(self.a2df,fg="Black",bg=BG,variable=self.var,onvalue = 1, offvalue = 0,command=self.cb)
        self.a2dc.grid(row=0,column=0,sticky="w")
        self.var.set(1)
        self.a2dl = StringVar(root, value="A2D Channel "+str(self.chan)+":")
        self.a2dt = Label(self.a2df,textvariable=self.valstring,fg="Black",bg=BG,width=5).grid(row=0,column=2,sticky="w")
        self.a2dtxt=Entry(self.a2df,textvariable=self.a2dl,fg="Black",bg=BG,bd=0,relief="flat",width=12)
        self.a2dtxt.grid(row=0,column=1,sticky="w")
        self.a2dcanvas=Canvas(self.a2df,bg=BG,width=self.CWidth,height=SLICE,bd=0,relief="flat")
        self.a2dcanvas.grid(row=0,column=3,sticky="e")
        self.buffer = deque([], self.CWidth)

    def cb(self):
        if (self.var==1):
            a=1
            
    def deSelect(self):
        self.a2dc.deselect()

    def Select(self):
        self.a2dc.select() 
        
    def sample(self):
        if (self.var.get()==1):
            self.last = DAQC.getADC(self.addr,self.chan)
            self.buffer.append(self.last)
            return self.last
        else:
            return ''
        
    def update(self):
        if (self.var.get()==1):
            self.val.set(self.last)
            self.valstring.set(str("{:5.3f}".format(self.last)))
            self.plot()

    def descriptors(self):
        if (self.var.get()==1):
            return self.a2dl.get()
        else:
            return ''

    def getLabel(self):
        return self.a2dl.get()

    def setLabel(self,label):
        self.a2dl.set(label)        
        
    def getState(self):
        return self.var.get()        
 
    def setState(self,state):
        if (state=='1'):
            self.a2dc.select()
        else:
            self.a2dc.deselect()
            
    def plot(self):
        points = []
        i = 0
        for value in self.buffer:
            points.append(i)
            y = (12.0-value) / 24 * (SLICE-2)
            points.append(int(y))
            i = i+1
        self.a2dcanvas.delete("all")
        self.a2dcanvas.create_line(points, fill="#FF0000",width=2)
