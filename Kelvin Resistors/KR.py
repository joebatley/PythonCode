# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 15:17:55 2014

@author: py07jtb
"""

import numpy as np
from scipy import interpolate
from scipy.interpolate import splrep, splev
from scipy.integrate import quad
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize
from lmfit import minimize, Parameters, Parameter, report_fit
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP

R = np.array([1.183,0.847,0.5111,0.28727])
Rerr = np.array([0.003,0.004,0.0004,0.0004])
A = np.array([5.7e-14,8.9e-14,1.6e-13,2.0e-13])
Aerr = np.array([0.7e-14,0.9e-14,0.1e-13,0.1e-13])

a = Analysis.AnalyseFile()

a.add_column(R,column_header = r'R ($\Omega$)')
a.add_column(1/A,column_header = r'Area$^{-1}$ (m$^{-2}$)')


fit = a.polyfit(1,0,1,result = True, header = 'fit')

print 'RA = ' + str(fit[0]*1e15) + ' f$\Omega m^2$'

a.add_column(Rerr,column_header = r'R err')
a.add_column((Aerr/A)*(1/A),column_header = r'Area err')


p=SP.PlotFile(a.clone)               #PLOT
p.template=SPF.JTBPlotStyle
title = None
label_fit=''
label = ''

#p.plot_xy('T (K)','Diff',label=label_fit,figure=1,title=title)

p.plot_xy(r'Area$^{-1}$ (m$^{-2}$)','fit',label=label_fit,figure=1,title=title)
p.plot_xy(r'Area$^{-1}$ (m$^{-2}$)',r'R ($\Omega$)',plotter = errorbar,yerr= 'R err',xerr = 'Area err', label=label,figure=1,title=title)


