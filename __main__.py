#!/usr/bin/python3
import os
import string
import subprocess
import sys
import time
import csv
from datetime import datetime

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.messagebox import showerror
from tkinter import font

import random
import math
import imp
import statistics

from lib.globals import *
from lib.daqcAdc import daqcADC
from lib.daqcDin import daqcDIN
from lib.daqcDash import daqcDASH

# define options for opening or saving a log file
newlogfile_opt = options = {}
options['defaultextension'] = '.csv'
options['filetypes'] = [('csv files', '.csv')]
options['title'] = 'Open new log file'
options['initialdir'] = "~/Documents"

# define options for opening or saving an existing log file
xlogfile_opt = options = {}
options['defaultextension'] = '.csv'
options['filetypes'] = [('csv files', '.csv')]
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
        if ('.csv' in fName):
            lfOpen=True
    
def StartLog():
    global logFile, lfOpen, Logging, fName, SampleC, csvfile
    if ((lfOpen) and  (Logging==False)):
        logHeader = ["DateTime"]
        logHeader += daqc.a2dGetLabels()
        logHeader += daqc.forceGetLabels()
        if (lfOpen):
            logFile=open(fName,'w')
            csvfile = csv.writer(logFile, dialect='excel-tab')
            csvfile.writerow(tuple(logHeader))
        Logging=True   
        SampleC=int(SampleCount.get())
    else:
        showerror(
            "Logging",
            "You must open a log file before you can start logging"
        )
    
def StopLog():
    global logFile, lfOpen, Logging, csvfile
    if (Logging):
        Logging=False
        root.wm_title("TensilePi")
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
    global lfOpen, Logging
    StopLog()
    if (lfOpen):
        logFile.close()
    root.destroy()

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

#sample all active channels
def sample():
    global logFile, lfOpen, Logging, fName, SampleC, SampleT, csvfile
    global theta, dnum
    root.after(int(SampleT*1000),sample)   
    date = datetime.now().strftime("%y-%m-%d %H:%M:%S.%f")[:-3]
    a2dvals=list(range(ADCHANNELS))
    #dinvals=list(range(8))
    forcevals=list(range(1))
    a2dvals=daqc.a2dsample() 
    #dinvals=daqc.dinsample()
    forcevals=daqc.forcesample() 
            
    if (Logging and lfOpen):
        csvfile.writerow(tuple([date] + a2dvals + forcevals))
        SampleC +=1
           
#update UI with values and plots
def update():
    global fName
    root.after(int(UpdateT*1000),update)   
    daqc.a2dupdate() 
    daqc.forceupdate() 

    if (Logging):
        root.wm_title("TensilePi - " + fName + " - " +str(SampleC)+" Samples and "+str(int(SampleT*SampleC))+" Seconds")

# Main program
UpdateT = config.getfloat('Main','update_t', fallback=0.3)
SampleT = config.getfloat('Main','sample_t', fallback=0.1)
theta=[0,0,0,0,0,0,0,0]  
dnum=[0,0,0,0,0,0,0,0]
SampleC=0
logFile=0
lfOpen=False
Logging=False
fName=''
csvfile=0
            
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

menu.add_command(label="START", foreground='green',font="-weight bold", command=StartLog)

menu.add_command(label="STOP", foreground='red',font="-weight bold",command=StopLog)

#Todo ViewLog class
#menu.add_command(label="VIEW", foreground='blue',font="-weight bold",command=ViewLog)

def callback():
    print ("click!")


canvas = Canvas(root, width=W, height=H)
canvas.pack()

#DAQCpresent=list(range(8))
DAQCpresent=[1,0,0,0,0,0,0,0]
#daqc=list(range(8))
DAQCFoundCount=0
#daqcpage=range(8)

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

SamplePeriod=StringVar()
SamplePeriod.set(str(SampleT))

SampleCount=StringVar()
SampleCount.set('0')

sDval=StringVar()
sDval.set(str(float(SamplePeriod.get())*float(SampleCount.get())))

AoutSignal=IntVar()
AoutSignal.set(0)
DoutSignal=IntVar()
DoutSignal.set(0)
    
root.after(int(SampleT*1000),sample) 
root.after(int(UpdateT*1000),update)
      
root.mainloop()        
