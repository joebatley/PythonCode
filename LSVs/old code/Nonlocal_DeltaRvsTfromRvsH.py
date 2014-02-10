
import numpy
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.Plot as plot


####### IMPORT DATA ######

folder = DataFolder(False, pattern = '*.txt') 

for f in folder:
  a=Analysis.AnalyseFile(f)
  
  ref = ((max(f.Resistance)-min(f.Resistance))/2)+min(f.Resistance) #Find reference resistance to seperate P and AP
  
  Parallel = numpy.mean(a.search('Resistance',lambda x,y:x>ref,'Resistance')) #average all resistances in P state
  AntiParallel = numpy.mean(a.search('Resistance',lambda x,y:x<ref,'Resistance')) #average all resistances in AP state
  Delta = (Parallel-AntiParallel)*1e6 #calculate Delta R in micro Ohms
   
  Perr = (numpy.std(a.search('Resistance',lambda x,y:x>ref,'Resistance')))/numpy.sqrt(len(a.search('Resistance',lambda x,y:x>ref,'Resistance'))) # error in average value for P state
  APerr = (numpy.std(a.search('Resistance',lambda x,y:x<ref,'Resistance')))/numpy.sqrt(len(a.search('Resistance',lambda x,y:x<ref,'Resistance')))
  DRerr = numpy.sqrt((Perr*Perr)+(APerr*APerr)) #calculate error in Delta R in micro Ohms
 
 
  offset = ref*1e6
  
  plt.title(r'NL Resistance offset vs Temperature')
  plt.xlabel(r'Temperature (K)')
  plt.ylabel(r'Nonlocal Spin Resistance offset($\mu\Omega$)')
  plt.ticklabel_format(style='plain', scilimits=(3 ,3))
  plt.hold(True)
  #plt.plot(f.metadata['Sample Temp'],offset,'ro')
  plt.errorbar(f.metadata['Sample Temp'],Delta,DRerr,ecolor='k',marker='o',mfc='red', mec='red')
  plt.grid(True)
  
  
plt.show()


