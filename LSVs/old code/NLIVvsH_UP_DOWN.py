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
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP



 
def quad(x,a,b,c):
  return (a*x**2)+(b*x)+c


folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_2_T/NLIVvsHat280K', pattern = '*.txt') 


############ Calculate Delta R with error ############

Rs = []
F = []
folder.sort('iterator')
for f in folder:
  a = Analysis.AnalyseFile(f)
  fit = a.curve_fit(quad,'Current','Voltage',p0=[20.0,1e-7,0.0], result=True, replace=False, header="fit",asrow=True)
  Rs.append(fit[2])
  F.append(a['Magnet Output']*1e-9)
  
Mean = (max(Rs)+min(Rs))/2


RS = Analysis.AnalyseFile()
RS.add_column(F,'Field')
RS.add_column(Rs,'Rs')

AP = RS.search('Rs',lambda x,y: x<Mean,'Rs')
print AP
P = RS.search('Rs',lambda x,y: x>Mean,'Rs')

DR = numpy.mean(P)-numpy.mean(AP)
DRerr = (numpy.std(P)**2+numpy.std(AP)**2)**0.5

print DR
print DRerr




################ Fit and plot Data ##################


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

result_down = Analysis.AnalyseFile()
result_down.add_column(Field_down,column_header=r'$\mu_o$H (mT)')
result_down.add_column(iterator_down,column_header='i')
result_down.add_column(NLR_down,column_header=r'$\alpha$ (V/A)')
result_down.mulitply(r'$\alpha$ (V/A)', 1e3, replace=True, header=r'$\alpha$ (mV/A)')
result_down.sort('i')


result_up = Analysis.AnalyseFile()
result_up.add_column(Field_up,column_header=r'$\mu_o$H (mT)')
result_up.add_column(iterator_up,column_header='i')
result_up.add_column(NLR_up,column_header=r'$\alpha$ (V/A)')
result_up.mulitply(r'$\alpha$ (V/A)', 1e3, replace=True, header=r'$\alpha$ (mV/A)')
result_up.sort('i')


#offset = (max(result_up.column(r'$\alpha$'))+min(result_up.column(r'$\alpha$')))/2

###Plot###

print result_down.column_headers

p=SP.PlotFile(result_down)
p.setas="x.y"
p.template=SPF.JTBPlotStyle
label = None
title = ' '
p.plot(label = label,title=title,figure=1)

q=SP.PlotFile(result_up)
q.setas="x.y"
q.template=SPF.JTBPlotStyle
label = None
title = ' '
q.plot(label = label,title=title,figure=1)



















