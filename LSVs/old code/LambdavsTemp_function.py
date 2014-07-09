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



Seperation = {'1A':160e-9,
              '1B':270e-9,
              2:450e-9,
              3:570e-9,
              4:690e-9,
              '5A':1040e-9,
              '5B':1150e-9,
              6:954e-9,
              7:1182e-9,
              8:1378e-9,
              9:1525e-9,}
# define objective function: returns the array to be minimized
def fcn2min(params, DR, L, t,err):
    """ model NLIV """
    print DR
    Lambda_N = params['Lambda_N'].value
    P = params['Alpha'].value
    
    Wpy1 = 170e-9
    Wpy2 = 140e-9
    Wcu = 150e-9
    Tcu = 100e-9
    Lambda_F = 5e-9*(PyR(10)/PyR(t))
    PyRes = PyR(t)
    CuRes = CuR(t)

    l = -1*L/Lambda_N
     
    Rf1 = (PyRes*Lambda_F)/(Wpy1*Wcu)
    Rf2 = (PyRes*Lambda_F)/(Wpy1*Wcu)
    Rn = (CuRes*Lambda_N)/(Wcu*Tcu)
    
    x1 = (2.0*P*Rf1)/(1.0-(P**2))
    x2 = (2.0*P*Rf2)/(1.0-(P**2))
    x3 = 1.0/Rn
    denom = ((1.0+(x1*x3))*(1.0+(x2*x3)))+numpy.exp(2.0*l)    
    
    Y = x1*x2*x3*numpy.exp(l)/denom
    
    model = (4.0*P*P*Rf1*Rf1*numpy.exp(l))/(((1.0-P**2.0)**2.0*Rn)*(((1.0+(2.0*Rf1/((1.0-P**2)*Rn)))**2.0)-numpy.exp(2.0*l)))

    return (Y - DR)/err
  


# Import and interpolate the resistivity data
Py = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/DeltaRvsT/SC018_4A_Py_rhovT_.txt')
Py.sort('T (K)')
PyR = interpolate.interp1d(Py.column('T (K)'),Py.column(r'$\rho (\Omega$m)'))


Cu = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/DeltaRvsT/SC020_5_A_Cu_rhovT_.txt')
Cu.sort('T (K)')
CuR = interpolate.interp1d(Cu.column('T (K)'),Cu.column(r'$\rho (\Omega$m)'))


# Import Delta R vs T data and group
pattern = re.compile('SC004_(?P<L>\d*)_(?P<Device>\w*)_DeltaRvsT.txt')
pattern = '*DeltaRsvsT.txt'
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/DeltaRvsT/',pattern = pattern)
print folder

## Interpolate Data
Spinsig=[]
Spinsigerr=[]
Sep=[]
for f in folder:
    print f['Sample ID']
    Spinsig.append(interpolate.interp1d(f.column('T (K)'),f.column(r'$\Delta R_s$ (V/A)')))
    Spinsigerr.append(interpolate.interp1d(f.column('T (K)'),f.column('DRerr')))
    Sep.append(Seperation[str(f['Sample ID'].split('_')[1]+f['Sample ID'].split('_')[2])])


# create a set of Parameters
params = Parameters()
params.add('Lambda_N',   value = 1000e-9,min=0)
params.add('Alpha', value = 0.2,min=0,max=1)

T1 = numpy.arange(10,140,10)
T3 = numpy.arange(100,260,20)
T = numpy.concatenate((T1,T3),axis=0)

Lambda = []
alpha = []
Lerr = []
alphaerr = []

