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
def Rs(L,Lambda_N,P):
  
  
  Wpy = 150e-9
  Wcu = 150e-9
  Tcu = 130e-9
  Lambda_F = 5e-9*(PyR(10)/PyR(t))    
  PyRes = -PyR(t)*((30e-9*5e-6)/50e-6)
  CuRes = CuR(t)*((Tcu*150e-9)/925e-9)


  Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
  Rn = (CuRes*Lambda_N)/(Wcu*Tcu)   
  model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))
  
  Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
  Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
  model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
  model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))
  
  return model_Cas
  
# Functionto interpolate each Delta R vs T curve  
def interpSig(folder,keys):
  '''
  # Test interpolated data
  plt.xlabel('Temperature (K)')
  plt.ylabel('$\Delta$R$_s$ (mV/A)')
  
  #plt.plot(folder[0].column('Sample Temp'),1e3*folder[0].column('DeltaR'),'o',label = folder[0]['Sample ID'])  
  inter = interpolate.interp1d(folder[0].column('Sample Temp'),folder[0].column('DeltaR'),kind = 'linear')
  T = numpy.arange(10,260,10)
  plt.plot(T,1e3*inter(T),'o',label = folder[0]['Sample ID'])
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



# Plot Spin diffusion fit for one temperature
t = 10
temp = []
for i in range(len(Sep)):
  Spinsig[i] = Spinsig[i](t)
  Spinsigerr[i] = Spinsigerr[i](t)
  
a = Analysis.AnalyseFile()
a.add_column(Spinsig,column_header = 'DeltaR')
a.add_column(Spinsigerr, column_header ='DeltaR err')
a.add_column(Sep, column_header = 'L')  

fit= a.curve_fit(Rs,'L','DeltaR',p0=[400e-9,0.4],sigma = 'DeltaR err',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
print fit


  
Lambda_N = fit[0]
P = fit[2]
L = numpy.arange(200e-9,3.5e-6,10e-9)
Wpy = 150e-9
Wcu = 150e-9
Tcu = 130e-9
Lambda_F = 5e-9*(PyR(10)/PyR(t))    
PyRes = -PyR(t)*((30e-9*5e-6)/50e-6)
CuRes = CuR(t)*((Tcu*150e-9)/925e-9)


Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
Rn = (CuRes*Lambda_N)/(Wcu*Tcu)   
model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))

Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))


  
  
plt.hold(True)
plt.ylabel('$\Delta$R$_s$ (mV/A)',labelpad=15)
plt.xlabel('Electrode seperation (nm)',labelpad=15)
plt.plot(1e9*a.L,1e3*a.DeltaR,'ok',label = 'Leeds')
#plt.errorbar(1e9*a.L,1e3*a.DeltaR,1e3*a.column('DeltaR err'),ecolor='k',marker='o',mfc='b', mec='k',linestyle='')
plt.plot(L*1e9,model_Cas*1e3,'-k',label = "$\lambda_s$ at " + str(t) + " K = " + str.format("{0:.2g}", fit[0])) 
#{} nm".format(format_error(fit[0],fit[1],latex=False)))
#plt.plot(1e9*a.L,1e3*a.Fit,'-r')
#plt.plot(d*1e9,1e3*model_Otani)
plt.legend(loc='upper right')
plt.tight_layout(pad=0.1, w_pad=0.0, h_pad=0.0)
plt.show





