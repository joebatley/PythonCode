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
def avg(x):
  return numpy.mean(x)
########## Find Mean Rs ##########

filedir = '/Users/Joe/PhD/Measurements/SC020/Transport/SC020_1_B/6221-2182 DC IV/NLRvsHvsT/'
filename = 'SC020_1_B_6221-2182 DC IV_Magnet Power Supply Multi-segment_0150 0.00_1.864800K_NLRvsH.txt'
file = Stoner.DataFile(filedir+filename)

a=Analysis.AnalyseFile(file)
mean = (a.max('b')[0]+a.min('b')[0])/2


########## Import IV Data ##########
folder = DataFolder('/Users/Joe/PhD/Measurements/SC020/Transport/SC020_1_B/6221-2182 DC IV/2K-IV_Data', pattern = '*.txt') 

print folder
########## Seperate IVs into P and AP ##########

P = Analysis.AnalyseFile()
AP = Analysis.AnalyseFile()

for f in folder:
  a = Analysis.AnalyseFile(f)
  fit = a.curve_fit(quad,'Current','Voltage',p0=[20.0,1e-7,0.0], result=True, replace=False, header="fit",asrow=True)
  if fit[2]>mean:
    P.add_column(f.column('Voltage'),str(f['Control:Magnet']))
  else:
    AP.add_column(f.column('Voltage'),str(f['Control:Magnet']))




########## Average P and AP state IVs ##########
alpha = 1e6
beta = 1e6
print P
  
P.apply(avg,0,replace=False,header='V$_{NL}$ (V)')
P.multiply('V$_{NL}$ (V)',alpha,header='V$_{NL}$ ($\mu$V)')
P.add_column(f.column('Current'),'Current')
P.multiply('Current',beta,header='I ($\mu$A)')

AP.apply(avg,0,replace=False,header='V$_{NL}$ (V)')
AP.multiply('V$_{NL}$ (V)',alpha,header='V$_{NL}$ ($\mu$V)')
AP.add_column(f.column('Current'),'Current')
AP.multiply('Current',beta,header='I ($\mu$A)')


################ plot Data ##################


p=SP.PlotFile(P)
print P.column_headers
p.template=SPF.JTBPlotStyle
label = 'P'
title = ' '
p.plot_xy('I ($\mu$A)','V$_{NL}$ ($\mu$V)',label = label,title=title,figure=1)

q=SP.PlotFile(AP)
q.template=SPF.JTBPlotStyle
label = 'AP'
title = ' '
q.plot_xy('I ($\mu$A)','V$_{NL}$ ($\mu$V)',label = label,title=title,figure=1)
























