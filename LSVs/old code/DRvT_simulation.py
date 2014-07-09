# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 09:25:53 2014

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


# Import Delta R data for SC004_2_T L=350 nm
DR = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaR_vs_Sep/SC004_4_B_DeltaRvsT.txt')
L = 650e-9
# Import Lambda_N and P data from fits
fit_data = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Spindiffusionlength_from_data.txt')

Lam = interpolate.interp1d(fit_data.column('Temperature'),fit_data.column('Lambda_Cu'))
#Pol = interpolate.interp1d(fit_data.column('Temperature'),fit_data.column('P'))

#Import Pol from sinle param fit
POL = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DR_simlulations/Fits with lam 1 over rho/Pol_from_data.txt')
Pol = interpolate.interp1d(POL.column('Temperature'),POL.column('P'))

# Importresistivity Data
Py = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Py Res/RN200_1um_rhovT_.txt')
Py.sort('Temperature')
Py.mulitply(r'$\rho$ ($\mu \Omega$ cm)',1e-8,replace=True,header=r'$\rho$ ($\Omega$ m)')
PyR = interpolate.interp1d(Py.column('Temperature'),Py.column(r'$\rho$ ($\Omega$ m)'))

Cu = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Cu spacer resistance/Resistivity/SC004_2_T_Cu_resistivity_vs_T.txt')
Cu.sort('T (K)')
CuR = interpolate.interp1d(Cu.column('T (K)'),Cu.column(r'$\rho$ ($\Omega$m)'))


T = numpy.arange(10.0,240.0,1.0)




P =Pol(T)

Wpy = 150e-9
Wcu = 150e-9
Tcu = 130e-9    
PyRes = PyR(T)
CuRes = CuR(T)


Lambda_N = 1.59e-14/CuR(T)#Lam(T)
Lambda_F = 5e-9*(PyR(10)/PyR(T))
'''

Lambda_N = 0.7e-4/(T+100)
Lambda_F = 0.6e-6/(T+100)
'''


Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
Rn = (CuRes*Lambda_N)/(Wcu*Tcu)   
model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))

Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))


p=SP.PlotFile()
p.add_column(T,column_header='Temperature (K)')
p.add_column(model_tak,column_header=r'$\Delta$ R')
p.add_column(Lambda_N,column_header=r'$\lambda_{Cu}$')
p.setas="x.y"
p.template=SPF.JTBPlotStyle
title = ''
label = r'$\lambda_{Cu} = \frac{1.59 \times 10^{-14}} { \rho_{Cu}}$'
p.plot(label=label,figure=1,title=title)


'''
q=SP.PlotFile(DR)
q.rename('Delta',r'$\Delta \alpha$ (V/A)')
q.rename('Temp','Temperature (K)')
q.setas="y.x"
q.template=SPF.JTBPlotStyle
title = ''
label = ''
q.plot(label=label,figure=1,title=title)

'''











