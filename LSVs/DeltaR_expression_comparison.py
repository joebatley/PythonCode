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

DelR = numpy.array([[0.146e-6,2.75e-3],
[0.29e-6,1.97e-3],
[0.52e-6,1.17e-3],
[1.04e-6,0.65e-3],
[1.61e-6,0.4e-3]])


L = 250e-9

Lambda_N = numpy.arange(100e-9,1000e-9,1e-9)
P =  0.4

Wpy = 140e-9
Wcu = 220e-9
Tcu = 320e-9    
PyRes = 17.1e-8
CuRes = 0.69e-8
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
plt.xlabel('$\lambda$ (nm)')
plt.ylabel(r'$\Delta$R$_s$')
#plt.ticklabel_format(style = 'sci', useOffset = False)
#plt.tick_params(axis='both', which='minor')
plt.hold(True)
plt.plot(1/(1e9*Lambda_N),model_tak,'-r',label='tak')
plt.plot(1/(1e9*Lambda_N),model_Otani,'-b',label='Otani')
plt.tight_layout()
plt.show()






