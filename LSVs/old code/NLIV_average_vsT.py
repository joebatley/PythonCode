import re
import numpy
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.Plot as plot


################ READ FILE INFO ########################
def func(x):
  return numpy.mean(x)

def quad(x,a,b,c):
  return a*x*x+b*x+c

def IV_group_Avg(folder,keys):
  avg = Analysis.AnalyseFile(folder[0])
  avg.del_column('Voltage')
  avg.del_column('Current')
  avg.del_column('Column 2')
  for f in folder:
    avg.add_column(f.Voltage*-1,str(f.metadata['iterator']))
  avg.apply(func, 1, replace = False, header = 'Mean NLVoltage')
  avg.add_column(folder[1].column('Current'),'Current')
  return avg


pattern = re.compile('_(?P<IVtemp>\d*)K_')
folder = DataFolder('/Users/py07jtb/PhD/Measurements/Blaatand/RN0151_4T/NLIVvsT/AP/',pattern = pattern)
folder.group('IVtemp')
print folder.groups.keys()
folder.walk_groups(IV_group_Avg,group=True,replace_terminal=True)

"""
for f in folder:
  a=Analysis.AnalyseFile(f)
  fit, fitVar= a.curve_fit(quad,'Current','Mean NLVoltage',bounds=lambda x,y:abs(x)>150e-6,result=True,header='Fit') 
  
  current = a.Current*1e6
  Voltage = a.column('Mean NLVoltage')*1e6
  
  plt.title(r'NL IV offset vs Temperature for Antiparallel State')
  plt.xlabel(r'Temperature (K)')
  plt.ylabel(r'NL V offset (nV)')
  plt.ticklabel_format(style='plain', scilimits=(3 ,3))
  plt.hold(True)
  #plt.plot(current,Voltage,label = str(a['IVtemp']))
  plt.errorbar(f['IVtemp'],fit[2]*1e9,(fitVar[2,2]/5),ecolor='k',marker='o',mfc='red', mec='red')
  plt.grid(True)
#plt.legend()
plt.show()

"""












