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
import pylab as plt

class workfile(Analysis.AnalyseFile,SP.PlotFile):
    """A class that combines AnalyseFile and PlotFile together"""
    pass

def BG(params,t,rho):
  K = params['K'].value
  K2 = params['K2'].value
  Dt = params['Dt'].value 
  rho_0 = params['rho_0'].value
  j1 = params['j1'].value
  Tk = params['Tk'].value
  
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
  
  x1 = numpy.log(t/Tk)
  p = numpy.pi
  x2 = ((x1**2) + p**2)**0.5
  Py = model1 + j1*(1-(x1/x2))
  return Py-rho

datadir = '/Users/Joe/PhD/Measurements/SC004/Transport/Scattering/'

R = workfile(datadir+'SC004_Cu_Avg_Resistivity.txt')
R.rename(r'$\rho$ ($\Omega$m)',r'$\rho (\Omega$m)')


# create a set of Parameters
params = Parameters()
params.add('K2', value= 9e-8,min=0.5e-10,max=50e-7)
params.add('K', value= 9e-8)
params.add('Dt', value= 400,min=300,max=500)
params.add('rho_0', value= 2.65e-8,min=0.5e-9,max=3.95e-8)
params.add('j1', value= 0.9e-10,min=8e-11,max=1.5e-10,vary=True)
params.add('Tk', value= 22,min=25,max=27,vary=True)

# do fit, here with leastsq model
result = minimize(BG, params, args=(R.column('T (K)'), R.column(r'$\rho (\Omega$m)')))

# calculate final result
final = R.column(r'$\rho (\Omega$m)') + result.residual
R.add_column(final,column_header='fit')

# write error report
report_fit(params)


R.subtract(r'$\rho (\Omega$m)','fit',replace=False,header='Diff')



p=SP.PlotFile(R.clone) 
p.figure()
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True)              #PLOT
p.template=SPF.JTBPlotStyle
title = None
label_fit='SC018_4_WA_1 (1130nm) B-G fit:\n K = ' + '%s' % float('%.3g' % params['K'].value) + '\n'+r'$\theta_D$ = ' + '%s' % float('%.3g' % params['Dt'].value) + '\n'+r'$\rho_0$ = ' + '%s' % float('%.3g' % params['rho_0'].value) + '\n RRR = ' + '%s' % float('%.2g' % (max(R.column(r'$\rho (\Omega$m)'))/params['rho_0'].value))
label = 'data'

#p.plot_xy('T (K)','Diff',label=label_fit,figure=1,title=title)

p.plot_xy('T (K)','fit',label=label_fit,title=title)
p.plot_xy('T (K)',r'$\rho (\Omega$m)',label=label,title=title)



