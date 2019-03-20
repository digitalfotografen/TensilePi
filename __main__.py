#!/usr/bin/python3
import time
from datetime import datetime
import os
import string
import subprocess
import sys

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.messagebox import showerror
from tkinter import font

import random
import math
import imp
import statistics

from lib.singeltons import *
from lib.daqcAdc import daqcADC
from lib.daqcDin import daqcDIN
from lib.daqcDash import daqcDASH

# define options for opening or saving a log file
newlogfile_opt = options = {}
options['defaultextension'] = '.log'
options['filetypes'] = [('log files', '.log')]
options['title'] = 'Open new log file'

# define options for opening or saving an existing log file
xlogfile_opt = options = {}
options['defaultextension'] = '.log'
options['filetypes'] = [('log files', '.log')]
options['title'] = 'Open existing log file'

# define options for opening or saving a setup file
setupfile_opt = options = {}
options['defaultextension'] = '.stp'
options['filetypes'] = [('setup files', '.stp')]
options['title'] = 'Open setup file'

# define user interface call backs
def on_closing():
    shutdown()

def NewLogFile():
    global logFile, lfOpen, fName
    if (Logging==False):
        fName=''
        fName=filedialog.asksaveasfilename(**newlogfile_opt)
        if ('.log' in fName):
            lfOpen=True
    
def StartLog():
    global logFile, lfOpen, Logging, fName, SampleC, logHeader
    if ((lfOpen) and  (Logging==False)):
        root.wm_title("DAQCplate Data Logger - LOGGING")

        Header="Time,"
        desc=['','','','','','','','']
        desc=daqc.a2dDescriptors()
        for k in range(8):
            if (desc[k] != ''):
                Header= Header+'DAQC'+'.'+desc[k]+','
        desc=['','','','','','','','']
        '''
        desc=daqc.dinDescriptors()
        for k in range(8):
            if (desc[k] != ''):
                Header= Header+'DAQC'+'.'+desc[k]+','
        '''        
        Header = Header[:-1] 
        logHeader=Header
        if (lfOpen):
            logFile=open(fName,'w')
            logFile.write(Header)
            logFile.write('\n')
        Logging=True   
        SampleC=int(SampleCount.get())
    else:
        showerror(
            "Logging",
            "You must open a log file before you can start logging"
        )
    
def StopLog():
    global logFile, lfOpen, Logging
    if (Logging):
        Logging=False
        root.wm_title("DAQCplate Data Logger")
        if (lfOpen):
            logFile.close()
            lfOpen=False

def About():
    Pmw.aboutversion('0.1')
    Pmw.aboutcopyright('DigitalFotografen AB, 2019\nAll rights reserved')
    Pmw.aboutcontact(
        'For information about this application contact:\n' +
        'ulrik@digitalfotografen.se'
    )
    about = Pmw.AboutDialog(root, applicationname = 'TensilePi')
    about.activate(globalMode = 0, geometry = 'centerscreenfirst')
    about.withdraw()
    about.show() 

def shutDown():
    global lfOpen, Logging, GPIO
    StopLog()
    if (lfOpen):
        logFile.close()
    root.destroy()
    GPIO.cleanup()

#Configure: Dialog box to get sampling parameters that holds focus until closed.    
def Configure():
    if (Logging==False):
        cBox=Toplevel()    
        cBox.transient(master=root)
        cBox.wm_title("Log Setup")   
        cBox.focus_set()

        sP=Label(cBox,text='Sample Period in Seconds (Minimum is '+str(SampleTmin)+'):', padx=2, pady=2)
        sP.grid(row=0,column=0,sticky="e")
        sPval=Entry(cBox,width=8,textvariable=SamplePeriod)
        sPval.grid(row=0,column=1,sticky="w")
        
        sC=Label(cBox,text="Sample Count:", padx=2, pady=2)
        sC.grid(row=1,column=0,sticky="e")
        sCval=Entry(cBox,width=8,textvariable=SampleCount)
        sCval.grid(row=1,column=1,sticky="w")

        sD1=Label(cBox,text="Log Duration in seconds = ", pady=20)
        sD1.grid(row=2,column=0,sticky="e")
        sD2=Label(cBox,textvariable=sDval, pady=20)
        sD2.grid(row=2,column=1,sticky="w")
    
        sB=Button(cBox, text='Close', command=cBox.destroy)
        sB.grid(row=3, columnspan=2, pady=4)

        cBox.grab_set()
        root.wait_window(cBox)

#signalSetup: Dialog box to control test signals that holds focus until closed.    
def signalSetup():
    global aoutSignalOn, doutSignalOn
    
    sigBox=Toplevel()    
    sigBox.transient(master=root)
    sigBox.wm_title("Test Signal Setup")   
    sigBox.focus_set()

    aoutchk=Checkbutton(sigBox,variable=AoutSignal,onvalue = 1, offvalue = 0)
    aoutchk.grid(row=0,column=0,sticky="e")
    sA=Label(sigBox,text='Enable Analog Signals     ', padx=2, pady=2)
    sA.grid(row=0,column=1,sticky="w")
    
    doutchk=Checkbutton(sigBox,variable=DoutSignal,onvalue = 1, offvalue = 0)
    doutchk.grid(row=1,column=0,sticky="e")
    sD=Label(sigBox,text='Enable Digital Signals     ', padx=2, pady=2)
    sD.grid(row=1,column=1,sticky="w")
        
    cBut=Button(sigBox, text='Close', command=sigBox.destroy)
    cBut.grid(row=2, columnspan=2, padx=2, pady=2)

    sigBox.grab_set()
    root.wait_window(sigBox) 

