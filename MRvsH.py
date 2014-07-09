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
#from lmfit import minimize, Parameters, Parameter, report_fit
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP


 
def quad(x,a,b,c):
  return (a*x**2)+(b*x)+c

def lin(x,m,c):
  return m*x+c


folder = DataFolder('/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Organics/Big Blue/Ross/B_MR_ii', pattern = '*.txt') 


############ Calculate Delta R with error ############

m = []
F = []
err = []

folder.sort('iterator')
for f in folder:
  a = Analysis.AnalyseFile(f)
  fit = a.curve_fit(lin,'Current','Voltage',p0=[20.0,0.0], result=True, replace=False, header="fit",asrow=True)
  m.append(fit[0])
  err.append(fit[1])
  F.append(a['Magnet Output'])
  
#Mean = (max(Rs)+min(Rs))/2
#offset = (max(Rs)+min(Rs))/2

MR = Analysis.AnalyseFile()
MR.add_column(F,r'$\mu_o$H (mT)')
MR.add_column(m,'R ($\Omega$)')
MR.add_column(err,'Rerr')

#MR.subtract('R$_s$ (V/A)',offset,replace=True,header=r'$\alpha$ (V/A)')
#MR.mulitply(r'$\alpha$ (V/A)',1e3,replace=True,header=r'$\alpha$ (mV/A)')

#AP = RS.search(r'$\alpha$ (mV/A)',lambda x,y: x<Mean,r'$\alpha$ (mV/A)')
#P = RS.search(r'$\alpha$ (mV/A)',lambda x,y: x>Mean,r'$\alpha$ (mV/A)')

#DR = numpy.mean(P)-numpy.mean(AP)
#DRerr = (numpy.std(P)**2+numpy.std(AP)**2)**0.5

#print DR,DRerr



################ plot Data ##################


p=SP.PlotFile(MR)
p.setas="xye"
p.template=SPF.JTBPlotStyle
label = 'MR at 0.244 K'
title = ' '
p.plot(label = label,title=title,figure=1)
























