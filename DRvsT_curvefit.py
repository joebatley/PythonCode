# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 19:34:56 2014

@author: py07jtb
"""

import re
import numpy
from scipy import interpolate
import pylab as plt
from Stoner.Util import format_error
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize
from lmfit import minimize, Parameters, Parameter, report_fit

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
         'lines.markersize':15,}
 
plt.rcParams.update(params)

Seperation = {1:325e-9,
              2:425e-9,
              3:525e-9,
              4:625e-9,
              5:725e-9,
              6:925e-9,
              7:1125e-9,
              8:1325e-9,
              9:1525e-9,}
# define objective function: returns the array to be minimized
def Rs(Temp,a,b,p):#,Alpha):
  
   
  P = p#*(1-(Temp/1200)**(3/2))#params['P'].value #0.8
  
  
  L = 425e-9
  t=Temp
  
  
  Wpy = 150e-9
  Wcu = 150e-9
  Tcu = 130e-9
  Lambda_F = 5e-9*(PyR(10)/PyR(t))    
  PyRes = -PyR(t)*((30e-9*5e-6)/50e-6)
  CuRes = CuR(t)*((Tcu*150e-9)/925e-9)
  Lambda_N = a/(t+b)
  
  Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
  Rn = (CuRes*Lambda_N)/(Wcu*Tcu)   
  model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))
  
  Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
  Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
  model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
  model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))

  return model_Cas
  


# Import and interpolate the resistivity data
Py = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaR_vs_Sep/RN200_5um_6221-2182 DC IV_Timed interval_RvT_500uA_.txt')
Py.sort('Sample Temp')
print min(Py.column('Sample Temp')),max(Py.column('Sample Temp'))
PyR = interpolate.interp1d(Py.column('Sample Temp'),Py.column('Resistance'))
Cu = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_6_T/SC004_6_T_6221-2182 DC IV_Timed interval_3.223900_RvT_CuBar_100uA.txt')
Cu.sort('Sample Temp')
print min(Cu.column('Sample Temp')),max(Cu.column('Sample Temp'))
CuR = interpolate.interp1d(Cu.column('Sample Temp'),Cu.column('Resistance'))

# Import Delta R vs T data and group
pattern = re.compile('SC004_(?P<L>\d*)_(?P<Device>\w*)_DeltaRvsT')
folder = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaR_vs_Sep/SC004_3_T_DeltaRvsT.txt',pattern = pattern)
print folder
print len(folder)
folder.del_rows(23)
folder.del_rows(0)
a = Analysis.AnalyseFile(folder)

fit= a.curve_fit(Rs,'Temp','DeltaR',p0=[400e-9,1.0,0.4],sigma = 'DeltaR err',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
print fit


# Plot Lambda and alpha
fig, ax1 = plt.subplots()
ax1.set_xlabel('Temperature (K)',labelpad=15)
plt.hold(True)

ax1.plot(a.column('Temp'),a.column('DeltaR'),'ob')
ax1.plot(a.column('Temp'),a.Fit,'-k')
ax1.set_ylabel('$\Delta$R$_s$ (mV/A)', color='k',labelpad=15)
for tl in ax1.get_yticklabels():
    tl.set_color('k')
#plt.legend(loc='upper left')  

ax2 = ax1.twinx()
#ax2.plot(a.column('Temp'),(fit[0]/a.column('Temp'))+fit[2],'-r')
ax2.plot(a.column('Temp'),fit[0]/(a.column('Temp')+fit[2]),'-r')
ax2.set_ylabel(r'$\lambda_{Cu}$', color='r',labelpad=15)
for t2 in ax2.get_yticklabels():
    t2.set_color('r')

plt.tight_layout(pad=0.1, w_pad=0.0, h_pad=0.0)
#plt.legend(loc = 'upper right')
plt.show()
 



