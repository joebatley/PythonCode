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
from Stoner.Util import format_error

class workfile(Analysis.AnalyseFile,SP.PlotFile):
    """A class that combines AnalyseFile and PlotFile together"""
    pass

Seperation = {'1A':300e-9,'1B':400e-9,'2A':500e-9,'2B':600e-9,'3A':700e-9,'3B':800e-9,'4A':900e-9,'5A':1200e-9,'5B':1400e-9,}

# define objective function: returns the array to be minimized
def fcn2min(params, DR, L, t):
    """ model NLIV """
    
    Lambda_N = params['Lambda_N'].value
    P = params['Alpha'].value
    
    Wpy1 = 190e-9
    Wpy2 = 140e-9
    Wcu = 150e-9
    Tcu = 120e-9
    Lambda_F = 5e-9*(PyR(20)/PyR(t))
    if sample=='SC020':    
        PyRes = PyR(t)
    else:
        PyRes = PyR(t)+CoR(t)
    CuRes = CuR(t)

    l = -1*L/Lambda_N
     
    Rf1 = (PyRes*Lambda_F)/(Wpy1*Wcu)
    Rf2 = (PyRes*Lambda_F)/(Wpy2*Wcu)
    Rn = (CuRes*Lambda_N)/(Wcu*Tcu)
    
    x1 = (2.0*Rf1)/(1.0-(P**2))
    x2 = (2.0*Rf2)/(1.0-(P**2))
    x3 = 1.0/Rn
    denom = ((1.0+(x1*x3))*(1.0+(x2*x3)))-numpy.exp(2.0*l)    
    
    Y = P*P*x1*x2*x3*numpy.exp(l)/denom
    
    model = (4.0*P*P*Rf1*Rf1*numpy.exp(l))/(((1.0-P**2.0)**2.0*Rn)*(((1.0+(2.0*Rf1/((1.0-P**2)*Rn)))**2.0)-numpy.exp(2.0*l)))

    return (Y - DR)
  

sample = 'SC021'
plot_T = [20.]
# Import and interpolate the resistivity data

if sample == 'SC020':
    Py = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/DeltaRvsT/SC018_4A_Py_rhovT_.txt')
    Py.sort('T (K)')
    PyR = interpolate.interp1d(Py.column('T (K)'),Py.column(r'$\rho (\Omega$m)'))
else:
    Co = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC021/Transport/DeltaRvsT/SC018_5A_rhovT.txt')
    Py = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/DeltaRvsT/SC018_4A_Py_rhovT_.txt')
    print min(Py.column('T (K)'))
    Py.sort('T (K)')
    PyR = interpolate.interp1d(Py.column('T (K)'),Py.column(r'$\rho (\Omega$m)'))
    Co.sort('T (K)')
    CoR = interpolate.interp1d(Py.column('T (K)'),Py.column(r'$\rho (\Omega$m)'))


Cu = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample+'/Transport/DeltaRvsT/'+sample+'_Cu_rhovT.txt')
Cu.sort('T (K)')
CuR = interpolate.interp1d(Cu.column('T (K)'),Cu.column(r'$\rho (\Omega$m)'))


# Import Delta R vs T data and group
pattern = '*DeltaRsvsT.txt'
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample+'/Transport/DeltaRvsT/',pattern = pattern,type=workfile)
#print folder

## Interpolate Data
Spinsig=[]
Spinsigerr=[]
Sep=[]
for f in folder:
    f.multiply('DR mV',1e-3,replace=True,header='DR')
    f.multiply('DRerr',1e-3,replace=True,header='DRerr')
    Spinsig.append(interpolate.interp1d(f.column('T'),f.column('DR')))
    Spinsigerr.append(interpolate.interp1d(f.column('T'),f.column('DRerr')))
    Sep.append(Seperation[str(f['Sample ID'].split('_')[1]+f['Sample ID'].split('_')[2])])


# create a set of Parameters
params = Parameters()
params.add('Lambda_N',   value = 600e-9,min=0,max=2e-6)
params.add('Alpha', value = 0.42,min=0,max=1,vary=True)

T1 = numpy.arange(20.,100.,10.)
T2 = numpy.arange(100.,200.,20.)
T3 = numpy.array([200.,225.,249.])
T = numpy.concatenate((T1,T2,T3),axis=0)

output = workfile()
output.column_headers = ['T','Lam_Cu','Lam_err','P','P_err','LamFM']
output.labels = ['T (K)',r'$\lambda_{Cu}$ (m)','Lam_err',r'$\alpha$','P_err',r'$\lambda_{FM}$ (m)']

output.template=SPF.JTBPlotStyle
#output.figure(1) # Creating new figures like this means we don;t reuse windows from run to run

decay_fit = workfile()
L = numpy.arange(0,1.5e-6,10e-9)
decay_fit.add_column(L,'L (m)')
decay_fit.template=SPF.JTBPlotStyle
decay_fit.figure(1)

