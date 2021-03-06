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
sample = 'SC021'

datadir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC021/Transport/Scattering Analysis/'

R = Analysis.AnalyseFile(datadir+'SC021_1_B_Cu_resistivity_vs_T.txt')

L = Analysis.AnalyseFile(datadir+'SC021_Spindiffusion_length_vs_T.txt')

################ FIT RESISTANCE DATA #######################

# create a set of Parameters
params = Parameters()
params.add('K', value= 9e-8,min=0.5e-8,max=5e-7)
params.add('Dt', value= 190,min=100,max=500)
params.add('rho_0', value= 2.9e-8,min=0.5e-8,max=10e-8)


# do fit, here with leastsq model
result = minimize(BG, params, args=(R.column('T (K)'), R.column('res')))

# calculate final result
final = R.column('res') + result.residual
R.add_column(final,column_header='BG')

# write error report
report_fit(params)

print params['K']
################ GET SCATTERING TIME #######################

rho = R.interpolate(L.column('T'))
print R.column_headers
tsf = L.column('Lam_Cu')**2*rho[:,2]*1.6e-19*1.81e28

tau = Analysis.AnalyseFile()
tau.add_column(L.column('T'),'T (K)')
tau.add_column(1/tsf,r'1/$\tau_{sf}$')
tau_err = (L.column('Lam_err')/L.column('Lam_Cu'))/tsf
tau.add_column(tau_err,'1/t_err')


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
    return (tau_ph_sf-tau)

# create a set of Parameters
sc_params = Parameters()
sc_params.add('epsilon', value= 9e20)
sc_params.add('imp', value= 1e9)


# do fit, here with leastsq model
q=SP.PlotFile(tau.clone)

d = Analysis.AnalyseFile(tau.clone)
d.del_rows('T (K)',lambda x,y:x<100 and x>230)

sc_result = minimize(phonon, sc_params, args=(d.column('T (K)'), d.column(r'1/$\tau_{sf}$')))

# calculate final result
sc_final = (d.column(r'1/$\tau_{sf}$')) + sc_result.residual
d.add_column(sc_final,column_header='fit')

# write error report
report_fit(sc_params)

e_ph = sc_params['epsilon'].value
e_ph_err = sc_params['epsilon'].stderr
print r'$\epsilon_ph$ = ' + str(e_ph) + '$\pm$' + str(e_ph_err)
print format_error(e_ph,e_ph_err,latex=True)

e_imp = sc_params['imp'].value*9.1e-31/(8.45e28*(1.6e-19**2)*params['rho_0'].value)
e_imp_err = e_imp*numpy.sqrt((sc_params['imp'].stderr/sc_params['imp'].value)**2 + (params['rho_0'].stderr/params['rho_0'].value)**2)
print r'$\epsilon_imp$ = ' + str(e_imp) + '$\pm$' + str(e_imp_err)
print format_error(e_imp,e_imp_err,latex=True)

################ PLOT SCATTERING DATA #######################
fit=SP.PlotFile(d.clone)
fit.template=SPF.JTBPlotStyle 
t=SP.PlotFile(tau.clone)
t.template=SPF.JTBPlotStyle
BG=SP.PlotFile(R.clone) 
BG.template=SPF.JTBPlotStyle

fit.figure()
t.figure()
BG.figure()

f=plt.gcf()
f.set_size_inches((6.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


plt.subplot2grid((1,2),(0,0))
l = r'$\epsilon_{ph}$ = ' + format_error(e_ph,e_ph_err,latex=True) + '\n' + r'$\epsilon_{imp}$ = ' + format_error(e_imp,e_imp_err,latex=True)
t.plot_xy('T (K)',r'1/$\tau_{sf}$',yerr='1/t_err',linestyle='',linewidth=1,marker='o')
fit.plot_xy('T (K)','fit',label=l,linestyle='-',linewidth=2,marker='')
t.ylabel = r'1/$\tau_{sf}$'
t.title = sample


################ PLOT B-G DATA #######################

#label_fit='B-G fit\n K = ' + str(params['K'].value) + '\n'+r'$\theta_D$ = ' + str(params['Dt'].value) + '\n'+r'$\rho_0$ = ' + str(params['rho_0'].value)
#label = 'data'
plt.subplot2grid((1,2),(0,1))
BG.plot_xy('T (K)','res',linestyle='',linewidth=3,marker='o',label = r'Cu spacer $\rho$')
BG.plot_xy('T (K)','BG',linestyle='-',linewidth=2,marker='',label = 'B-G fit')
BG.ylabel = r'$\rho (\Omega m)$'
plt.tight_layout()

