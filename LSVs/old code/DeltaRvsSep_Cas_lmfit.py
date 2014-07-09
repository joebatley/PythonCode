# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 12:42:02 2014

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

fig_width_pt = 1000.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 42,
          #'axes.color_cycle':['b','r','k','g','p','c'],
          #'axes.formatter.limits' : [-7, 7],
          'text.fontsize': 36,
          'legend.fontsize': 24,
          'xtick.labelsize': 28,
          'ytick.labelsize': 28,
          'xtick.direction': 'in',
          'ytick.direction': 'in',
          'xtick.major.size':10,
          'ytick.major.size':10,
          'xtick.major.width':1,
          'ytick.major.width':1,
          'figure.figsize': fig_size,
         'font.family':'Arial',
         'xtick.major.pad':20,
         'ytick.major.pad':20,
         'font.size':32,
         'lines.linewidth':2,
         'lines.markersize':15,
         }
 
plt.rcParams.update(params)



DelR = numpy.array([[2.7412995E-7,1.9602897e-3],
[3.6587295E-7,1.635928e-3],
[4.349177E-7,1.27904e-3],
[6.0653764E-7,1.0964783e-3],
[7.897722E-7,0.8583656e-3],
[1.035783E-6,0.6812257e-3],
[1.5346881E-6,0.24863502e-3],
[2.032643E-6,0.14115156e-3],
[2.5192905E-6,0.07606467e-3],
[3.033871E-6,0.0545705e-3]])


              
# define objective function: returns the array to be minimized
def fcn2min(params, L, DRs):
    """ model NLIV """
    Lambda_N = params['Lambda_N'].value    
    P = params['P'].value
    
    Wpy = 135e-9
    Wcu = 170e-9
    Tcu = 100e-9    
    PyRes = 22.4e-8
    CuRes = 1.6e-8
    Lambda_F = 5e-9
  
  
    Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
    Rn = (CuRes*Lambda_N)/(Wcu*Tcu)   
    model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))
  
    Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
    Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
    model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
    model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))
  
    return model_Cas - DRs

# create a set of Parameters
params = Parameters()
params.add('Lambda_N', value= 1.9e-6)
params.add('P', value= 0.5)


# do fit, here with leastsq model
result = minimize(fcn2min, params, args=(DelR[:,0], DelR[:,1]))

# calculate final result
final = DelR[:,1] + result.residual

# write error report
report_fit(params)

print params['Lambda_N'].value, params['P'].value


L = numpy.arange(200e-9,3.5e-6,10e-9)
Lambda_N = params['Lambda_N'].value    
P = params['P'].value

Wpy = 135e-9
Wcu = 170e-9
Tcu = 100e-9    
PyRes = 22.4e-8
CuRes = 1.6e-8
Lambda_F = 5e-9


Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
Rn = (CuRes*Lambda_N)/(Wcu*Tcu)   
model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))

Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))



###Plot###
plt.title(r'')
plt.xlabel('Seperation (nm)')
plt.ylabel(r'$\Delta$R$_s$')
#plt.ticklabel_format(style = 'sci', useOffset = False)
#plt.tick_params(axis='both', which='minor')
plt.hold(True)
plt.plot(1e9*DelR[:,0], 1e3*DelR[:,1],'or',label = 'Casanova')
plt.plot(L*1e9,model_Cas*1e3,'-r',label = "$\lambda_s$ at 10 K = " + str.format("{0:.2g}", Lambda_N)) 
#plt.plot(1e9*DelR[:,0],1e3*final,'-g')
plt.tight_layout()
plt.show()






