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

ScuT = numpy.array([[0.000000,0.000010],
[21.516088,0.302055],
[25.651305,0.572288],
[29.100301,0.775845],
[33.240838,1.007481],
[35.658327,1.126813],
[39.114093,1.281247],
[42.225057,1.414624],
[46.040618,1.481344],
[49.514761,1.502445],
[53.686731,1.506012],
[58.209791,1.485023],
[62.388048,1.442977],
[65.871379,1.397412],
[72.489854,1.309785],
[78.760625,1.222154],
[82.593111,1.166068],
[91.300231,1.060927],
[100.697924,0.990884],
[108.698995,0.962926],
[120.872037,0.938536],
[136.171517,0.935242],
[151.814350,0.963531],
[165.023251,0.991787],
[178.925143,1.037596],
[194.910845,1.100978],
[207.419984,1.160802],
[223.750972,1.241733],
[237.301775,1.312099],
[247.377467,1.368380]])

SpyTbulk = numpy.array([[0.000000,0.000000],
[5.336256,-0.345924],
[10.778056,-0.736119],
[16.223007,-1.301498],
[21.669533,-1.954469],
[25.155624,-2.389889],
[29.078856,-2.956379],
[33.655828,-3.609984],
[36.707930,-4.089517],
[41.068301,-4.787077],
[48.262599,-5.920533],
[53.057747,-6.617775],
[58.725600,-7.489567],
[62.214842,-8.100170],
[68.972787,-9.146351],
[78.783622,-10.715861],
[88.375494,-12.197938],
[97.750765,-13.723970],
[106.690471,-15.206523],
[113.887919,-16.515162],
[118.467254,-17.300155],
[300.467254,-20.00155]])

Seperation = {2:425e-9,
              3:525e-9,
              4:625e-9,
              5:725e-9,
              6:925e-9,
              7:1125e-9,
              8:1325e-9,}

Sc = interpolate.interp1d(ScuT[:,0],ScuT[:,1])
Sp = interpolate.interp1d(SpyTbulk[:,0],SpyTbulk[:,1])
              
# define objective function: returns the array to be minimized
def fcn2min(params, TD, x, t):
    """ model NLIV """
    m = params['m'].value
    c = params['c'].value
    model = m*(x) + c 
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
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Beta_vs_sep',pattern = pattern)
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
T = numpy.arange(6.0,270.0,1.0)
I = 300e-6

intercept = []
DeltaT = []
T_d = []
l = []
for t in T:
    
    Spc = ((-0.01411*t)-0.11185)*1e-6
    #Spc = (Sp(t)-Sc(t))*1e-6
    TD = []
    
    for i in range(len(seperation)):
        beta = -1*float(beta_interp[i](t))
        Td = t + ((beta*I*I)/Spc)
        TD.append(Td)
        
      
    # do fit, here with leastsq model
    result = minimize(fcn2min, params, args=(numpy.array(TD), numpy.array(seperation), t))
    # calculate final result
    final = TD + result.residual
    # write error report
    report_fit(params)
    intercept.append(params['c'].value)
    DeltaT.append(params['c'].value-TD[1]) 
    T_d.append(TD[0])

temp = Stoner.DataFile()
Ti = numpy.array(intercept,dtype='d')

temp.add_column(T,'T (K)')
temp.add_column(Ti,'Ti')
temp['Sample ID'] = 'SC004_2_T'
print temp
temp.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/'+temp['Sample ID']+'_TivsT.txt')

plt.ylabel('$\Delta$T')
plt.xlabel('T (K)')
#plt.plot(T,T_d-T,'ob')
#plt.plot(sep,final,'-r')
plt.plot(T,intercept-T)
#plt.plot(T,numpy.array(intercept)-numpy.array(T_d),'o',label = 'SC004_8')
plt.legend(loc='upper right')