# Loop over temperature range and fit for spin diffusion length and alph at each temp
for t in T1:
  print t
  DRs = []
  DRs_err=[]
  for i in range(len(Sep)):
      DRs.append(Spinsig[i](t))
      DRs_err.append(Spinsigerr[i](t))
 
  
  # do fit, here with leastsq model
  result = minimize(fcn2min, params, args=(numpy.array(DRs), numpy.array(Sep), t, DRs_err))
  
  # calculate final result
  final = Spinsig[i](t) + result.residual
  
  # write error report
  report_fit(params)
  
  #make two lists of fitting params
  #Lambda.append(params['Lambda_N'].value)
  Lambda.append(params['Lambda_N'].value)
  alpha.append(params['Alpha'].value)
  Lerr.append(params['Lambda_N'].stderr)
  alphaerr.append(params['Alpha'].stderr)
  
output = Analysis.AnalyseFile()
output.add_column(Lambda,column_header='Lambda_Cu')
output.add_column(Lerr,column_header='Lambda_Cu_err')
output.add_column(alpha,column_header='P')
output.add_column(alphaerr,column_header='P_err')
output.add_column(T,column_header='Temperature')



# Plot Lambda and alpha



p=SP.PlotFile(output)
print p.column_headers
p.setas="ye..x"
p.template=SPF.JTBPlotStyle
title = r' '
label = None
p.plot(label=label,figure=1,title=title)

#p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Spindiffusionlength_from_data.txt')


##### Plot DR vs Sep with fit

T = 20
DRs = []
DRs_err=[]
for i in range(len(Sep)):
  DRs.append(Spinsig[i](T))
  DRs_err.append(Spinsigerr[i](T))
 
# do fit, here with leastsq model
result = minimize(fcn2min, params, args=(numpy.array(DRs), numpy.array(Sep), T, DRs_err))
  
# calculate final result
final = Spinsig[i](t) + result.residual
  
# write error report
report_fit(params)
  
Lambda_N = params['Lambda_N'].value
P = params['Alpha'].value
L = numpy.arange(100e-9,2e-6,10e-9)    
Wpy1 = 170e-9
Wpy2 = 140e-9
Wcu = 150e-9
Tcu = 100e-9
Lambda_F = 5e-9*(PyR(10)/PyR(t))
PyRes = PyR(t)
CuRes = CuR(t)

l = -1*L/Lambda_N     
Rf1 = (PyRes*Lambda_F)/(Wpy1*Wcu)
Rf2 = (PyRes*Lambda_F)/(Wpy1*Wcu)
Rn = (CuRes*Lambda_N)/(Wcu*Tcu)
    
x1 = (2.0*P*Rf1)/(1.0-(P**2))
x2 = (2.0*P*Rf2)/(1.0-(P**2))
x3 = 1.0/Rn
denom = ((1.0+(x1*x3))*(1.0+(x2*x3)))+numpy.exp(2.0*l)    
    
Y = x1*x2*x3*numpy.exp(l)/denom
    
model = (4.0*P*P*Rf1*Rf1*numpy.exp(l))/(((1.0-P**2.0)**2.0*Rn)*(((1.0+(2.0*Rf1/((1.0-P**2)*Rn)))**2.0)-numpy.exp(2.0*l)))

  
DRsep = Analysis.AnalyseFile()
DRsep.add_column(DRs,column_header=r'$\Delta R_s$ (V/A)')
DRsep.add_column(DRs_err,column_header='DRerr')
DRsep.add_column(Sep,column_header='d (m)')
DRsep.sort('d (m)')


fit = Analysis.AnalyseFile()
fit.add_column(L,'d (m)')
fit.add_column(model,'DR_fit')
fit.add_column(Y,'DR_fit1')
# Plot Lambda and alpha


q=SP.PlotFile(DRsep)
print q.column_headers
q.setas="yex"
q.template=SPF.JTBPlotStyle
title = r' '
label = None
q.plot(label=label,figure=2,title=title)

s=SP.PlotFile(fit)
print s.column_headers
#s.setas="xyy"
s.template=SPF.JTBPlotStyle
title = r' '
label = None
s.plot_xy('d (m)',['DR_fit','DR_fit1'],label=label,figure=2,title=title)






