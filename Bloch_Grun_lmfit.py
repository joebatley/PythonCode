# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 10:44:51 2014

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


def BG(params,t,rho):
  K = params['K'].value
  K2 = params['K2'].value
  Dt = params['Dt'].value 
  rho_0 = params['rho_0'].value
  
  a=numpy.ones(len(t))
  b=numpy.ones(len(t))
  c=numpy.ones(len(t))
  for i in range(len(t)):
    func_ph = lambda x:(x**5)/((numpy.exp(x)-1)*(1-numpy.exp(-x)))#((numpy.sinh(x))**2)
    func_sd = lambda x:(x**3)/((numpy.exp(x)-1)*(1-numpy.exp(-x)))
    func_ee = lambda x:(x**2)/((numpy.exp(x)-1)*(1-numpy.exp(-x)))
    ph = quad(func_ph,0,(Dt/t[i]))
    sd = quad(func_sd,0,(Dt/t[i]))
    ee = quad(func_ee,0,(Dt/t[i]))
    a[i]=ph[0]  #Phonon scattering
    b[i]=sd[0]  # s-d scattering
    c[i]=ee[0]  # e-e scattering
    
  model3 =  rho_0 + K * ((t/Dt)**5) * a + K2 * ((t/Dt)**3) * b + K * ((t/Dt)**2) * c
  model2 =  rho_0 + K * ((t/Dt)**5) * a + K2 * ((t/Dt)**3) * b 
  model1 =  rho_0 + K * ((t/Dt)**5) * a 
  Py = model1 + K2 * t**2
  return Py-rho

R = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Blaatand/SC018_4/SC018_4_WA_1/6221-2182 DC IV/SC018_4_WA_1_6221-2182 DC IV_Timed interval_0000 0.00_RvsT_50uA.txt')

R.rename('Sample Temp','T (K)')
w = 200e-9
t = 30e-9
l = 35e-6
rho = w*t/l
R.mulitply('Resistance',rho,replace = False, header = r'$\rho (\Omega$m)')

# create a set of Parameters
params = Parameters()
params.add('K2', value= 9e-8,min=0.5e-8,max=50e-7)
params.add('K', value= 9e-8)
params.add('Dt', value= 400,min=100,max=500)
params.add('rho_0', value= 2.9e-8,min=0.5e-9,max=3.95e-6)


# do fit, here with leastsq model
result = minimize(BG, params, args=(R.column('T (K)'), R.column(r'$\rho (\Omega$m)')))

# calculate final result
final = R.column(r'$\rho (\Omega$m)') + result.residual
R.add_column(final,column_header='fit')

# write error report
report_fit(params)


R.subtract(r'$\rho (\Omega$m)','fit',replace=False,header='Diff')

p=SP.PlotFile(R.clone)               #PLOT
p.template=SPF.JTBPlotStyle
title = None
label_fit='SC018_4_WA_1 (1130nm) B-G fit:\n K = ' + '%s' % float('%.3g' % params['K'].value) + '\n'+r'$\theta_D$ = ' + '%s' % float('%.3g' % params['Dt'].value) + '\n'+r'$\rho_0$ = ' + '%s' % float('%.3g' % params['rho_0'].value) + '\n RRR = ' + '%s' % float('%.2g' % (max(R.column(r'$\rho (\Omega$m)'))/params['rho_0'].value))
label = 'data'

#p.plot_xy('T (K)','Diff',label=label_fit,figure=1,title=title)

p.plot_xy('T (K)','fit',label=label_fit,figure=1,title=title)
p.plot_xy('T (K)',r'$\rho (\Omega$m)',label=label,figure=1,title=title)



