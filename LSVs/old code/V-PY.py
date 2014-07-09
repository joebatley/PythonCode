import re
import numpy
from scipy import interpolate
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize

import Stoner.PlotFormats as SPF
import Stoner.Plot as SP

fig_width_pt = 800.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 28,
          'axes.linewidth':2,
          'text.fontsize': 28,
          'title.fontsize':28,
          'legend.fontsize': 24,
          'xtick.labelsize': 28,
          'ytick.labelsize': 28,
          'xtick.direction': 'in',
          'ytick.direction': 'in',
          'xtick.major.size':10,
          'xtick.major.width':2,
          'ytick.major.size':10,
          'ytick.major.width':2,
          'figure.figsize': fig_size,
         'font.family':'Arial',
         'xtick.major.pad':20,
         'ytick.major.pad':20,
         'font.size':25,
         'lines.linewidth':4,
         'lines.markersize':15}
 
plt.rcParams.update(params)



################ READ FILE INFO ########################
def func(x):
  return numpy.mean(x)

def quad(x,a,b,c):
  return a*x*x+b*x+c
  
def heat(x,i,R,Ks,As,dz,Kcu,Acu,dx,Td,Ts): 
  y=(i**2)*R - (Ks*As/dz)*(x-Ts) - (Kcu*Acu/dx)*(x-Td) 
  return y

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





#################### DELTA R VS TEMP ####################

def Py_V(folder,keys):
  folder.group('Inj') 
  print folder
  Py_beta = 0
  V_beta = 0  
  print len(folder.groups['V'])
  for f in folder.groups['V']:
    print f
    V = Analysis.AnalyseFile(f)
    fit = V.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
    V_beta = V_beta+fit[0]
  for f in folder.groups['Py']:
    Py = Analysis.AnalyseFile(f)
    fit = Py.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
    Py_beta = Py_beta+fit[0] 

  
  V_beta_norm = (V_beta/len(folder.group('V')))/Res_V(V['Sample Temp'])
  Py_beta_norm = (Py_beta/len(folder.group('Py')))/Res_Py(Py['Sample Temp'])
 
  plt.hold(True)
  plt.title('',verticalalignment='bottom')
  plt.xlabel('Temperture (K)')
  plt.ylabel('')
  plt.plot(f['IVtemp'],Py_beta_norm-V_beta_norm,'ob')
  
  return 1
  



  

InjPy = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/SC004_3_T_6221-2182 DC IV_Timed interval_0_PyInj_RvT_100uA_Full.txt')
InjPy.sort('Sample Temp')
InjV = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/SC004_3_T_6221-2182 DC IV_Timed interval_0__V_RvT_100uA_!0000.txt')
InjV.sort('Sample Temp')
CuRvt = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/SC004_3_T_6221-2182 DC IV_Timed interval_RvT_CuBar_100uA_!0001.txt')
CuRvt.sort('Sample Temp')

Res_Cu = interpolate.interp1d(CuRvt[:,3],CuRvt[:,2])
Res_V = interpolate.interp1d(InjV[:,3],InjV[:,2])
Res_Py = interpolate.interp1d(InjPy[:,3],InjPy[:,2])

Acu = 130e-9*150e-9
Asi = 150e-9*16e-6
dz = 1000e-9
dx = 425e-9

Seperation = {1:325e-9,
              2:425e-9,
              3:525e-9,
              4:625e-9,
              5:725e-9,
              6:925e-9,
              7:1125e-9,
              8:1325e-9,
              9:1525e-9,}

  
  
  

#################### IMPORTDATA AND WALK GROUPS ####################

pattern = re.compile('_(?P<state>\d*)_(?P<IVtemp>\d*)K_(?P<Inj>\w*)_NLIV_300uA_')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/NLIVvsHvsT_BOTH',pattern = pattern)


Output = Stoner.DataFile()
Output['Sample ID'] = folder[0]['Sample ID']
folder.group('IVtemp')
#print folder


folder.walk_groups(Py_V,group=True,replace_terminal=True)


