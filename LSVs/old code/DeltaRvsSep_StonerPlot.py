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
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP


Seperation = {1:325e-9,
              2:460e-9,
              3:525e-9,
              4:650e-9,
              5:725e-9,
              6:960e-9,
              7:1125e-9,
              8:1360e-9,
              9:1525e-9,}
# define objective function: returns the array to be minimized
def Rs(L,Lambda,P,Pi):
  
  
  Wpy = 150e-9
  Wcu = 150e-9
  Tcu = 130e-9
  LF=5e-9
  Lambda_F = LF*(PyR(10)/PyR(t))    
  PyRes = PyR(t)
  CuRes = CuR(t)
  
  Lambda_N=Lambda/CuR(t)

  Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
  Rn = (CuRes*Lambda_N)/(Wcu*Tcu)  
  Ri=1e-5 * Wpy*Wcu  
  ri=Ri/((1-Pi**2)*Rn)
  rf=Rf/((1-P**2)*Rn)
  #model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))
  T1 = ((((2*Pi*ri)+(2*P*rf))**2)*numpy.exp(-L/Lambda_N))
  T2 = (((1+(2*ri)+(2*rf))**2)-numpy.exp(-(2*L/Lambda_N)))
  model_tak = T1/T2
  
  Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
  Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
  model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
  model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))
  
  return model_tak
  
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
Py = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Py Res/RN200_1um_rhovT_.txt')
Py.sort('Temperature')
Py.mulitply(r'$\rho$ ($\mu \Omega$ cm)',1e-8,replace=True,header=r'$\rho$ ($\Omega$ m)')
PyR = interpolate.interp1d(Py.column('Temperature'),Py.column(r'$\rho$ ($\Omega$ m)'))

Cu = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Cu spacer resistance/Resistivity/SC004_2_T_Cu_resistivity_vs_T.txt')
Cu.sort('T (K)')
CuR = interpolate.interp1d(Cu.column('T (K)'),Cu.column(r'$\rho$ ($\Omega$m)'))


# Import Delta R vs T data and group
pattern = re.compile('SC004_(?P<L>\d*)_(?P<Device>\w*)_DeltaRvsT')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaR_vs_Sep/Plot',pattern = pattern)
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
a.add_column(Spinsigerr, column_header ='DRerr')
a.add_column(Sep, column_header = 'L')  

#Do Fit
fit,fitvar= a.curve_fit(Rs,'L','DeltaR',p0=[2e-14,0.4,0.4],sigma = 'DRerr',bounds=lambda x,y:x,result=True,header='Fit',asrow=False)

print fit

#Plot Data
'''
a.mulitply('DeltaR',1e3,replace=True,header=r'$\Delta \alpha$ (mV/A)')
a.mulitply('L',1e9,replace=True,header='L (nm)')
a.mulitply('DRerr',1e3,replace=True,header='DRerr')
p=SP.PlotFile(a)
print p.column_headers
p.setas="y..x"
p.template=SPF.JTBPlotStyle
label = str(t) + ' K'
title = ' '
p.plot(label = label,title=title,figure=1)



'''
Lambda_N = fit[0]/CuR(t)
print Lambda_N
P = fit[1]
Pi=fit[2]
print P
LF = 5e-9
L = numpy.arange(300e-9,1.5e-6,10e-9)
Wpy = 150e-9
Wcu = 150e-9
Tcu = 130e-9
Lambda_F = LF*(PyR(10)/PyR(t))    
print Lambda_F
PyRes = PyR(t)
CuRes = CuR(t)


Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
Rn = (CuRes*Lambda_N)/(Wcu*Tcu)  
Ri=1e-5 #* Wpy*Wcu  
ri=Ri/((1-Pi**2)*Rn)
rf=Rf/((1-P**2)*Rn)
#model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))
model_tak = (((2*Pi*ri+2*P*rf)**2)*numpy.exp(-L/Lambda_N))/((1+2*ri+2*rf)**2-numpy.exp(-2*L/Lambda_N))

Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))


q=SP.PlotFile()
q.add_column(L*1e9,column_header='L (nm)')
q.add_column(model_tak*1e3,column_header=r'$\Delta \alpha$ (mV/A)')
print q.column_headers
q.setas="xy"
q.template=SPF.JTBPlotStyle
label = None
title = ' '
q.plot(label = label,title=title,figure=1)








