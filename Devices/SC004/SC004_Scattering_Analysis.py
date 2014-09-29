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


def BG(params,t,rho):
  K = params['K'].value
  Dt = params['Dt'].value 
  rho_0 = params['rho_0'].value
  j = params['j'].value
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
    a[i]=ph[0]
    b[i]=sd[0]
    c[i]=ee[0]
    
  model3 =  rho_0 + K * ((t/Dt)**5) * a + K * ((t/Dt)**3) * b + K * ((t/Dt)**2) * c
  model2 =  rho_0 + K * ((t/Dt)**5) * a + K * ((t/Dt)**3) * b 
  model1 =  rho_0 + K * ((t/Dt)**5) * a 
  x1 = numpy.log(t/Tk)
  p = numpy.pi
  x2 = ((x1**2) + (1.)*p**2)**0.5
  
  mag = model1 + j*(1-(x1/x2)) 
  return mag-rho


### IMPORT FILE ###
sample = 'SC004'

datadir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Scattering/'

R = workfile(datadir+'SC004_5_B_Cu_resistivity_vs_T.txt')
R.rename(r'$\rho$ ($\Omega$m)','res')

L = workfile(datadir+'SC004_Spindiffusion_length_vs_T.txt')

### FIT RESISTANCE DATA ###

# create a set of Parameters
params = Parameters()
params.add('K', value= 9e-8,min=0)
params.add('Dt', value= 350,min=32,max=500)
params.add('rho_0', value= 2.65e-8,min=0)
params.add('j', value= 7e-11,min=5e-11,max=5e-10,vary=True)
params.add('Tk', value= 10,min=5,max=50,vary=False)


# do fit, here with leastsq model
result = minimize(BG, params, args=(R.column('T (K)'), R.column('res')))

# calculate final result
final = R.column('res') + result.residual
R.add_column(final,column_header='BG')

# write error report
report_fit(params)



print 'K = '+format_error(params['K'].value,params['K'].stderr,latex=True)
print 'Dt = '+format_error(params['Dt'].value,params['Dt'].stderr,latex=True)
print 'rho0 = '+format_error(params['rho_0'].value,params['rho_0'].stderr,latex=True)
### GET SCATTERING TIME ###

rho = R.interpolate(L.column('T'))
tsf = L.column('Lam_Cu')**2*rho[:,2]*1.6e-19*1.81e28

tau = workfile()
tau.add_column(L.column('T'),'T (K)')
tau.add_column(1/tsf,r'1/$\tau_{sf}$')
tau_err = (L.column('Lam_err')/L.column('Lam_Cu'))/tsf
tau.add_column(tau_err,'1/t_err')


### FIT SCATTERING TIME ###
def phonon(sc_params,t,tau):
    func_ph = lambda x:(x**5)/((numpy.exp(x)-1)*(1-numpy.exp(-x))) 
    K = params['K'].value
    Dt = params['Dt'].value 
    rho_0 = params['rho_0'].value    
    j = params['j'].value
    Tk = params['Tk'].value 
    
    e = sc_params['epsilon'].value    
    i = sc_params['imp'].value 
    m = sc_params['m'].value 
 
    a=numpy.ones(len(t))
    for jj in range(len(t)):
        ph = quad(func_ph,0,(Dt/t[jj]))
        a[jj] = ph[0]
    
    rho_ph = K * ((t/Dt)**5) * numpy.array(a)

    x1 = numpy.log(t/Tk)
    p = numpy.pi
    x2 = ((x1**2) + (1.)*p**2)**0.5
    rho_m = j*(1-(x1/x2)) 

    tau_ph_sf = ((8.45e28*1.6e-19**2)/9.1e-31)*((e*rho_ph)+(m*rho_m)+(i*rho_0))
    return (tau_ph_sf-tau)

# create a set of Parameters
sc_params = Parameters()
sc_params.add('epsilon', value= 1.7e-1,min=0,vary=True)
sc_params.add('imp', value= 5e-4,min=0,vary=True)
sc_params.add('m', value=.3e-3 ,min=6e-2,vary=True)


# do fit, here with leastsq model
q=tau.clone

d = tau.clone
#d.del_rows('T (K)',lambda x,y:x<39)

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

e_imp = sc_params['imp'].value#*9.1e-31/(8.45e28*(1.6e-19**2)*params['rho_0'].value)
e_imp_err = sc_params['imp'].stderr#e_imp*numpy.sqrt((sc_params['imp'].stderr/sc_params['imp'].value)**2 + (params['rho_0'].stderr/params['rho_0'].value)**2)
print r'$\epsilon_imp$ = ' + str(e_imp) + '$\pm$' + str(e_imp_err)
print format_error(e_imp,e_imp_err,latex=True)

e_m = sc_params['m'].value
e_m_err = sc_params['m'].stderr
print r'$\epsilon_m$ = ' + str(e_m) + '$\pm$' + str(e_m_err)
print format_error(e_m,e_m_err,latex=True)

### PLOT SCATTERING DATA ###
fit=d.clone
fit.template=SPF.JTBPlotStyle 
t=tau.clone
t.template=SPF.JTBPlotStyle
BG=R.clone 
BG.template=SPF.JTBPlotStyle

fit.figure(1)
t.figure(1)

f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday



#l = r'$\epsilon_{ph}$ = ' + format_error(e_ph,e_ph_err,latex=True) + '\n' + r'$\epsilon_{imp}$ = ' + format_error(e_imp,e_imp_err,latex=True)
tau_sf = (1/t.column(r'1/$\tau_{sf}$'))*1e12
tau_sf_err = (t.column(r'1/t_err')/t.column(r'1/$\tau_{sf}$'))*tau_sf
t.add_column(tau_sf,'tau_sf')
t.add_column(tau_sf_err,'tau_sf_err')
#plt.subplot(2,1,1)
t.plot_xy('T (K)','tau_sf',yerr='tau_sf_err',linestyle='',linewidth=1,marker='o',markersize=5)

tau_fit = (1/fit.column('fit'))*1e12
fit.add_column(tau_fit,'tau_fit')
fit.plot_xy('T (K)','tau_fit',label=None,linestyle='-',linewidth=2,marker='')
t.ylabel = r'$\tau_{sf}$ (ps)'


### PLOT B-G DATA ###

#label_fit='B-G fit\n K = ' + str(params['K'].value) + '\n'+r'$\theta_D$ = ' + str(params['Dt'].value) + '\n'+r'$\rho_0$ = ' + str(params['rho_0'].value)
#label = 'data'
BG.figure(2)

f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday

#plt.subplot(2,1,2)
BG.multiply('res',1e8,replace=True,header='res')
BG.divide('res',min(BG.column('res')),header='res.norm')
BG.divide('BG',min(BG.column('BG')),header='BG.norm')
BG.plot_xy('T (K)','res.norm',linestyle='',linewidth=3,marker='o',markersize=5,label=None)#,label = r'Cu spacer $\rho$')
BG.multiply('BG',1e8,replace=True,header='BG')
BG.plot_xy('T (K)','BG.norm',linestyle='-',linewidth=2,marker='',label=None)#,label = 'B-G fit')
BG.ylabel = r'$\rho (\mu\Omega cm)$'
plt.tight_layout()

