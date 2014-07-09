# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:06:31 2014

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

fig_width_pt = 800.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 28,
          'axes.linewidth':2,
          'text.fontsize': 28,
          'title.fontsize':28,
          'legend.fontsize': 24,
          'xtick.labelsize': 28,
          'ytick.labelsize': 28,
          'xtick.direction': 'in',
          'ytick.direction': 'in',
          'xtick.major.size':10,
          'xtick.major.width':2,
          'ytick.major.size':10,
          'ytick.major.width':2,
          'figure.figsize': fig_size,
         'font.family':'Arial',
         'xtick.major.pad':20,
         'ytick.major.pad':20,
         'font.size':25,
         'lines.linewidth':4,
         'lines.markersize':15,}
 
plt.rcParams.update(params)


DelR = numpy.array([[0.146e-6,2.75e-3],
[0.29e-6,1.97e-3],
[0.52e-6,1.17e-3],
[1.04e-6,0.65e-3],
[1.61e-6,0.4e-3]])


# define objective function: returns the array to be minimized
def Rs(L,Lambda_N,Alpha):
  
  Wpy = 140e-9
  Wcu = 220e-9
  Tcu = 320e-9    
  PyRes = 17.1e-8
  CuRes = 0.69e-8
  Lambda_F = 5e-9
  Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
  Rn = (CuRes*Lambda_N)/(Wcu*Tcu)
   
  model = ((2*Alpha**2)/((1-Alpha**2)**2))*((Rf**2)/Rn)*(1/numpy.sinh(L/Lambda_N)) 
     
  #model = (2*(Alpha**2)*(Rsf**2)*(numpy.exp(-L/Lambda_N)))/(((CuRes*Lambda_N)/(Tcu*Wcu))*((1-(Alpha**2))**2)*(1-numpy.exp(-2*L/Lambda_N)))
  return model
  
def Rs_otani(L,Lambda_N,Alpha):
  
  Wpy = 140e-9
  Wcu = 220e-9
  Tcu = 320e-9    
  PyRes = 17.1e-8
  CuRes = 0.69e-8
  Lambda_F = 5e-9
  Rf = (2*PyRes*Lambda_F)/((1-Alpha**2)*Wpy*Wcu)
  Rn = (2*CuRes*Lambda_N)/(Wcu*Tcu)
   
  model = ((Alpha**2)*(Rf**2))/((2*Rf*numpy.exp(L/Lambda_N))+(Rn*numpy.sinh(L/Lambda_N)))
  
  return model


# Plot Spin diffusion fit for one temperature
t = 10

  
a = Analysis.AnalyseFile()
a.add_column(DelR[:,1],column_header = 'DeltaR')
a.add_column(DelR[:,0], column_header = 'L')  
print a
fit= a.curve_fit(Rs_otani,'L','DeltaR',p0=[1000e-9,0.5],bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
print fit

Alpha = fit[2]
Lambda_N = fit[0]
d = numpy.arange(100.0e-9,2.0e-6,10.0e-9)
Wpy = 140.0e-9
Wcu = 220.0e-9
Tcu = 320.0e-9    
PyRes = 17.1e-8
CuRes = 0.69e-8
Lambda_F = 5e-9
Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
Rn = (CuRes*Lambda_N)/(Wcu*Tcu)
#Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
#Rn = (CuRes*fit[0])/(Wcu*Tcu)


#model = ((2*(Alpha**2))/((1-(Alpha**2))**2))*((Rf**2)/Rn)*(1/numpy.sinh(d/Lambda_N))
#model = ((2*fit[2]**2)/((1-fit[2]**2)**2))*((Rf**2)/Rn)*(1/numpy.sinh(d/fit[0])) 
#model = (2*(fit[2]**2)*(Rsf**2)*(numpy.exp(-d/fit[0])))/(((CuRes*fit[0])/(Tcu*Wcu))*((1-(fit[2]**2))**2)*(1-numpy.exp(-2*d/fit[0])))


#Rf = (2*PyRes*Lambda_F)/((1-fit[2]**2)*Wpy*Wcu)
#Rn = (2*CuRes*fit[0])/(Wcu*Tcu)
 
#model = (fit[2]**2*Rf**2)/(2*Rf*numpy.exp(d/fit[0])+Rn*numpy.sinh(d/fit[0]))

Rf = (2*PyRes*Lambda_F)/((1-(Alpha**2))*Wpy*Wcu)
Rn = (2*CuRes*Lambda_N)/(Wcu*Tcu)
 
model = ((Alpha**2)*(Rf**2))/((2*Rf*numpy.exp(d/Lambda_N))+(Rn*numpy.sinh(d/Lambda_N)))

print a
plt.hold(True)
plt.ylabel('$\Delta$R$_s$ (mV/A)',labelpad=15)
plt.xlabel('Electrode seperation (nm)',labelpad=15)
plt.semilogy(1e9*a.L,1e3*a.DeltaR,'ob')
plt.semilogy(1e9*a.L,1e3*a.Fit,'or')
plt.semilogy(d*1e9,model*1e3,'-r',label = "$\lambda_s$ at " + str(t) + " K = " + str.format("{0:.2g}", fit[0])) 
#{} nm".format(format_error(fit[0],fit[1],latex=False)))
plt.legend(loc='upper right')
plt.tight_layout(pad=0.1, w_pad=0.0, h_pad=0.0)
plt.show





