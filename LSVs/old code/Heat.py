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

K_Cu =  numpy.array([[0,0],
[1.400009,1.092419],
[2.798056,2.418300],
[3.573732,3.275956],
[4.505982,4.133937],
[9.949443,8.503286],
[12.438929,10.376189],
[15.394212,12.716993],
[19.918499,14.671941],
[23.043431,15.456650],
[29.465558,15.158688],
[36.054719,13.615915],
[42.022816,11.449274],
[49.402035,9.052095],
[56.458955,7.743759],
[63.984288,6.592041],
[74.327290,5.523992],
[89.363573,4.932617],
[100.794744,4.800695],
[111.756194,4.667799],
[135.400750,4.483400],
[145.264225,4.581692],
[300.0,4.501692]])

NewK_Cu = interpolate.interp1d(K_Cu[:,0],K_Cu[:,1])

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
def fcn2min(params, T_d, L, t):#,err):
    """ model NLIV """
    K = params['K'].value
    T_i = params['T_i'].value
    dz=params['dz'].value
    
    
    Wcu = 150e-9
    Tcu = 130e-9
    Ks = NewK_Si(t)
    Kcu = 100*NewK_Cu(t)
    PyRes = -PyR(t)*((30e-9*5e-6)/50e-6)
    R = -PyR(t)
    CuRes = CuR(t)*((130e-9*150e-9)/925e-9)
    
    a = numpy.sqrt(Ks/(K*Tcu*dz))
       
    model = ((T_i-t)*numpy.exp(-a*L))+t
    
    return model-T_d
    
# Functionto interpolate each Beta vs T curve  
def interpSig(folder,keys):
   
  # Test interpolated data
  plt.xlabel('Temperature (K)',labelpad=15)
  plt.ylabel(r'$\beta$ (V/A$^2$)',labelpad=15)
  Spc = ((-0.01411*t)-0.11185)*1e-6
  i = 300e-6
  plt.plot(folder[0].column('Sample Temp'),folder[0].column('Beta'),'o',label = folder[0]['Sample ID'])  
  interp = interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('Beta'),kind = 'linear')
  
  T = numpy.arange(7,270,1)
  #Td = ((i*i*-interp(T))/Spc)
  #plt.plot(T,Td,'r')
  
  return Beta.append(interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('Beta'))),Sep.append(Seperation[folder[0]['L']]),Betaerr.append(interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('Beta err')))


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
Beta = []
Betaerr = []
Sep = []
folder.walk_groups(interpSig,group=True,replace_terminal=True)



# create a set of Parameters for fit
params = Parameters()
params.add('K',   value = 1.0e2,min=0)
params.add('T_i', value = 100.0,min=0)
params.add('dz', value = 1e-9,min=0)




T = numpy.arange(6,260,10)
KCu = []
Ti = []
Kerr = []
Tierr = []

# Loop over temperature range and fit for spin diffusion length and alph at each temp
for t in T:
  temp = []
  temperr=[]
  Spc = ((-0.01411*t)-0.11185)*1e-6
  I = 300e-6
  for i in range(len(Sep)):
    Td = t+((I*I*(-Beta[i](t)))/Spc)
    temp.append(Td)
    #temperr.append(float(interperr[i](t)))
    
  # do fit, here with leastsq model
  result = minimize(fcn2min, params, args=(numpy.array(temp), numpy.array(Sep), t))#, temperr))
  
  # calculate final result
  final = temp + result.residual
  
  # write error report
  report_fit(params)
 
  #make two lists of fitting params
  KCu.append(params['K'].value)
  Ti.append(params['T_i'].value)
  Kerr.append(params['K'].stderr)
  Tierr.append(params['T_i'].stderr)
  
output = Stoner.DataFile()
output.add_column(KCu,column_header='K')
output.add_column(Kerr,column_header='K_err')
output.add_column(Ti,column_header='Ti')
output.add_column(Tierr,column_header='Ti_err')
output.add_column(T,column_header='Temperature')

'''
# Plot Lambda and alpha
fig, ax1 = plt.subplots()
ax1.set_xlabel('Temperature (K)')
plt.hold(True)

ax1.errorbar(output.column('Temperature'),output.column('K'),output.column('K_err'),ecolor='k',marker='o',mfc='r', mec='k')
ax1.set_ylabel('$\lambda_{Cu}$ nm', color='k')
for tl in ax1.get_yticklabels():
    tl.set_color('k')
#plt.legend(loc='upper left')  
   
#ax2 = ax1.twinx()
ax1.errorbar(output.column('Temperature'),output.column('Ti')-T,output.column('Ti_err'),ecolor='k',marker='o',mfc='r', mec='k')
ax1.set_ylabel(r'$\alpha$', color='r')
for tl in ax1.get_yticklabels():
    tl.set_color('r')
'''
plt.legend(loc = 'upper left')
plt.tight_layout(pad=0.1, w_pad=0.0, h_pad=0.0)
plt.show()





