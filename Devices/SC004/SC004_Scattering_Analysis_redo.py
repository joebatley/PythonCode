# -*- coding: utf-8 -*-
"""
Code to fit spin diffusion length data and anylise the different scattering terms.

Includes bloch-gruneissen fit to the LSV spacer resistivity to extract electronic scattering contributions.

@author: py07jtb
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


### Function to fit BG equation to the resistivity ###
def BG(params,t,rho):
  K = params['K'].value
  Dt = params['Dt'].value
  j = params['j'].value
  
  a=numpy.ones(len(t))
  for i in range(len(t)):
    func_ph = lambda x:(x**5)/((numpy.exp(x)-1)*(1-numpy.exp(-x)))
    ph = quad(func_ph,0,(Dt/t[i]))
    a[i]=ph[0]
    
  phonon =  K * ((t/Dt)**5) * a #BG phonon contribution
  kondo = -j*numpy.log(t)       #Kondo magnetic scatterin term
  
  model = phonon + kondo
  return model-rho
  
### FIT SCATTERING TIME ###
def scatter(sc_params,t,tau):
    func_ph = lambda x:(x**5)/((numpy.exp(x)-1)*(1-numpy.exp(-x))) 
    K = res_params['K'].value
    Dt = res_params['Dt'].value 
    rho_0 = min(R.column('res'))  
    j = res_params['j'].value
    
    e = sc_params['e_ph'].value    
    i = sc_params['e_imp'].value 
    m = sc_params['e_m'].value 
 
    a=numpy.ones(len(t))
    for jj in range(len(t)):
        ph = quad(func_ph,0,(Dt/t[jj]))
        a[jj] = ph[0]
            
    rho_ph = K * ((t/Dt)**5) * numpy.array(a)
    rho_m = -j*numpy.log(t) 

    tau_sf = ((8.45e28*1.6e-19**2)/9.1e-31)*((e*rho_ph)+(m*rho_m)+(i*rho_0))
    return (tau_sf-tau)
  
  
### IMPORT FILE ###
sample = 'SC004'
datadir = '/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Scattering/'

R = workfile(datadir+'SC004_5_B_Cu_resistivity_vs_T.txt')       #Resistivity of LSV spacer
R.rename(r'$\rho$ ($\Omega$m)','res')

L = workfile(datadir+'SC004_Spindiffusion_length_vs_T.txt')     #Spin diffusion length data
  
  
### FIT RESISTANCE DATA ### Fit data to get electron relaxation terms

# create a set of Parameters
res_params = Parameters()
res_params.add('K', value= 1.309e-7,min=1e-8,max=1e-6,vary=False)
res_params.add('Dt', value= 288,min=250,max=400,vary=False)
res_params.add('j', value= 7e-12,min=7e-12,max=5e-6,vary=False)

R.subtract('res',min(R.column('res')),header='res.norm')        #subtract off the minimum (residual) to help Kondo fit

# do fit, here with leastsq model
result = minimize(BG, res_params, args=(R.column('T (K)'), R.column('res.norm')))

# calculate final result
final = R.column('res.norm') + result.residual + min(R.column('res'))
R.add_column(final,column_header='fit')

# write error report
report_fit(res_params)

### Print output parameters from fit ###
print 'K = ' + format_error(res_params['K'].value,res_params['K'].stderr,latex=True)
print 'Dt = ' + format_error(res_params['Dt'].value,res_params['Dt'].stderr,latex=True)
print 'rho0 = ' + str(min(R.column('res'))) 
  
### Plot resistivity data ###
R.template=SPF.JTBPlotStyle
R.figure(1)
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


R.multiply('res',1e8,replace=False,header='res.plot')         #Convert to micro Ohm cm
R.multiply('fit',1e8,replace=False,header='fit.plot')
R.plot_xy('T (K)','res.plot',linestyle='',linewidth=3,marker='o',markersize=5,label=None)
R.plot_xy('T (K)','fit.plot',linestyle='-',linewidth=2,marker='',label=None)
R.ylabel = r'$\rho\ (\mu\Omega cm)$'
plt.tight_layout()
  
  
  
### GET SCATTERING TIME ###

rho = R.interpolate(L.column('T'),xcol='T (K)')

tsf = (L.column('Lam_Cu')**2)*rho[:,4]*1.6e-19*1.81e28
tau = workfile()
tau.add_column(L.column('T'),'T (K)')
tau.add_column(1/tsf,'1/tsf')
tau.add_column(tsf,'tsf')
tau_err = (2*L.column('Lam_err')/L.column('Lam_Cu'))*tsf
tau.add_column(tau_err,'t_err')
tau.add_column(tau_err/tsf**2,'1/t_err')  
  

### FIT SCATTERING TIME DATA ###

# create a set of Parameters
sc_params = Parameters()
sc_params.add('e_ph', value= 1.7e-1,min=0,vary=True)
sc_params.add('e_imp', value= 5e-4,min=0,vary=True)
sc_params.add('e_m', value=.3e-1 ,min=3e-4,vary=True)


# do fit, here with leastsq model

sc_result = minimize(scatter, sc_params, args=(tau.column('T (K)'), tau.column('1/tsf')))

# calculate final result
sc_final = (tau.column('1/tsf')) + sc_result.residual
tau.add_column(sc_final,column_header='1/t_fit')
tau.add_column(1/sc_final,column_header='t_fit')

# write error report
report_fit(sc_params)


### PRINT SPIN FLIP PROBABLITIES ###
e_ph = sc_params['e_ph'].value
e_ph_err = sc_params['e_ph'].stderr
print r'$\epsilon_ph$ = ' + str(e_ph) + '$\pm$' + str(e_ph_err)
print format_error(e_ph,e_ph_err,latex=True)

e_imp = sc_params['e_imp'].value#*9.1e-31/(8.45e28*(1.6e-19**2)*params['rho_0'].value)
e_imp_err = sc_params['e_imp'].stderr#e_imp*numpy.sqrt((sc_params['imp'].stderr/sc_params['imp'].value)**2 + (params['rho_0'].stderr/params['rho_0'].value)**2)
print r'$\epsilon_imp$ = ' + str(e_imp) + '$\pm$' + str(e_imp_err)
print format_error(e_imp,e_imp_err,latex=True)

e_m = sc_params['e_m'].value
e_m_err = sc_params['e_m'].stderr
print r'$\epsilon_m$ = ' + str(e_m) + '$\pm$' + str(e_m_err)
print format_error(e_m,e_m_err,latex=True)  
  
  
### PLOT SCATTERING DATA ###
tau.template=SPF.JTBPlotStyle
tau.figure(2)
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday

func_ph = lambda x:(x**5)/((numpy.exp(x)-1)*(1-numpy.exp(-x))) 
K = res_params['K'].value
Dt = res_params['Dt'].value 
rho_0 = min(R.column('res'))  
j = res_params['j'].value
    
e = sc_params['e_ph'].value    
i = sc_params['e_imp'].value 
m = sc_params['e_m'].value 

a=numpy.ones(len(tau.column('T (K)')))
for jj in range(len(tau.column('T (K)'))):
    ph = quad(func_ph,0,(Dt/tau.column('T (K)')[jj]))
    a[jj] = ph[0]
            
rho_ph = K * ((tau.column('T (K)')/Dt)**5) * numpy.array(a)
rho_m = -j*numpy.log(tau.column('T (K)'))
    
tau_ph = ((8.45e28*1.6e-19**2)/9.1e-31)*(e*rho_ph)
tau_m = ((8.45e28*1.6e-19**2)/9.1e-31)*(m*rho_m)
  
tau.add_column((tau_ph)*1e-12,'t_ph')
tau.add_column((tau_m)*1e-12,'t_m')  
tau.multiply('tsf',1e12,replace=False,header='tsf.plot')         #Convert to ps
tau.multiply('t_fit',1e12,replace=False,header='t_fit.plot')
tau.multiply('t_err',1e12,replace=False,header='t_err.plot')
tau.plot_xy('T (K)','tsf.plot', linestyle='',linewidth=3,marker='o',markersize=5,label=None)
tau.plot_xy('T (K)','t_fit.plot',linestyle='-',linewidth=2,marker='',label=None)
#tau.plot_xy('T (K)','t_ph',linestyle='-',linewidth=2,marker='',label=r'$\frac{1}{\tau_{sf}^{ph}}$')
#tau.plot_xy('T (K)','t_m',linestyle='-',linewidth=2,marker='',label=r'$\frac{1}{\tau_{sf}^{m}}$')
tau.ylabel = r'$\frac{1}{\tau_{sf}}$ (ps$^{-1}$)'
plt.tight_layout()  
plt.legend(loc='best')  
  
tau_e = 3/((1.57e6**2)*1.86e28*1.6e-19*rho[:,4]) 
lam =   1e9*(1.57e6*9.1e-31)/(1.86e28*1.6e-19**2*rho[:,4])
tau.add_column(1/tau_e,'tau_e')  
tau.add_column(lam,'lam')
  
tau.figure(3)
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


tau.multiply('tau_e',1e12,replace=False,header='tau_e.plot') 
tau.plot_xy('T (K)','lam',linestyle='',linewidth=3,marker='o',markersize=5,label=None)
#tau.ylabel = r'$\tau_{sf}$ (ps)'
#tau.xlabel = r'$\tau_{e}$ (ps)'
tau.ylabel = r'$\lambda_e$ (nm)'
plt.tight_layout()    
  
  
  