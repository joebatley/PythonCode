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


folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC021/SC021_1_B/6221-2182 DC IV/High_Field_8T_5K-IV_Data', pattern = '*.txt') 


############ Calculate Delta R with error ############


pRs = []
perr = []
nRs = []
nerr = []
F = []
folder.sort('iterator')
for f in folder:
  a = Analysis.AnalyseFile(f)
  fitp = a.curve_fit(quad,'Current','Voltage',p0=[20.0,1e-7,0.0],bounds=lambda x,y:x>0, result=True, replace=False, header="fit",asrow=True)
  fitn = a.curve_fit(quad,'Current','Voltage',p0=[20.0,1e-7,0.0],bounds=lambda x,y:x<0, result=True, replace=False, header="fit",asrow=True)  
  pRs.append(fitp[2])
  perr.append(fitp[3])
  nRs.append(fitn[2])
  nerr.append(fitn[3])
  F.append(a['Magnet Output'])
  
#Mean = (max(Rs)+min(Rs))/2
#offset = (max(Rs)+min(Rs))/2

RS = Analysis.AnalyseFile()
RS.add_column(F,'H ($\mu_o$T)')
RS.add_column(pRs,'pR$_s$ (mV/A)')
RS.add_column(perr,'perr')
RS.add_column(nRs,'nR$_s$ (mV/A)')
RS.add_column(nerr,'nerr')
#RS.subtract('R$_s$ (mV/A)',offset,replace=True,header='R$_s$ (mV/A)')
#RS.mulitply('R$_s$ (mV/A)',1e3,replace=True,header='R$_s$ (mV/A)')

#AP = RS.search('R$_s$ (mV/A)',lambda x,y: x<Mean,'R$_s$ (mV/A)')
#P = RS.search('R$_s$ (mV/A)',lambda x,y: x>Mean,'R$_s$ (mV/A)')

#DR = numpy.mean(P)-numpy.mean(AP)
#DRerr = (numpy.std(P)**2+numpy.std(AP)**2)**0.5




################ plot Data ##################


p=SP.PlotFile(RS)
print p.column_headers
#p.setas="xy"
p.template=SPF.JTBPlotStyle
label = None
title = ' '
p.plot_xy('H',['pR','nR'],plotter=errorbar,yerr=['perr','nerr'],label = label,title=title,figure=1)
























