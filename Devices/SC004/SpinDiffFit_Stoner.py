"""
Code to fit DeltaR vs L and extract the spin diffusion length and polarisation.

Expects a folder of files containing DRvsT data created by DeltaRvsT_from_NLRvsHvsT.py.

Also requires reference resistivity data for the FM anf NM materials.

@author: py07jtb
"""


import numpy
from scipy import interpolate
import pylab as plt
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP

class workfile(Analysis.AnalyseFile,SP.PlotFile):
   """A class that combines AnalyseFile and PlotFile together"""
   pass

#Dictionary used to link sample IDs with the lateral seperation
Seperation = {'1A':300e-9,'1B':400e-9,'2A':500e-9,'2B':600e-9,'3A':700e-9,'3B':800e-9,'4A':900e-9,'5A':1200e-9,'5B':1400e-9,}

#Device geometry
Wpy1 = 190e-9
Wpy2 = 140e-9
Wcu = 150e-9
Tcu = 120e-9

# Function to fit to data - this is based on the 1D spin diffusion equation
def spindiff(L,params,t=None):
   """ model NLIV """
   Lambda_N = params[0] 
   P = params[1]

   Lambda_F = 5e-9*(PyR(5)/PyR(t))
   PyRes = PyR(t)
   CuRes = CuR(t)
   l = -1*L/Lambda_N
   Rf1 = (PyRes*Lambda_F)/(Wpy1*Wcu)
   Rf2 = (PyRes*Lambda_F)/(Wpy2*Wcu)
   Rn = (CuRes*Lambda_N)/(Wcu*Tcu)
   x1 = (2.0*Rf1)/(1.0-(P**2))
   x2 = (2.0*Rf2)/(1.0-(P**2))
   x3 = 1.0/Rn
   denom = ((1.0+(x1*x3))*(1.0+(x2*x3)))-numpy.exp(2.0*l)
   model = P*P*x1*x2*x3*numpy.exp(l)/denom
   return model


sample = 'SC020'

# Import and interpolate the resistivity data

#Switch to a PC path
Py = workfile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/DeltaRvsT/SC018_4A_Py_rhovT_.txt')
#Py = workfile('S:/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/DeltaRvsT/SC018_4A_Py_rhovT_.txt')
Py.sort('T (K)')
print Py.span('T (K)')
PyR = interpolate.interp1d(Py.column('T (K)'),Py.column(r'$\rho (\Omega$m)'))


Cu = workfile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample+'/Transport/DeltaRvsT/'+sample+'_Cu_rhovT.txt')
#Cu = workfile('S:/Projects/Spincurrents/Joe Batley/Measurements/'+sample+'/Transport/DeltaRvsT/'+sample+'_Cu_rhovT.txt')
Cu.sort('T (K)')
CuR = interpolate.interp1d(Cu.column('T (K)'),Cu.column(r'$\rho (\Omega$m)'))
print Cu.span("T (K)")

# Import Delta R vs T data and group
pattern = '*DeltaRsvsT.txt'
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample+'/Transport/DeltaRvsT/',pattern = pattern,type=workfile)
#folder = DataFolder('S:/Projects/Spincurrents/Joe Batley/Measurements/'+sample+'/Transport/DeltaRvsT/',pattern = pattern,type=workfile)



#create the temperature array to map spin diffusion data onto
T1 = numpy.arange(5.,80.,5.)
T2 = numpy.arange(80.,100.,10.)
T3 = numpy.arange(100.,200.,20.)
T4 = numpy.array([200.,225.,249.,270.])
T = numpy.concatenate((T1,T2,T3,T4),axis=0)

## Interpolate Data spin diffusion data so it can all be mapped onto the same temperature values
DR = workfile()
headers=[str(t) for t in T]
err_headers = [str(t)+'.err' for t in T]
headers.insert(0,'l')
headers.append(err_headers)



for f in folder:
   f.multiply('DR mV',1e-3,replace=True,header='DR') #Convert to V/A
   f.multiply('DRerr',1e-3,replace=True,header='DRerr')
   R = f.interpolate(T,xcol='T')[:,5].tolist()  #Interpolate and create a list of DR values
   R+=f.interpolate(T,xcol='T')[:,6].tolist()   #Interpolate and add a list of DR errors to above list
   l = Seperation[str(f['Sample ID'].split('_')[1]+f['Sample ID'].split('_')[2])]   #Get seperation
   R.insert(0,l)    #Add seperation at the begining of the ist
   DR+=numpy.array(R)   #Add row to datafile
   

# create a set of Parameters to be used in the fitting
params = [{'value':300e-9, 'fixed':False, 'limited':[True,True], 'limits':[50e-9,2e-6], 'parname':'Spin diffusion length'},
         {'value':0.4, 'fixed':False, 'limited':[True,True], 'limits':[0.,1.], 'parname':'Polarisation'}]

output = workfile() #create file to store fit parameters
output.column_headers = ['T','Lambda','Lambda.err','P','P.err']

for i in range(len(T)):
   func_args = {'t':T[i]}
   m = DR.mpfit(spindiff,  'l', i+1, params,  func_args=func_args, sigma=len(T)+i+1)
   fit_row = numpy.array([T[i],m.params[0],m.perror[0],m.params[1],m.perror[1]])    #Row of fit params
   output+=fit_row  #add row to ouput datafile
   
   
### PLOT OUTPUT ###   
output.template=SPF.JTBPlotStyle
output.figure(10) 
f=plt.gcf()
f.set_size_inches((11,7.5),forward=True) 
#Lambda    
output.subplot(121)
output.plot_xy("T","Lambda",yerr = 'Lambda.err',linestyle='',marker='o',label=None)
output.ylabel=r'$\lambda_{Cu}$ (m)'
output.xlabel='T (K)'
#Polarisation
output.subplot(122)
output.plot_xy("T","P",yerr='P.err',linestyle='',marker='o',label=None)
output.ylabel=r'$\alpha$'
output.xlabel='T (K)'

plt.tight_layout()



