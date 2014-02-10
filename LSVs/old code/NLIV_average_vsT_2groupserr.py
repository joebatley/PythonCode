import re
import numpy
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.Plot as plot


################ READ FILE INFO ########################
def row_avg(x):
  return numpy.mean(x)

def err(x):
  return numpy.std(x)/numpy.sqrt(len(x))
  
def quad(x,a,b,c):
  return a*x*x+b*x+c

def IV_group_Avg(folder,keys):
  avg = Analysis.AnalyseFile()
  for f in folder:
    a=Analysis.AnalyseFile(f)
    fit, fitVar= a.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:abs(x)>200e-6)
    avg.add_column(fit,str(a.metadata['iterator']))
    avg['state']=f['state']
    avg['IVtemp']=f['IVtemp']
  avg.apply(row_avg, 1, replace = False, header = 'Mean Coef')
  avg.apply(err, 1, replace = False, header = 'Err Coef')
  return avg
  
def P_AP_col(folder,keys):
  coef = Stoner.DataFile()
  for f in folder:
    coef.add_column(f.column('Mean Coef'),str(f['IVtemp']))
    coef.add_column(f.column('Err Coef'),str(f['IVtemp'])+' Err')
  print coef
  return coef

pattern = re.compile('_(?P<IVtemp>\d*)K_NLDCIV_300uA_DigFilt10rep_(?P<state>\w*)_')
folder = DataFolder('/Users/Joe/PhD/Measurements/RN0151_4T/NLIVvsT/Both/',pattern = pattern)
folder.group(['state','IVtemp'])

folder.walk_groups(IV_group_Avg,group=True,replace_terminal=True)

folder.walk_groups(P_AP_col,group=True,replace_terminal=True)

print folder['AP']
  
for f in folder:
  
  for column in f.column_headers:
    plt.title(r'NL IV offset vs Temperature for Parallel (red) and Antiparallel (blue) State')
    plt.xlabel(r'Temperature (K)')
    plt.ylabel(r'$\alpha$ ($\mu$V/A) ')
    plt.ticklabel_format(style='plain', scilimits=(3 ,3))
    plt.hold(True)
    plt.grid(True)
    
    if folder['state'] == 'P':
        plt.errorbar(folder['IVtemp'],folder['P'].column('Mean Coef')[1],folder['P'].column('Err Coef')[1],ecolor='k',marker='o',mfc='red', mec='red')
    else:
        plt.errorbar(folder['IVtemp'],folder['AP'].column('Mean Coef')[1],folder['AP'].column('Err Coef')[1],ecolor='k',marker='o',mfc='blue', mec='blue')
  
#plt.legend()
plt.show()














