from tkinter import *
from lib.globals import *
import lib.HX711
from lib.HX711 import sensor
import time
import pigpio # http://abyz.co.uk/rpi/pigpio/python.html
from collections import deque

class daqcForce:
    offset = 0
    last = 0
    last_reading = 0
    min = 0
    max = 0
    
    def __init__(self, root, SCALE=1, DATA_PIN=20, SCLK_PIN=21,
                 RANGE_MIN = -1000, RANGE_MAX = 5000,
                 WIDTH=800, HEIGHT=150, Y=0, LABEL='F'):
        self.root=root
            
        pi = pigpio.pi()
        if not pi.connected:
            exit(0)

        self.sensor = sensor(
            pi, DATA=DATA_PIN, CLOCK=SCLK_PIN, mode=lib.HX711.CH_A_GAIN_64)
        self.scale = SCALE
        self.range_min = RANGE_MIN
        self.range_max = RANGE_MAX

        self.CWidth=int(.85*WIDTH)
        self.CHeight = HEIGHT
        self.buffer = deque([], self.CWidth)

        self.minval=DoubleVar()
        self.maxval=DoubleVar()
        self.val=DoubleVar()

        off=Y
        BG='#FFFFFFFFF'
        self.a2df=Frame(self.root,bg=BG,bd=1,relief="ridge")
        self.a2df.place(x=0,y=off,width=WIDTH,height=HEIGHT)
        
        self.button1=Button(self.a2df, text='0', command=self.tare)
        self.button1.grid(row=2, column=0, rowspan=2, padx=0,pady=0)

        self.a2dl = StringVar(root, value=LABEL)
        self.a2dtxt=Label(self.a2df,textvariable=self.a2dl,fg="Black",bg=BG,bd=0,width=12,font="-weight bold")
        self.a2dtxt.grid(row=0,column=0,columnspan=3,sticky="w")
        self.a2dt = Label(self.a2df,textvariable=self.val,fg="Black",bg=BG,width=12,font="-weight bold")
        self.a2dt.grid(row=1,column=0,columnspan=3,sticky="w")

        self.a2minLabel=Label(self.a2df,text="Min",fg="Black",bg=BG,bd=0,width=4).grid(row=2,column=1,sticky="w")
        self.a2min = Label(self.a2df,textvariable=self.minval,fg="Black",bg=BG,width=6)
        self.a2min.grid(row=3,column=2)
        self.a2maxLabel=Label(self.a2df,text="Max",fg="Black",bg=BG,bd=0,width=4).grid(row=3,column=1,sticky="w")
        self.a2max = Label(self.a2df,textvariable=self.maxval,fg="Black",bg=BG,width=6)
        self.a2max.grid(row=2,column=2)

        self.a2dcanvas=Canvas(self.a2df,bg=BG,width=self.CWidth,height=self.CHeight,bd=0,relief="flat")
        self.a2dcanvas.grid(row=0,rowspan=4,column=3,sticky="e")
        self.tare()
            
    def tare(self):
        sum = 0.0
        n = 25
        print("Tare in process")
        count, mode, self.last_reading = self.sensor.get_reading()
        if (self.last_reading == 0):
            time.sleep(1.0)
        for i in range(n):
            time.sleep(0.1)
            count, mode, self.last_reading = self.sensor.get_reading()
            sum = sum + float(self.last_reading)
        self.offset = sum / n;
        print("Offset: ",self.offset)
        self.min = 0.0
        self.max = 0.0
        return self.offset
        
    def sample(self):
        count, mode, reading = self.sensor.get_reading()
        if (abs(reading - self.last_reading) > 100000):
            count, mode, reading = self.sensor.get_reading()
            print("HX711 reading error")
        self.last_reading = reading
        self.last = round((self.offset - self.last_reading) / self.scale, 5)
        self.buffer.append(self.last)
        if self.last < self.min:
            self.min = self.last
        if self.last > self.max:
            self.max = self.last
        return self.last

    def update(self):
        self.val.set(int(self.last))
        self.minval.set(int(self.min))
        self.maxval.set(int(self.max))
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
            points.append(self.yCoord(value))
            i = i+1
        if (len(points) > 4):
            self.a2dcanvas.delete("all")
            self.a2dcanvas.create_line(base, fill="#000000",width=1)
            self.a2dcanvas.create_line(points, fill="#FF0000",width=2)

    def yCoord(self, value):
        return int((self.range_max - value) / (self.range_max - self.range_min) * (self.CHeight-2))
