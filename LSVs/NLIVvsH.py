# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 19:08:57 2014

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

'''
fig_width_pt = 800.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 40,
          'axes.linewidth':2,
          'text.fontsize': 30,
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
         'font.size':28,
         'lines.linewidth':4,
         'lines.markersize':15}
 
plt.rcParams.update(params)
'''
 
def quad(x,a,b,c):
  return (a*x**2)+(b*x)+c


folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_2_T/NLIVvsHat5K', pattern = '*.txt') 


Field_down = []
NLR_down = []
iterator_down = []
Field_up = []
NLR_up = []
iterator_up = []


for f in folder:
  a = Analysis.AnalyseFile(f)
  fit = a.curve_fit(quad,'Current','Voltage',p0=[20.0,1e-7,0.0], result=True, replace=False, header="fit",asrow=True)
  
  if a['iterator']<len(folder)/2:  
    NLR_down.append(fit[2])
    Field_down.append(a['Magnet Output']*1e-9)
    iterator_down.append(a['iterator'])
  else:
    NLR_up.append(fit[2])
    Field_up.append(a['Magnet Output']*1e-9)
    iterator_up.append(a['iterator'])

result_down = Stoner.DataFile()
result_down.add_column(Field_down,column_header='Field')
result_down.add_column(iterator_down,column_header='i')
result_down.add_column(NLR_down,column_header='NLR')
result_down.sort('i')


result_up = Stoner.DataFile()
result_up.add_column(Field_up,column_header='Field')
result_up.add_column(iterator_up,column_header='i')
result_up.add_column(NLR_up,column_header='NLR')
result_up.sort('i')


offset = (max(result_up.column('NLR'))+min(result_up.column('NLR')))/2

###Plot###
#plt.title('NLR vs H of SC004_2_T\n from linear fit to NLIV',verticalalignment='bottom')
plt.xlabel('$\mu_o$H (T)',labelpad=10)
plt.ylabel(r'R$_s$ (mV/A)',labelpad=10)
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.hold(True)

#plt.plot(result_up.column('Field'),1e3*(result_up.column('NLR')),'-ob',label = '280 K')
#plt.plot(result_down.column('Field'),1e3*(result_down.column('NLR')),'-or')

plt.plot(result_up.column('Field'),1e3*(result_up.column('NLR')),'-ob',label = '5 K')
plt.plot(result_down.column('Field'),1e3*(result_down.column('NLR')),'-or')




plt.legend()
plt.tight_layout()
plt.show()


















