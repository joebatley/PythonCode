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
          'axes.formatter.limits' : [-7, 7],
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



Seperation = {1:325e-9,
              2:425e-9,
              3:525e-9,
              4:625e-9,
              5:725e-9,
              6:925e-9,
              7:1125e-9,
              8:1325e-9,
              9:1525e-9,}
              
# define objective function: returns the array to be minimized
def fcn2min(params, TD, x, t):
    """ model NLIV """
    m = params['m'].value
    c = params['c'].value
    model = m*(1/x) + c 
    return model - TD
  
# Functionto interpolate each Beta vs T curve  
def interpSig(folder,keys):
  ''' 
  # Test interpolated data
  plt.xlabel('Temperature (K)')
  plt.ylabel(r'$\beta$ (V/A$^2$)')
  
  plt.plot(folder[0].column('Sample Temp'),folder[0].column('Beta'),'ob')  
  inter = interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('Beta'),kind = 'linear')
  T = numpy.arange(7,280,1)
  plt.plot(T,inter(T),'r')
  '''
  return beta_interp.append(interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('Beta'))),seperation.append(Seperation[folder[0]['L']])




# Import  Beta vs T data and group
pattern = re.compile('SC004_(?P<L>\d*)_(?P<Device>\w*)_BetavsT')
folder = DataFolder('/Volumes/stonerlab.leeds.ac.uk/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Beta_vs_sep',pattern = pattern)
folder.group('L')


# Walk groups and interpolate
beta_interp = []
seperation = []
folder.walk_groups(interpSig,group=True,replace_terminal=True)



# create a set of Parameters for fit
params = Parameters()
params.add('m',   value = -1.0)
params.add('c', value = 10.0)



# Plot Thermal diffusion fit for one temperature
t = 100
I = 300e-6
print I
print I**2
Spc = ((-0.01411*t)-0.11185)*1e-6
TD = []

for i in range(len(seperation)):
    beta = -1*float(beta_interp[i](t))
    print beta
    print beta*I**2
    Td = t + ((beta*I*I)/Spc)
    TD.append(Td)
  
# do fit, here with leastsq model
result = minimize(fcn2min, params, args=(numpy.array(TD), numpy.array(seperation), t))
# calculate final result
final = TD + result.residual
# write error report
report_fit(params)




sep = numpy.array(seperation)
T_d = numpy.array(TD)

plt.ylabel(' ')
plt.xlabel('Electrode seperation (nm)')
plt.plot(sep,T_d,'ob')
plt.plot(sep,final,'-r')
plt.legend(loc='upper right')






