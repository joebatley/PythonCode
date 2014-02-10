
import numpy
import pylab as plt
from scipy import *
import tkFileDialog
import Stoner
from Stoner.Folders import DataFolder

#from pylab import arange,pi,sin,cos,sqrt
 


################ READ FILE INFO ########################

#filename = tkFileDialog.askopenfilename(message = 'Pick first file', title = 'Pick file ')
#workingpath = filename.rpartition('/')[0]
   
####### IMPORT DATA ######

folder = DataFolder(False, pattern = '*.txt') 

for f in folder:
  Ref = ((max(f.Resistance)-min(f.Resistance))/2)+min(f.Resistance)
  
  
  Field = f.column('Control:Magnet Output')
 
  
  plt.title('NL dc R vs H for different Temp')
  plt.xlabel(r'Field (T)')
  plt.ylabel(r'Resistance ($\mu$R)')
  plt.ticklabel_format(style='plain', scilimits=(3 ,3))
  plt.hold(True)
  plt.plot(Field,f.column('Resistance')*1e6,label=str(f.metadata['Sample Temp']))
  plt.grid(True)
  
plt.legend()   
plt.show()


