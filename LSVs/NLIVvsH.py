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


folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_2_T/NLIVvsHat5K/', pattern = '*.txt') 


############ Calculate Delta R with error ############

Rs = []
Rserr = []
F = []
folder.sort('iterator')
for f in folder:
  a = Analysis.AnalyseFile(f)
  fit = a.curve_fit(quad,'Current','Voltage',p0=[20.0,1e-7,0.0], result=True, replace=False, header="fit",asrow=True)
  Rs.append(fit[2])
  F.append(a['Magnet Output']*1e-9)
  Rserr.append(fit[3])
  
Mean = (max(Rs)+min(Rs))/2
offset = (max(Rs)+min(Rs))/2

RS = Analysis.AnalyseFile()
RS.add_column(F,r'$\mu_o$H (mT)')
RS.add_column(Rs,'R$_s$ (V/A)')
RS.add_column(Rserr,'Rserr')

RS.subtract('R$_s$ (V/A)',offset,replace=True,header=r'$\alpha$ (V/A)')
RS.multiply(r'$\alpha$ (V/A)',1e3,replace=True,header=r'$R_s$ (mV/A)')
RS.multiply('Rserr',1e3,replace=True,header='Rserr')

'''
AP = RS.search(r'$\alpha$ (mV/A)',lambda x,y: x<Mean,r'$\alpha$ (mV/A)')
P = RS.search(r'$\alpha$ (mV/A)',lambda x,y: x>Mean,r'$\alpha$ (mV/A)')

DR = numpy.mean(P)-numpy.mean(AP)
DRerr = (numpy.std(P)**2+numpy.std(AP)**2)**0.5

print DR,DRerr
'''


################ plot Data ##################


p=SP.PlotFile(RS)
p.setas="xye"
p.template=SPF.JTBPlotStyle
label = '2 K'
title = ' '
p.plot(label = None,title=title,figure=1,color='k')
p.show()


q=SP.PlotFile(RS)
q.setas="xye"
q.template=SPF.JTBPlotStyle
label = '2 K'
title = ' '
q.plot(label = '5 K',title=title,figure=1,color='k')
q.show()




















