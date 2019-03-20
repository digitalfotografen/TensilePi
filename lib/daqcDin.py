from tkinter import *
from lib.singeltons import *

class daqcDIN:
    def __init__(self,root,addr,channel):
        self.root=root
        self.addr=addr
        self.chan=channel
        self.var=IntVar()
        self.var.set(1)    
        self.val=IntVar()
        self.val.set(DAQC.getDINbit(self.addr,self.chan))
        self.valstring=StringVar()
        self.valstring.set(str(self.val.get()))
        
        off=H-2-9*SLICE+self.chan*SLICE
        BG='#FFFFFF888'
        self.CWidth=int(.75*W+20)        
        self.dinf=Frame(self.root,bg=BG,bd=0,relief="ridge")
        self.dinf.place(x=0,y=off,width=W,height=SLICE)
        self.dinc=Checkbutton(self.dinf,fg="Black",bg=BG,variable=self.var,command=self.cb)
        self.dinc.grid(row=0,column=0,sticky="w")
        self.dinl = StringVar(root, value="DIN Channel "+str(self.chan)+":")
        self.dint = Label(self.dinf,textvariable=self.valstring,fg="Black",bg=BG,width=5)
        self.dint.grid(row=0,column=2,sticky="w")
        self.dintxt=Entry(self.dinf,textvariable=self.dinl,fg="Black",bg=BG,bd=0,relief="flat",width=12)
        self.dintxt.grid(row=0,column=1,sticky="w")
        self.dincanvas=Canvas(self.dinf,bg=BG,width=self.CWidth,height=SLICE,bd=0,relief="flat")
        self.dincanvas.grid(row=0,column=3,sticky="e")
        self.maxrange=self.CWidth
        self.log=list(range(self.maxrange))
        for i in range(self.maxrange):
            self.log[i]=0.0
        self.nextPtr=0
        
    def cb(self):
        if (self.var==1):
            a=1  

    def deSelect(self):
        self.dinc.deselect()

    def Select(self):
        self.dinc.select()  
        
    def update(self):
        if (self.var.get()==1):
            self.val.set(DAQC.getDINbit(self.addr,self.chan))
            self.valstring.set(str(self.val.get()))
            self.log[self.nextPtr]=self.val.get()
            self.nextPtr=(self.nextPtr+1)%self.maxrange
            self.plot()
            return self.val.get()
        else:
            return ''

    def descriptors(self):
        if (self.var.get()==1):
            return self.dinl.get()
        else:
            return ''            

    def getLabel(self):
        return self.dinl.get()

    def setLabel(self,label):
        self.dinl.set(label)         

    def getState(self):
        return self.var.get()  

    def setState(self,state):
        if (state=='1'):
            self.dinc.select()
        else:
            self.dinc.deselect()
            
    def plot(self):
        points=list(range(2*self.CWidth))
        for i in range(self.CWidth):
            j=(self.nextPtr-1+self.CWidth+i)%self.CWidth
            lval=int(self.log[j]*(SLICE-3))
            points[2*i]=i
            points[2*i+1]=SLICE-1-lval
        self.dincanvas.delete("all")
        self.dincanvas.create_line(points, fill="#0000FF",width=2)
