from tkinter import *
from lib.singeltons import *
global hx

class daqcADC:
    def __init__(self,root,addr,channel):
        self.addr=addr
        self.root=root
        self.chan=channel
        self.var=IntVar()   #This is the select button for each channel
        self.var.set(1)
        self.val=DoubleVar()
        self.val.set(DAQC.getADC(self.addr,self.chan))
        self.valstring=StringVar()
        self.valstring.set(str(self.val.get()))
        off=H-2-17*SLICE+self.chan*SLICE
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
        self.maxrange=self.CWidth
        self.log=list(range(self.maxrange))
        for i in range(self.maxrange):
            self.log[i]=0.0
        self.nextPtr=0
        
    def cb(self):
        if (self.var==1):
            a=1
            
    def deSelect(self):
        self.a2dc.deselect()

    def Select(self):
        self.a2dc.select() 
        
    def update(self):
        if (self.var.get()==1):
            self.val.set(DAQC.getADC(self.addr,self.chan))
            self.valstring.set(str("{:5.3f}".format(self.val.get())))
            self.log[self.nextPtr]=self.val.get()
            self.nextPtr=(self.nextPtr+1)%self.maxrange
            #self.plot()
            return self.val.get()
        else:
            return ''

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
        points=list(range(2*self.CWidth))
        for i in range(self.CWidth):
            #j=(self.nextPtr-1+self.CWidth+i)%self.CWidth
            #lval=int(self.log[j]*(SLICE-2)/4.096)
            #lval=int((self.log[j]+12)/24*(SLICE-2))
            lval=int((self.log[i]+12.0)/24.0)*(SLICE-2)
            points[2*i]=i
            points[2*i+1]=SLICE-1-lval
        self.a2dcanvas.delete("all")
        self.a2dcanvas.create_line(points, fill="#FF0000",width=2)
