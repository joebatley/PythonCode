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
              2:450e-9,
              3:570e-9,
              4:690e-9,
              5:742e-9,
              6:954e-9,
              7:1182e-9,
              8:1378e-9,
              9:1525e-9,}
# define objective function: returns the array to be minimized
def fcn2min(params, DR, L, t,err):
    """ model NLIV """
    Lambda_N = params['Lambda_N'].value
    P = params['Alpha'].value
    
    Wpy = 169e-9
    Wcu = 168e-9
    Tcu = 130e-9
    Lambda_F = 5e-9*(PyR(10)/PyR(t))
    PyRes = -PyR(t)*((30e-9*5e-6)/50e-6)
    CuRes = CuR(t)*((130e-9*150e-9)/925e-9)

     
    Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
    Rn = (CuRes*Lambda_N)/(Wcu*Tcu)   
    model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))
    
    Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
    Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
    model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
    model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))


    
    return (model_Cas - DR)/err
  
# Functionto interpolate each Delta R vs T curve  
def interpSig(folder,keys):
  '''
  # Test interpolated data
  plt.xlabel('Temperature (K)')
  plt.ylabel('$\Delta$R$_s$ (mV/A)')
  
  plt.plot(folder[0].column('Sample Temp'),1e3*folder[0].column('DeltaR'),'o',label=folder[0]['Sample ID'])  
  inter = interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('DeltaR'),kind = 'linear')
  T = numpy.arange(7,280,1)
  plt.plot(T,1e3*inter(T),'r')
  plt.tight_layout()
  plt.legend()
  
  plt.plot(folder[0].column('Sample Temp'),1e3*folder[0].column('DeltaR err'),'ob')  
  inter = interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('DeltaR err'),kind = 'linear')
  T = numpy.arange(7,280,1)
  plt.plot(T,1e3*inter(T),'r')
  '''
  Spinsig.append(interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('DeltaR')))
  Sep.append(Seperation[folder[0]['L']])
  Spinsigerr.append(interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('DeltaR err')))
  return Spinsig,Sep,Spinsigerr


# Import and interpolate the resistivity data
Py = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaR_vs_Sep/RN200_5um_6221-2182 DC IV_Timed interval_RvT_500uA_.txt')
Py.sort('Sample Temp')
print min(Py.column('Sample Temp')),max(Py.column('Sample Temp'))
PyR = interpolate.interp1d(Py.column('Sample Temp'),Py.column('Resistance'))
Cu = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_6_T/SC004_6_T_6221-2182 DC IV_Timed interval_3.223900_RvT_CuBar_100uA.txt')
Cu.sort('Sample Temp')
print min(Cu.column('Sample Temp')),max(Cu.column('Sample Temp'))
CuR = interpolate.interp1d(Cu.column('Sample Temp'),Cu.column('Resistance'))

# Import Delta R vs T data and group
pattern = re.compile('SC004_(?P<L>\d*)_(?P<Device>\w*)_DeltaRvsT')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaR_vs_Sep',pattern = pattern)
folder.group('L')
#T = folder[0].column('Sample Temp')
# Walk groups and interpolate
Spinsig = []
Spinsigerr = []
Sep = []
folder.walk_groups(interpSig,group=True,replace_terminal=True)
print Sep



# create a set of Parameters
params = Parameters()
params.add('Lambda_N',   value = 500e-9,min=0)
params.add('Alpha', value = 0.2,min=0,max=1)

T1 = numpy.arange(10,60,5)
T2 = numpy.arange(60,100,10)
T3 = numpy.arange(100,260,20)
T = numpy.concatenate((T1,T2,T3),axis=0)

Lambda = []
alpha = []
Lerr = []
alphaerr = []

# Loop over temperature range and fit for spin diffusion length and alph at each temp
for t in T:
  
  temp = []
  temperr=[]
  for i in range(len(Sep)):
    temp.append(float(Spinsig[i](t)))
    temperr.append(float(Spinsigerr[i](t)))
    
  # do fit, here with leastsq model
  result = minimize(fcn2min, params, args=(numpy.array(temp), numpy.array(Sep), t, temperr))
  
  # calculate final result
  final = Spinsig[i](t) + result.residual
  
  # write error report
  report_fit(params)
  
  #make two lists of fitting params
  Lambda.append(params['Lambda_N'].value)
  alpha.append(params['Alpha'].value)
  Lerr.append(params['Lambda_N'].stderr)
  alphaerr.append(params['Alpha'].stderr)
  
output = Analysis.AnalyseFile()
output.add_column(Lambda,column_header='Lambda_Cu')
output.add_column(Lerr,column_header='Lambda_Cu_err')
output.add_column(alpha,column_header='Alpha')
output.add_column(alphaerr,column_header='Alpha_err')
output.add_column(T,column_header='Temperature')



# Plot Lambda and alpha
fig, ax1 = plt.subplots()
ax1.set_xlabel('Temperature (K)',labelpad=15)
plt.hold(True)

ax1.errorbar(output.column('Temperature'),output.column('Lambda_Cu')*1e9,output.column('Lambda_Cu_err')*1e9,ecolor='k',marker='o',mfc='b', mec='k',linestyle='')
ax1.set_ylabel('$\lambda_{Cu}$ nm', color='k',labelpad=15)
for tl in ax1.get_yticklabels():
    tl.set_color('k')
#plt.legend(loc='upper left')  
'''
#ax2 = ax1.twinx()
ax1.errorbar(output.column('Temperature'),output.column('Alpha'),output.column('Alpha_err'),ecolor='k',marker='o',mfc='r', mec='k',linestyle='')
ax1.set_ylabel(r'$\alpha$', color='k',labelpad=15)
for t1 in ax1.get_yticklabels():
    t1.set_color('k')
'''   
plt.tight_layout(pad=0.1, w_pad=0.0, h_pad=0.0)
#plt.legend(loc = 'upper right')
plt.show()








