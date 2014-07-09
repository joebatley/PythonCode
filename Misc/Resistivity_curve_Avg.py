# -*- coding: utf-8 -*-
"""
Created on Sat Jun  7 18:52:20 2014

@author: Joe
"""


import numpy
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


dir = '/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Cu spacer resistance/Resistivity/' 

folder = DataFolder(dir,pattern='*.txt')
print folder
T = numpy.arange(10,250,0.5)
avg = Analysis.AnalyseFile()
for f in folder:
    
    f.sort('T (K)')
    print f.column_headers
    a = Analysis.AnalyseFile(f.clone)
    a.interpolate(T)
    
    avg.add_column(a.column(r'$\rho$ ($\Omega$m)'))
    
avg.apply(lambda x: numpy.mean(x),0,replace=False,header=r'$\rho$ ($\Omega$m)')
avg.add_column(T,'T (K)')
avg.del_rows('T (K)',lambda x,y:x<5)

#avg.save(dir +'SC004_Cu_Avg_Resistivity.txt')

p=SP.PlotFile(avg.clone)               #PLOT
p.template=SPF.JTBPlotStyle
title = None
p.plot_xy('T (K)',r'$\rho$ ($\Omega$m)',label=None,figure=1,title=title)

