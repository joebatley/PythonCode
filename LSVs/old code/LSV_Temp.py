# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:00:06 2013

@author: py07jtb
"""

import re
import numpy
from scipy import interpolate
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis


fig_width_pt = 1000.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 42,
          #'axes.color_cycle':['b','r','k','g','p','c'],
          'axes.formatter.limits' : [-7, 7],
          'text.fontsize': 36,
          'legend.fontsize': 24,
          'xtick.labelsize': 28,
          'ytick.labelsize': 28,
          'xtick.direction': 'in',
          'ytick.direction': 'in',
          'xtick.major.size':10,
          'ytick.major.size':10,
          'xtick.major.width':1,
          'ytick.major.width':1,
          'figure.figsize': fig_size,
         'font.family':'Arial',
         'xtick.major.pad':20,
         'ytick.major.pad':20,
         'font.size':32,
         'lines.linewidth':2,
         'lines.markersize':10,
         }
 
plt.rcParams.update(params)


#S_Cu = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/Heat_Transport_Data/Thermopower_Copper.txt',1,2,',',',')
#S_Py = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/Heat_Transport_Data/Thermopower_Permalloy.txt',1,2,',',',')
K_Cu = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/Heat_Transport_Data/Themalconductivity_Copper.txt',1,2,',',',')
K_Si = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/Heat_Transport_Data/Themalconductivity_Si.txt',1,2,',',',')
R = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/RN0151_4T_6221-2182 DC IV_Timed interval_0000_1.75_Cuspacer_RvT.txt')


#NewS_Cu = interpolate.interp1d(S_Cu[:,0],S_Cu[:,1])
#NewS_Py = interpolate.interp1d(S_Py[:,0],S_Py[:,1])
NewK_Cu = interpolate.interp1d(K_Cu[:,0],K_Cu[:,1])
NewK_Si = interpolate.interp1d(K_Si[:,0],K_Si[:,1])
Res = -1.0*R.column('Resistance')
NewR = interpolate.interp1d(R.column('Sample Temp')[::-1],Res[::-1])


Acu = 100e-9*50e-9
Asi = 100e-9*10e-6
dz = 100e-9
dx = 500e-9

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
  
 
  
  
  
  
pattern = re.compile('_(?P<IVtemp>\d*)K_NLDCIV_300uA_DigFilt10rep_(?P<state>\w*)_')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/NLIVvsT/Both/',pattern = pattern)
folder.group('IVtemp')
folder.walk_groups(IV_group_Avg,group=True,replace_terminal=True)



for f in folder:
  a=Analysis.AnalyseFile()
  a.add_column(f.column('Current'),'Current')
  a.add_column(f.column('Mean'),'NLV')

  fit, fitVar= a.curve_fit(quad,'Current','NLV',bounds=lambda x,y:abs(x)>150e-6,result=True,header='Fit') 

  plt.title(r'Interface temperature increase - Blue = Detector, Red = Injector')
  plt.xlabel(r'Temperature (K)')
  plt.ylabel(r'T$_{inter}$ (K)')
  plt.ticklabel_format(style='plain', scilimits=(3 ,3))
  plt.hold(True)
  
  KCu = NewK_Cu(f['IVtemp'])*1e2  
  KSi = NewK_Si(f['IVtemp'])
  res = 200*NewR(f['IVtemp'])/min(Res)
  denom =  (KCu*Acu/dx) + (KSi*Asi/dz)
  Spc = ((-0.01411*f['IVtemp'])-0.11185)*1e-6
  T_d = (numpy.min(f.column('Mean'))-numpy.max(f.column('Mean')))/Spc
  T_i = (res*(300e-6*300e-6)+(KSi*Asi*f['IVtemp']/dz)+(KCu*Acu*T_d/dx))/denom
  
  
  plt.plot(f['IVtemp'],T_d,'bo')
  plt.plot(f['IVtemp'],T_i,'ro')
  #plt.plot(f.column('Current'),f.column('Mean'))
plt.figure()
 
  
for f in folder:
  a=Analysis.AnalyseFile()
  a.add_column(f.column('Current'),'Current')
  a.add_column(f.column('Mean'),'NLV')

  fit, fitVar= a.curve_fit(quad,'Current','NLV',bounds=lambda x,y:abs(x)>150e-6,result=True,header='Fit') 

  plt.title(r'Temperature gradient across LSV')
  plt.xlabel(r'Temperature (K)')
  plt.ylabel(r'$\Delta$T (K)')
  plt.ticklabel_format(style='plain', scilimits=(3 ,3))
  plt.hold(True)
  
  KCu = NewK_Cu(f['IVtemp'])*1e2  
  KSi = NewK_Si(f['IVtemp'])
  res = 200*NewR(f['IVtemp'])/min(Res)
  denom =  (KCu*Acu/dx) + (KSi*Asi/dz)
  Spc = ((-0.01411*f['IVtemp'])-0.11185)*1e-6
  T_d = numpy.min(f.column('Mean'))/Spc
  T_i = (res*(300e-6*300e-6)+(KSi*Asi*f['IVtemp']/dz)+(KCu*Acu*T_d/dx))/denom

  
  plt.plot(f['IVtemp'],T_i-T_d,'ro')

plt.show()
  