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
              3:570e-9,
              4:650e-9,
              5:742e-9,
              6:960e-9,
              7:1182e-9,
              8:1360e-9,
              9:1525e-9,}
# define objective function: returns the array to be minimized
def fcn2min(params, DR, L, t,err):
    """ model NLIV """

    Lambda_N = 1.34e-14/CuR(t)#params['Lambda_N'].value
    P = params['Alpha'].value
    
    Wpy = 150e-9
    Wcu = 150e-9
    Tcu = 130e-9
    Lambda_F = 5e-9*(PyR(10)/PyR(t))
    PyRes = PyR(t)
    CuRes = CuR(t)

     
    Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
    Rn = (CuRes*Lambda_N)/(Wcu*Tcu)   
    #model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))
    model_tak = (P*P)*Rn*numpy.exp((-L/Lambda_N))
    
    Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
    Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
    model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
    model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))


    
    return (model_tak - DR)/err
  
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
Py = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Py Res/RN200_1um_rhovT_.txt')
Py.sort('Temperature')
Py.mulitply(r'$\rho$ ($\mu \Omega$ cm)',1e-8,replace=True,header=r'$\rho$ ($\Omega$ m)')
print Py.column_headers
PyR = interpolate.interp1d(Py.column('Temperature'),Py.column(r'$\rho$ ($\Omega$ m)'))

Cu = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Cu spacer resistance/Resistivity/SC004_2_T_Cu_resistivity_vs_T.txt')
Cu.sort('T (K)')
print Cu.column_headers
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
print Sep



# create a set of Parameters
params = Parameters()
#params.add('Lambda_N',   value = 500e-9,min=0)
params.add('Alpha', value = 0.4,min=0,max=1)

T1 = numpy.arange(10,60,5)
T2 = numpy.arange(60,100,10)
T3 = numpy.arange(100,260,20)
T = numpy.concatenate((T1,T2,T3),axis=0)

Lambda = []
alpha = []
Lerr = []
alphaerr = []

RFM = []
RNM = []
Rs=[]
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
  #Lambda.append(params['Lambda_N'].value)
  #Lambda.append(params['Lambda_N'].value)
  alpha.append(params['Alpha'].value)
  #Lerr.append(params['Lambda_N'].stderr)
  alphaerr.append(params['Alpha'].stderr)
  Lambda_N = 1.34e-14/CuR(t)
  Lambda_F = 5e-9*(PyR(10)/PyR(t))
  Wpy = 150e-9
  Wcu = 150e-9
  Tcu = 130e-9
  pol=params['Alpha'].value
  Rs.append((pol**2)/(1+(1-pol**2)))
  #Rs.append(((pol**2)*1.34e-14)/(1+(1-pol**2)*(1.34e-14/(5e-9*PyR(10)))))
  RFM.append( (PyR(t)*Lambda_F)/(Wpy*Wcu))
  RNM.append((CuR(t)*Lambda_N)/(Wcu*Tcu))
  
output = Analysis.AnalyseFile()
#output.add_column(Lambda,column_header='Lambda_Cu')
#output.add_column(Lerr,column_header='Lambda_Cu_err')
output.add_column(alpha,column_header='P')
output.add_column(alphaerr,column_header='P_err')
output.add_column(RFM,column_header='RFM')
output.add_column(RNM,column_header='RNM')
output.add_column(Rs,column_header='Rs')
output.add_column(T,column_header='Temperature')

#output.subtract('P',0.51,replace=True)
#output.mulitply('P',0.05,replace=True)

# Plot Lambda and alpha



p=SP.PlotFile(output)
p.setas="....yx"
p.template=SPF.JTBPlotStyle
title = r' '
label = None
p.plot(label=label,figure=2,title=title)

Lambda_N = 1.34e-14/CuR(t)
Lambda_F = 5e-9*(PyR(10)/PyR(t))
Wpy = 150e-9
Wcu = 150e-9
Tcu = 130e-9
print (PyR(t)*Lambda_F)/(Wpy*Wcu)
print (CuR(t)*Lambda_N)/(Wcu*Tcu)  

#p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DR_simlulations/Fits with lam 1 over rho/Pol_from_data.txt')



'''
def spinwave(x,a,b):
  return a*(1-b*(x**(3/2)))

print output.column_headers

output.mulitply('Lambda_Cu',1e9,replace=True,header=r'$\lambda_{Cu}$ (nm)')
output.mulitply('Lambda_Cu_err',1e9,replace=True,header=r'$\lambda_{Cu}$ Error (nm)')
output.rename('Temperature','Temperature (K)')

mag=output.curve_fit(spinwave,4,2,bounds=lambda x,y:x>100,asrow=True)

p=SP.PlotFile(output)
p.setas="..yex"
p.template=SPF.JTBPlotStyle
title = r' '
label = None
p.plot(label=label,figure=1,title=title)


temp = numpy.arange(0.0,900.0,1.0)
M = mag[0]*(1-mag[2]*(temp**(3/2)))
print mag[0],mag[2]
q=SP.PlotFile()
q.add_column(temp,column_header='T (K)')
q.add_column(M,column_header='P')
q.setas="xy"
q.template=SPF.JTBPlotStyle
title = r' '
label = None
q.plot(label=label,figure=1,title=title)



fig, ax1 = plt.subplots()
ax1.set_xlabel('Temperature (K)',labelpad=15)
plt.hold(True)

ax1.errorbar(output.column('Temperature'),output.column('Lambda_Cu')*1e9,output.column('Lambda_Cu_err')*1e9,ecolor='k',marker='o',mfc='b', mec='k',linestyle='')
ax1.set_ylabel('$\lambda_{Cu}$ nm', color='k',labelpad=15)
for tl in ax1.get_yticklabels():
    tl.set_color('k')
#plt.legend(loc='upper left')  

#ax2 = ax1.twinx()
ax1.errorbar(output.column('Temperature'),output.column('Alpha'),output.column('Alpha_err'),ecolor='k',marker='o',mfc='r', mec='k',linestyle='')
ax1.set_ylabel(r'$\alpha$', color='k',labelpad=15)
for t1 in ax1.get_yticklabels():
    t1.set_color('k')
   
plt.tight_layout(pad=0.1, w_pad=0.0, h_pad=0.0)
#plt.legend(loc = 'upper right')
plt.show()
'''







