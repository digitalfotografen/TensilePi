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
    
    def __init__(self, root, SCALE=1, DATA_PIN=20, SCLK_PIN=21, RANGE_MIN = -1000, RANGE_MAX = 5000, LABEL='F'):
        self.root=root
            
        pi = pigpio.pi()
        if not pi.connected:
            exit(0)

        self.sensor = sensor(
            pi, DATA=DATA_PIN, CLOCK=SCLK_PIN, mode=lib.HX711.CH_A_GAIN_64)
        self.scale = SCALE
        self.range_min = RANGE_MIN
        self.range_max = RANGE_MAX
        self.tare()

        self.CWidth=int(.75*W+20)
        self.buffer = deque([], self.CWidth)

        self.val=DoubleVar()
        self.val.set(self.sample())
        self.valstring=StringVar()
        self.valstring.set(str(self.val.get()))
        off=H-2-(ADCHANNELS+FCHANNELS)*SLICE
        BG='#DDDFFFFFF'
        self.a2df=Frame(self.root,bg=BG,bd=0,relief="ridge")
        self.a2df.place(x=0,y=off,width=W,height=SLICE)
        
        self.button1=Button(self.a2df, text='0', command=self.tare)
        self.button1.grid(row=0, column=0, padx=2,pady=2)

        self.a2dl = StringVar(root, value=LABEL)
        self.a2dt = Label(self.a2df,textvariable=self.valstring,fg="Black",bg=BG,width=11).grid(row=0,column=2,sticky="w")
        self.a2dtxt=Entry(self.a2df,textvariable=self.a2dl,fg="Black",bg=BG,bd=0,relief="flat",width=6)
        self.a2dtxt.grid(row=0,column=1,sticky="w")
        self.a2dcanvas=Canvas(self.a2df,bg=BG,width=self.CWidth,height=SLICE,bd=0,relief="flat")
        self.a2dcanvas.grid(row=0,column=3,sticky="e")
            
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
        return self.offset
        
    def sample(self):
        count, mode, reading = self.sensor.get_reading()
        if (abs(reading - self.last_reading) < 1000000):
            self.last_reading = reading
            self.last = (self.offset - self.last_reading) / self.scale
        else:
            print("HX711 reading error")
        self.buffer.append(self.last)
        return self.last

    def update(self):
        self.val.set(self.last)
        self.valstring.set(str("{:5.1f}".format(self.last)))
        self.plot()

    def descriptors(self):
        return self.a2dl.get()

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
