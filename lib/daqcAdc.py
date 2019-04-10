from tkinter import *
from lib.globals import *
from collections import deque
global hx

class daqcADC:
    last = 0.0;
    offset = 0
    
    def __init__(self,root,addr,channel,SCALE=1,RANGE_MIN=-15,RANGE_MAX=15):
        self.addr=addr
        self.root=root
        self.chan=channel
        self.scale=SCALE
        self.range_min = RANGE_MIN
        self.range_max = RANGE_MAX
        self.last = 0.0
        self.val=DoubleVar()
        self.val.set(DAQC.getADC(self.addr,self.chan))
        self.valstring=StringVar()
        self.valstring.set(str(self.val.get()))
        off=H-2-ADCHANNELS*SLICE+self.chan*SLICE
        BG='#DDDFFFFFF'
        self.CWidth=int(.75*W+20)
        self.a2df=Frame(self.root,bg=BG,bd=0,relief="ridge")
        self.a2df.place(x=0,y=off,width=W,height=SLICE)

        self.button1=Button(self.a2df, text='Tare', command=self.tare)
        self.button1.grid(row=0, column=0, padx=2,pady=2)

        self.a2dl = StringVar(root, value="A2D Channel "+str(self.chan)+":")
        self.a2dt = Label(self.a2df,textvariable=self.valstring,fg="Black",bg=BG,width=5).grid(row=0,column=2,sticky="w")
        self.a2dtxt=Entry(self.a2df,textvariable=self.a2dl,fg="Black",bg=BG,bd=0,relief="flat",width=12)
        self.a2dtxt.grid(row=0,column=1,sticky="w")
        self.a2dcanvas=Canvas(self.a2df,bg=BG,width=self.CWidth,height=SLICE,bd=0,relief="flat")
        self.a2dcanvas.grid(row=0,column=3,sticky="e")
        self.buffer = deque([], self.CWidth)

    def tare(self):
        sum = 0.0
        n = 25
        print("Tare in process")
        self.last = DAQC.getADC(self.addr,self.chan)
        for i in range(n):
            time.sleep(0.1)
            self.last = DAQC.getADC(self.addr,self.chan)
            sum = sum + float(self.last)
        self.offset = sum / n;
        print("Offset: ",self.offset)
        return self.offset

    def sample(self):
        self.last = (DAQC.getADC(self.addr,self.chan) - self.offset) / self.scale
        self.buffer.append(self.last)
        return self.last
        
    def update(self):
        self.val.set(self.last)
        self.valstring.set(str("{:5.1f}".format(self.last)))
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
        
    def plot(self):
        points = []
        i = 0
        for value in self.buffer:
            points.append(i)
            y = (self.range_max - value) / (self.range_max - self.range_min) * (SLICE-2)
            points.append(int(y))
            i = i+1
        if (len(points) > 4):
            self.a2dcanvas.delete("all")
            self.a2dcanvas.create_line(points, fill="#FF0000",width=2)
