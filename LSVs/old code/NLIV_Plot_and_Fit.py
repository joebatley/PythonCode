
import re
import numpy
import time
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import pylab as plt
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
         'lines.markersize':10,
         }
 
plt.rcParams.update(params)

def func(x):
  return numpy.mean(x)

def quad(x,a,b,c,d):
  return (a*x**4)+(b*x**2)+(c*x)+d

####### IMPORT DATA ######

pattern = re.compile('_249K_(?P<state>\w*)_NLIV_300uA_')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_8_B/NLIVvsHvsT',pattern = pattern)

print folder
'''
avg = Analysis.AnalyseFile(folder[0])
avg.del_column('Voltage')
avg.del_column('Current')
avg.del_column('Column 2')
'''
avg = Analysis.AnalyseFile()
for f in folder:
  avg.add_column(f.Voltage,str(f.metadata['iterator']))
avg.apply(func, 1, replace = False, header = 'Mean NLVoltage')
avg.add_column(folder[1].column('Current'),'Current')
  


#fit = avg.curve_fit(quad,'Current','NLV',p0=[20,-10,1e-7,0], result=True, replace=False, header="fit")
#poly = avg.polyfit('Current','NLV',4,result=True)
#polyfit = (poly[0]*avg.column('Current')**4)+(poly[1]*avg.column('Current')**3)+(poly[2]*avg.column('Current')**2)+(poly[3]*avg.column('Current')**1)+poly[4]
#avg.subtract('Voltage','parabolic',replace=False,header='minus background')


# define objective function: returns the array to be minimized
def fcn2min(params, I, V):
    """ model NLIV """
    a = params['a'].value
    
    c = params['c'].value
    d = params['d'].value

    model = (a*I**2)+(c*I)+d
    return model - V

# create a set of Parameters
params = Parameters()
params.add('a',   value= -1000000)

params.add('c', value= 1e-6)
params.add('d', value= 0)


# do fit, here with leastsq model
result = minimize(fcn2min, params, args=(avg.column('Current'), avg.column('NLV')))

# calculate final result
final = avg.column('NLV') + result.residual

# write error report
report_fit(params)



###Plot###
plt.title(r'NLIV SC004_8_T at 60 K')
plt.xlabel('Current ($\mu$A)')
plt.ylabel(r'V$_{NL}$ ($\mu$V)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.hold(True)
plt.plot(1e6*avg.column('Current'),1e6*avg.column('NLV'),'-ob')
plt.plot(1e6*avg.column('Current'),1e6*final,'-r')
#plt.plot(avg.column('Current'),polyfit,'-k')
plt.tight_layout()
plt.show()