decay = workfile()
decay.add_column(Sep,'L (m)')
decay.template=SPF.JTBPlotStyle
decay.figure(1)


f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday



# Loop over temperature range and fit for spin diffusion length and alph at each temp
for t in T:
  print t
  DRs = []
  DRs_err=[]
  for i in range(len(Sep)):
      DRs.append(Spinsig[i](t))
      DRs_err.append(Spinsigerr[i](t))
 
  
  # do fit, here with leastsq model
  result = minimize(fcn2min, params, args=(numpy.array(DRs), numpy.array(Sep), t))
  
  # calculate final result
  final = numpy.array(DRs) + result.residual
  
  # write error report
  report_fit(params)
  
  Lambda_F = 5e-9*(PyR(20)/PyR(t))
  row = numpy.array([t,params['Lambda_N'].value,params['Lambda_N'].stderr,params['Alpha'].value,params['Alpha'].stderr,Lambda_F])
  output+=row

  if t in plot_T:
     Lambda_N = params['Lambda_N'].value
     P = params['Alpha'].value
         
     Wpy1 = 190e-9
     Wpy2 = 140e-9
     Wcu = 150e-9
     Tcu = 120e-9
     Lambda_F = 5e-9*(PyR(20)/PyR(t))
     if sample=='SC020':    
        PyRes = PyR(t)
     else:
        PyRes = PyR(t)+CoR(t)
     CuRes = CuR(t)

     l = -1*L/Lambda_N     
     Rf1 = (PyRes*Lambda_F)/(Wpy1*Wcu)
     Rf2 = (PyRes*Lambda_F)/(Wpy2*Wcu)
     Rn = (CuRes*Lambda_N)/(Wcu*Tcu)
    
     x1 = (2.0*Rf1)/(1.0-(P**2))
     x2 = (2.0*Rf2)/(1.0-(P**2))
     x3 = 1.0/Rn
     denom = ((1.0+(x1*x3))*(1.0+(x2*x3)))-numpy.exp(2.0*l)    
    
     Y = P*P*x1*x2*x3*numpy.exp(l)/denom
     
     decay_fit.add_column(Y,'DR'+str(t))
     decay.add_column(DRs,'DRs'+str(t))
     decay.add_column(DRs_err,'DRs_err'+str(t))

print decay_fit.column_headers
# Plot Lambda and alpha
plt.subplot2grid((2,2),(0,0))
output.title = sample
output.plot_xy('T','Lam_Cu',yerr='Lam_err',linestyle='',marker='o',figure=1) 
plt.subplot2grid((2,2),(0,1))
output.plot_xy('T','P',yerr='P_err',linestyle='',marker='o',figure=1)
plt.subplot2grid((2,2),(1,0),colspan=2)
for t in plot_T:
    decay_fit.plot_xy('L (m)','DR'+str(t),linestyle='--',linewidth=1,marker='',color='k',label=None,figure=1)
    decay.plot_xy('L (m)','DRs'+str(t),yerr='DRs_err'+str(t),linestyle='',marker='o',markersize=4,label=str(t)+' K',figure=1)
    decay.ylabel=r'$\Delta R_s$ (V/A)'
#plt.subplot2grid((2,2),(1,0))    
#output.plot_xy('T','LamFM',linestyle='',marker='o')
plt.tight_layout()


#output.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample+'/Transport/Scattering Analysis/'+sample+'_Spindiffusion_length_vs_T.txt')
if sample =='SC020':
    device='Py/Cu'
else:
    device='Py/Co/Cu'
    
decay_fit.multiply('DR'+str(t),1e3,header='DRmV'+str(t))
decay.multiply('DRs'+str(t),1e3,header='DRsmV'+str(t))
decay.multiply('DRs_err'+str(t),1e3,header='DRsmV_err'+str(t))
decay_fit.plot_xy('L (m)','DRmV'+str(t),linestyle='--',linewidth=1,marker='',color='k',label=None,figure=2)
decay.plot_xy('L (m)','DRsmV'+str(t),yerr='DRsmV_err'+str(t),linestyle='',marker='o',markersize=4,label=device,figure=2)
decay.ylabel=r'$\Delta R_s$ (mV/A)'

output.multiply('Lam_Cu',1e9,header='Lam_Cu nm')
output.multiply('Lam_err',1e9,header='Lam_err nm')
output.plot_xy('T','Lam_Cu nm',yerr='Lam_err nm',linestyle='',marker='o',figure=3,label=device)
output.ylabel=r'$\lambda_{Cu}$ (nm)'

output.plot_xy('T','P',yerr='P_err',linestyle='',marker='o',figure=4,label=device)

print numpy.mean(output.column('P'))
print numpy.mean(output.column('P_err'))
print output