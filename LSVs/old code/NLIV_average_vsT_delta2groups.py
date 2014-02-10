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

def P_AP(folder,keys):
  coef = Stoner.DataFile()
  for f in folder:
    a=Analysis.AnalyseFile(f)
    fit, fitVar= a.curve_fit(quad,'Current','Mean NLVoltage',bounds=lambda x,y:abs(x)>150e-6,result=True,header='Fit') 
    coef.add_column(fit,str(a['IVtemp']))
    coef['state'] = a['state']
  return coef
  
  
pattern = re.compile('_(?P<IVtemp>\d*)K_NLDCIV_300uA_DigFilt10rep_(?P<state>\w*)_')
folder = DataFolder('/Users/py07jtb/PhD/Measurements/Blaatand/RN0151_4T/NLIVvsT/Both/',pattern = pattern)
folder.group(['state','IVtemp'])

folder.walk_groups(IV_group_Avg,group=True,replace_terminal=True)
    
folder.walk_groups(P_AP,group=True,replace_terminal=True)

for column in folder['P'].column_headers:
  print column
  print folder['AP'].column_headers
  if column in folder['AP'].column_headers:
    
    Delta = folder['AP'].column(column)[0]-folder['P'].column(column)[0]
    plt.hold(True)
    plt.title(r'NL IV $\Delta$ Quad Coefficient vs Temperature')
    plt.xlabel(r'Temperature (K)')
    plt.ylabel(r'NL IV $\Delta$ Quad Coefficient')
    plt.grid(True)
    plt.ticklabel_format(style='plain', scilimits=(3 ,3))
    plt.plot(int(column),Delta,'ro')
plt.show()





"""
    
    current = a.Current*1e6
    Voltage = a.column('Mean NLVoltage')*1e6
    
    plt.title(r'NL IV offset vs Temperature for Parallel (red) and Antiparallel (blue) State')
    plt.xlabel(r'Temperature (K)')
    plt.ylabel(r'NL V offset (nV) ')
    plt.ticklabel_format(style='plain', scilimits=(3 ,3))
    plt.hold(True)
    #plt.plot(current,Voltage,label = str(a['IVtemp']))
    print a['state'],a['IVtemp']
    if a['state'] == 'P':
      plt.errorbar(f['IVtemp'],fit[2]*1e9,(fitVar[1,1]/5),ecolor='k',marker='o',mfc='red', mec='red')
    else:
      plt.errorbar(f['IVtemp'],fit[2]*1e9,(fitVar[1,1]/5),ecolor='k',marker='o',mfc='blue', mec='blue')
    plt.grid(True)
  #plt.legend()
  plt.show()

"""









