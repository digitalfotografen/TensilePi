from tkinter import *
from lib.globals import *
from collections import deque
global hx

class daqcADC:
    last = 0.0;
    offset = 0
    min = 0
    max = 0
    
    def __init__(self,root,addr,channel,SCALE=1,RANGE_MIN=-15,RANGE_MAX=15,LABEL='A'):
        self.addr=addr
        self.root=root
        self.chan=channel
        self.scale=SCALE
        self.range_min = RANGE_MIN
        self.range_max = RANGE_MAX
        self.last = 0.0

        self.CWidth=int(.83*W+20)
        self.buffer = deque([], self.CWidth)

        self.minval=DoubleVar()
        self.maxval=DoubleVar()
        self.val=DoubleVar()

        off=H-2-ADCHANNELS*SLICE+self.chan*SLICE
        BG='#FFFFFFFFF'
        self.a2df=Frame(self.root,bg=BG,bd=1,relief="ridge")
        self.a2df.place(x=0,y=off,width=W,height=SLICE)

        self.button1=Button(self.a2df, text='0', command=self.tare)
        self.button1.grid(row=4, column=0, padx=2,pady=2)

        self.a2dl = StringVar(root, value=LABEL)
        self.a2dtxt=Label(self.a2df,textvariable=self.a2dl,fg="Black",bg=BG,bd=0,width=12,font="-weight bold")
        self.a2dtxt.grid(row=0,column=0,columnspan=2,sticky="w")
        self.a2dt = Label(self.a2df,textvariable=self.val,fg="Black",bg=BG,width=12,font="-weight bold")
        self.a2dt.grid(row=1,column=0,columnspan=2,sticky="w")

        self.a2minLabel=Label(self.a2df,text="Min",fg="Black",bg=BG,bd=0,width=5).grid(row=2,column=0,sticky="w")
        self.a2min = Label(self.a2df,textvariable=self.minval,fg="Black",bg=BG,width=5)
        self.a2min.grid(row=2,column=1)
        self.a2maxLabel=Label(self.a2df,text="Max",fg="Black",bg=BG,bd=0,width=5).grid(row=3,column=0,sticky="w")
        self.a2max = Label(self.a2df,textvariable=self.maxval,fg="Black",bg=BG,width=5)
        self.a2max.grid(row=3,column=1)

        self.a2dcanvas=Canvas(self.a2df,bg=BG,width=self.CWidth,height=SLICE,bd=0,relief="flat")
        self.a2dcanvas.grid(row=0,rowspan=5,column=2,sticky="e")

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
        self.min = 0.0
        self.max = 0.0
        return self.offset

    def sample(self):
        self.last = round((DAQC.getADC(self.addr,self.chan) - self.offset) / self.scale,5)
        self.buffer.append(self.last)
        if self.last < self.min:
            self.min = self.last
        if self.last > self.max:
            self.max = self.last
        return self.last
        
    def update(self):
        self.val.set(round(self.last,2))
        self.minval.set(round(self.min,2))
        self.maxval.set(round(self.max,2))
        self.plot()

    def getLabel(self):
        return self.a2dl.get()

    def setLabel(self,label):
        self.a2dl.set(label)        
        
    def plot(self):
        base = [0, self.yCoord(0), self.CWidth, self.yCoord(0)]
        points = []
        i = 0
        for value in self.buffer:
            points.append(i)
            y = self.yCoord(value)
            points.append(self.yCoord(value))
            i = i+1
        if (len(points) > 4):
            self.a2dcanvas.delete("all")
            self.a2dcanvas.create_line(base, fill="#000000",width=1)
            self.a2dcanvas.create_line(points, fill="#FF0000",width=2)

    def yCoord(self, value):
        return int((self.range_max - value) / (self.range_max - self.range_min) * (SLICE-2))
    