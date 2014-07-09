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
    a[i]=ph[0]
    b[i]=sd[0]
    c[i]=ee[0]
    
  model3 =  rho_0 + K * ((t/Dt)**5) * a + K * ((t/Dt)**3) * b + K * ((t/Dt)**2) * c
  model2 =  rho_0 + K * ((t/Dt)**5) * a + K * ((t/Dt)**3) * b 
  model1 =  rho_0 + K * ((t/Dt)**5) * a 
  return model1-rho


################ IMPORT FILE #######################

R = Analysis.AnalyseFile('/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Cu spacer resistance/Resistivity/SC004_Cu_Avg_Resistivity.txt')

L = Analysis.AnalyseFile('/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Spindiffusionlength_from_data.txt')

################ FIT RESISTANCE DATA #######################

# create a set of Parameters
params = Parameters()
params.add('K', value= 9e-8,min=0.5e-8,max=5e-7)
params.add('Dt', value= 190,min=100,max=500)
params.add('rho_0', value= 2.9e-8,min=0.5e-8,max=10e-8)


# do fit, here with leastsq model
result = minimize(BG, params, args=(R.column('T (K)'), R.column(r'$\rho$ ($\Omega$m)')))

# calculate final result
final = R.column(r'$\rho$ ($\Omega$m)') + result.residual
R.add_column(final,column_header='fit')

# write error report
report_fit(params)


################ GET SCATTERING TIME #######################

rho = R.interpolate(L.column('Temp'))
tsf = L.column('Lambda_Cu')**2*rho[:,0]*1.6e-19*1.81e28

tau = Analysis.AnalyseFile()
tau.add_column(L.column('Temp'),'T (K)')
tau.add_column(1/tsf,r'1/$\tau_{sf}$')



################ FIT SCATTERING TIME #######################
def phonon(sc_params,t,tau):
    func_ph = lambda x:(x**5)/((numpy.exp(x)-1)*(1-numpy.exp(-x))) 
    K = params['K'].value
    Dt = params['Dt'].value 
    e = sc_params['epsilon'].value    
    i = sc_params['imp'].value    
    a=numpy.ones(len(t))
    for j in range(len(t)):
        ph = quad(func_ph,0,(Dt/t[j]))
        a[j] = ph[0]
    
    rho_ph = K * ((t/Dt)**5) * numpy.array(a)
    tau_ph_sf = ((e*8.45e28*(1.6e-19**2)*rho_ph)/9.1e-31)+i
    return tau_ph_sf-tau

# create a set of Parameters
sc_params = Parameters()
sc_params.add('epsilon', value= 9e20)
sc_params.add('imp', value= 1e9)


# do fit, here with leastsq model
q=SP.PlotFile(tau.clone)

d = Analysis.AnalyseFile(tau.clone)
d.del_rows('T (K)',lambda x,y:x<40)

sc_result = minimize(phonon, sc_params, args=(d.column('T (K)'), d.column(r'1/$\tau_{sf}$')))

# calculate final result
sc_final = (d.column(r'1/$\tau_{sf}$')) + sc_result.residual
d.add_column(sc_final,column_header='fit')

# write error report
report_fit(sc_params)

def kondo(x,a,b,c):
    return a + b*numpy.log(c/x)
    
tau.curve_fit(kondo,'T (K)',r'1/$\tau_{sf}$',p0=[1e10,1,1],bounds=lambda x,y:x<40,result=True,header='fit')

print tau
################ PLOT SCATTERING DATA #######################
qd=SP.PlotFile(d.clone)              
qd.template=SPF.JTBPlotStyle
title = None
label = 'fit'
qd.plot_xy('T (K)','fit',label=label,figure=2,title=title)


q=SP.PlotFile(tau.clone)              
q.template=SPF.JTBPlotStyle
title = None
label = ''
q.plot_xy('T (K)',[r'1/$\tau_{sf}$','fit'],label=label,figure=2,title=title)



################ PLOT B-G DATA #######################

#R.subtract(r'$\rho$ ($\Omega$m)','fit',replace=False,header='Diff')
R.add_column(1/R.column(r'$\rho$ ($\Omega$m)'),'1/rho')
R.add_column(1/R.column('fit'),'1/fit')

p=SP.PlotFile(R.clone)               
p.template=SPF.JTBPlotStyle
title = None
label_fit='B-G fit\n K = ' + str(params['K'].value) + '\n'+r'$\theta_D$ = ' + str(params['Dt'].value) + '\n'+r'$\rho_0$ = ' + str(params['rho_0'].value)
label = 'data'

#p.plot_xy('T (K)','Diff',label=label_fit,figure=1,title=title)
p.plot_xy('T (K)',['1/rho','1/fit'],label=label_fit,figure=1,title=title)
#p.plot_xy('T (K)','fit',label=label_fit,figure=1,title=title)
#p.plot_xy('T (K)',r'$\rho$ ($\Omega$m)',label=label,figure=1,title=title)



