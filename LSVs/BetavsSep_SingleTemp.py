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

K_Si = numpy.array([[0.0,0.0],
[11.245201,0.127662],
[18.419407,0.145956],
[24.052527,0.173345],
[30.710408,0.203781],
[36.852840,0.243322],
[41.970511,0.279816],
[50.158083,0.340636],
[59.372169,0.398430],
[67.561494,0.453176],
[84.449457,0.574822],
[97.243634,0.666057],
[111.578022,0.751235],
[121.816870,0.812075],
[135.132632,0.872948],
[146.909937,0.933804],
[159.204444,0.979481],
[172.519329,1.043390],
[191.985413,1.116472],
[209.408110,1.162201],
[230.413528,1.232262],
[255.012185,1.290211],
[279.612595,1.342087],
[305.239520,1.390936]])

NewK_Si = interpolate.interp1d(K_Si[:,0],K_Si[:,1])

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
def fcn2min(params, B, L, t,err):
    """ model NLIV """
    K = params['K'].value
    T_i = params['T_i'].value
    dz=params['dz'].value
    
    i = 300e-6
    Wcu = 150e-9
    Tcu = 130e-9
    A = Wcu*Tcu
    Ks = NewK_Si(t)
    As = 150e-9*25e-6
    PyRes = -PyR(t)*((30e-9*5e-6)/50e-6)
    R = -PyR(t)
    CuRes = CuR(t)*((130e-9*150e-9)/925e-9)
    Spc = ((-0.01411*t)-0.11185)*1e-6
    #a = Ks/(K*Tcu*dz)
    a = K/dz    
    T_d = (T_i-t)*numpy.exp(-a*L)+t
     
    model = Spc*(t-T_d)/(i*i)
    return (model - B)/err
  
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
  return interp.append(interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('Beta'))),Sep.append(Seperation[folder[0]['L']]),interperr.append(interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('Beta err')))


# Import and interpolate the resistivity data
Py = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaR_vs_Sep/RN200_5um_6221-2182 DC IV_Timed interval_RvT_500uA_.txt')
Py.sort('Sample Temp')
PyR = interpolate.interp1d(Py.column('Sample Temp'),Py.column('Resistance'))

Cu = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_6_T/SC004_6_T_6221-2182 DC IV_Timed interval_3.223900_RvT_CuBar_100uA.txt')
Cu.sort('Sample Temp')
CuR = interpolate.interp1d(Cu.column('Sample Temp'),Cu.column('Resistance'))


# Import  Beta vs T data and group
pattern = re.compile('SC004_(?P<L>\d*)_(?P<Device>\w*)_BetavsT')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Beta_vs_Sep',pattern = pattern)
folder.group('L')


# Walk groups and interpolate
interp = []
interperr = []
Sep = []
folder.walk_groups(interpSig,group=True,replace_terminal=True)



# create a set of Parameters for fit
params = Parameters()
params.add('K',   value = 4000.0,min=0)
params.add('T_i', value = 10.0,min=0)
params.add('dz', value = 1e-4,min=0)

T = numpy.arange(6,260,10)
KCu = []
Ti = []
Kerr = []
Tierr = []


# Plot Thermal diffusion fit for one temperature
t = 100
temp = []
temperr = []
for i in range(len(Sep)):
  temp.append(float(interp[i](t)))
  temperr.append(float(interperr[i](t)))

# do fit, here with leastsq model
result = minimize(fcn2min, params, args=(numpy.array(temp), numpy.array(Sep), t,temperr))

# calculate final result
final = interp[i](t) + result.residual

# write error report
report_fit(params)


d = numpy.arange(200e-9,1.2e-6,10e-9)
K = params['K'].value
T_i = params['T_i'].value
dz=params['dz'].value

i = 300e-6
dz=100e-9
Wcu = 150e-9
Tcu = 130e-9
A = Wcu*Tcu
Ks = NewK_Si(t)
As = 150e-9*15e-6
R = -PyR(t)
PyRes = -PyR(t)*((30e-9*5e-6)/50e-6)
CuRes = CuR(t)*((130e-9*150e-9)/925e-9)
Spc = ((-0.01411*t)-0.11185)*1e-6
#a = Ks/(K*Tcu*dz)
a = K/dz
T_d = (T_i-t)*numpy.exp(-a*d)+t
     
model = Spc*(t-T_d)/(i*i)

sep = numpy.array(Sep)
DR = numpy.array(temp)
plt.ylabel('$\Delta$R$_s$ (mV/A)')
plt.xlabel('Electrode seperation (nm)')
#plt.plot(sep,temp,'ob')
plt.plot(d,model,'-r',label = "$\lambda_s$ at " + str(t) + " K =  {} nm".format(format_error(params['K'].value,params['K'].stderr,latex=False)))
plt.legend(loc='upper right')