def task():
    global logFile, lfOpen, Logging, fName, SampleC, SampleT, logHeader
    global theta, dnum
    aChannelCount=0
    dChannelCount=0
    fChannelCount=0
    try:
        SampleT=float(SamplePeriod.get())
        if (SampleT<SampleTmin):
            SampleT=SampleTmin
    except ValueError:
        SampleT=SampleTmin
    root.after(int(SampleT*1000),task)   
    date = datetime.now().strftime("%y-%m-%d %H:%M:%S.%f")[:-3]
    logString=date+','
    dTypes=''
    # loop removed
    a2dvals=list(range(8))
    #dinvals=list(range(8))
    forcevals=list(range(1))
    #Retrieve and plot  values
    a2dvals=daqc.a2dupdate() 
    #dinvals=daqc.dinupdate()
    forcevals=daqc.forceupdate() 
            
    #Convert data to strings for log
    for k in range(8):
        if (a2dvals[k] != ''):
            logString=logString+str(a2dvals[k])+','
            aChannelCount += 1
            dTypes = dTypes+'a,'
    '''
    for k in range(8):
        if (dinvals[k] != ''):
            logString=logString+str(dinvals[k])+','
            dChannelCount += 1
            dTypes = dTypes+'d,'
    '''        
    for k in range(1):
        if (forcevals[k] != ''):
            logString=logString+str(forcevals[k])+','
            fChannelCount += 1
            dTypes = dTypes+'d,'
     
    dtypes = dTypes[:-1]
    #logString = logString[:-1] 
    #logString = time.strftime("%H:%M:%S.%f")[:-3]+','+logString    
    if (Logging and lfOpen):
        #logString = logString[:-1]
        #logString = time.strftime("%H:%M:%S",time.localtime())+','+logString
        logFile.write(logString)
        logFile.write('\n')        
           
    if (Logging):
        SampleC -= 1
        root.wm_title("DAQCplate Data Logger - LOGGING - "+str(SampleC)+" Samples and "+str(SampleT*SampleC)+" Seconds Remaining")
        if (SampleC==0):
            StopLog()
            showinfo("Logging","Logging Complete")                                      
            
#doUpdates: a recurring routine to update the value of the displayed test duration value
def doUpdates():
    root.after(500,doUpdates)   
    try:
        sDval.set(str(float(SamplePeriod.get())*float(SampleCount.get())))
    except ValueError:
        sDval.set('0') 

SampleT=0.1
theta=[0,0,0,0,0,0,0,0]  
dnum=[0,0,0,0,0,0,0,0]
SampleC=0
logFile=0
lfOpen=False
Logging=False
logHeader=''
fName=''
            
root = Tk()
root.resizable(0,0)
#root=Pmw.initialise()

menu=Menu(root)
root.wm_title("TensilePi")
    
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
x = w/2 - W/2
y = h/2 - H/2
root.geometry("%dx%d+%d+%d" % (W,H,x, y))

root.config(menu=menu)
filemenu = Menu(menu,tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open New File for Logging", command=NewLogFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=shutDown)

setupmenu = Menu(menu,tearoff=0)
menu.add_cascade(label="Setup", menu=setupmenu)
setupmenu.add_command(label="Logging", command=Configure)
setupmenu.add_command(label="Test Signals", command=signalSetup)
  
menu.add_command(label="START", foreground='green',font="-weight bold", command=StartLog)

menu.add_command(label="STOP", foreground='red',font="-weight bold",command=StopLog)

#Todo ViewLog class
#menu.add_command(label="VIEW", foreground='blue',font="-weight bold",command=ViewLog)

def callback():
    print ("click!")


#notebook = Pmw.NoteBook(root,borderwidth=2,pagemargin=2)
#notebook.pack(fill = 'both', expand = 1)
#off=0
#frame=Frame(root,bd=0,relief="ridge")
#frame.place(x=0,y=off,width=W,height=H)   

canvas = Canvas(root, width=W, height=H)
canvas.pack()

DAQCpresent=list(range(8))
#daqc=list(range(8))
DAQCFoundCount=0
#daqcpage=range(8)

SampleTmin=0
focusSet=False
rtn = DAQC.getADDR(0)
DAQCpresent[0]=1
DAQCFoundCount+=1
DAQC.setDOUTall(0,0)
DAQC.setDAC(0,0,0)
DAQC.setDAC(0,1,0)
DAQC.setDAC(0,2,0)
DAQC.setDAC(0,3,0)        
daqc=daqcDASH(canvas,0)
SampleTmin+=0.1


if (SampleTmin>0):
    SampleT=SampleTmin
else:
    SampleT=0.2

SamplePeriod=StringVar()
SamplePeriod.set(str(SampleT))

SampleCount=StringVar()
SampleCount.set('1000')

sDval=StringVar()
sDval.set(str(float(SamplePeriod.get())*float(SampleCount.get())))

AoutSignal=IntVar()
AoutSignal.set(0)
DoutSignal=IntVar()
DoutSignal.set(0)
    
root.after(int(SampleT*1000),task) 

root.after(500,doUpdates) 
      
root.mainloop()        
