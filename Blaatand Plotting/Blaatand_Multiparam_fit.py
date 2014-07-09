'''
import and average MR files from Serban's rig
'''

'''
Note:
debug in Pythonwin.exe
from command window open folder	to check and change directory use
	os.curdir    #retrieves current directory `.' for windows
	os.getcwd()  #retrieves current working directory
	PathName = 'y:\\Python\\NAP\\DWsensor'
	os.chdir(PathName)  #change directory
then to run use:
	execfile('DWsensor.py')
	#import DWsensor.py
runs better from pylab or other environments
'''

import os
import sys
import numpy
import time
import pylab as plt
import mpl_toolkits.mplot3d.axes3d as p3
from scipy import *
import tkFileDialog
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.Plot as plot
#from pylab import arange,pi,sin,cos,sqrt
 


################ READ FILE INFO ########################

filename = tkFileDialog.askopenfilename()
workingpath = filename.rpartition('/')[0]
   
####### IMPORT DATA ######

folder = DataFolder(workingpath, pattern = '*.txt') 

####### ANALYSE DATA ########

d=Stoner.DataFile()
I = folder[1].search('Current',lambda x,y: x>0,'Current')
Current = []
for x in I:
  Current.append(float(x))
d.add_column(Current,'Current')

Vdiff = []
Field = []
for f in folder:
  Vpos = array(f.search('Current',lambda x,y: x>0,'Voltage'))
  Vneg = array(f.search('Current',lambda x,y: x<-10e-9,'Voltage'))
  Vdiff=Vpos-Vneg
  
  Voltagediff=[]
  for x in Vdiff:
    Voltagediff.append(float(x))
  if Vdiff.all() =0.0:
    print str('error')
  else:
    d.add_column(Voltagediff,str(f.metadata['Control:Magnet Output']))
    Field.append(f.metadata['Control:Magnet Output'])
  
  
  
print d.data
print shape(d.data)
filename = str('test')
###### PLT DATA ##########
d.save(filename)
p=plot.PlotFile(d)
p.plot_matrix()


#plt.title('Voltage at plus/minus 300 microAmps vs B, 1.4K')
#plt.xlabel('B (T)')
#plt.ylabel(u'Voltage (V)')
#plt.ticklabel_format(style='plain', scilimits=(3 ,3))
#plt.hold(True)
#plt.plot(d.Current,d.column(2))
#plt.grid(True)
#plt.show()
















