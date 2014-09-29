# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 10:44:51 2014

@author: Joe
"""



import numpy
import pylab as plt
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
from Stoner.Util import format_error

class workfile(Analysis.AnalyseFile,SP.PlotFile):
    """A class that combines AnalyseFile and PlotFile together"""
    pass


def bloch(params,t,P,err):
  a = params['a'].value
  b = params['b'].value 
  
  model = a*(1-b*t**(3/2))  
  
  return (P-model)/err


### IMPORT FILE ###
sample = 'SC004'

L = workfile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Scattering/SC004_Spindiffusion_length_vs_T.txt')

print L.column_headers
### FIT RESISTANCE DATA ###

# create a set of Parameters
params = Parameters()
params.add('a', value= 0.5,min=0,max=1)
params.add('b', value= 2e-4)


# do fit, here with leastsq model
result = minimize(bloch, params, args=(L.column('T'), L.column('P'),L.column('P_err')))

# calculate final result
final = L.column('P') + result.residual
L.add_column(final,column_header='fit')

# write error report
report_fit(params)

a = params['a'].value
b = params['b'].value 
  
model = a*(1-b*L.column('T')**(3/2)) 
L.add_column(model,'model')

### PLOT SCATTERING DATA ###

L.template=SPF.JTBPlotStyle 
L.figure(1)

f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


L.plot_xy('T','P',yerr='P_err',linestyle='',linewidth=3,marker='o',markersize=5,label=None)
#L.plot_xy('T','fit',linestyle='-',linewidth=2,marker='',label=None)
L.plot_xy('T','model',linestyle='-',linewidth=2,marker='',label=None)
L.ylabel = r'$\alpha$'
L.xlabel = 'T (K)'
plt.tight_layout()

