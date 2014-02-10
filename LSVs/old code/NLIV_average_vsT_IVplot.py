import re
import numpy
import pylab as plt
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis


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
    avg.add_column(f.Voltage,str(f.metadata['iterator']))
  avg.apply(func, 1, replace = False, header = 'Mean NLVoltage')
  avg.add_column(folder[1].column('Current'),'Current')
  return avg


pattern = re.compile('_(?P<IVtemp>\d*)K_')
folder = DataFolder('/Users/Joe/PhD/Measurements/RN0151_4T/NLIVvsT/70K-PandAP/',pattern = pattern)
folder.group('IVtemp')
folder.walk_groups(IV_group_Avg,group=True,replace_terminal=True)


for f in folder:
  offset = f.column('Mean')[0]
  Voltage = f.column('Mean') - offset
  plt.title(r'')
  plt.xlabel(r'Current ($\mu$A)')
  plt.ylabel(r'Non Local Voltage ($\mu$V)')
  plt.ticklabel_format(style='plain', scilimits=(3 ,3))
  plt.hold(True)
  plt.plot(1e6*f.column('Current'),1e6*Voltage,label = str(f['IVtemp']) + 'K')
  plt.grid(False)
plt.legend()
plt.show()














