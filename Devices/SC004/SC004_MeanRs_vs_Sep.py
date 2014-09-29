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

class workfile(Analysis.AnalyseFile,SP.PlotFile):
    """A class that combines AnalyseFile and PlotFile together"""
    pass

###### Define dicts to link sample ID ans seperation ######
Seperation = {1:325e-9,2:425e-9,3:525e-9,4:625e-9, 5:725e-9, 6:925e-9,7:1125e-9, 8:1325e-9, 9:1525e-9,} 
sc020 = {'1A':300e-9,'1B':400e-9,'2A':500e-9,'2B':600e-9,'3A':700e-9,'3B':800e-9,'5A':1200e-9,'5B':1400e-9,}


# Import Beta vs T data and group
pattern = '*DeltaRsvsT.txt'
folder = DataFolder('/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaRvsT',pattern = pattern,type=workfile)  
 
## Interpolate Data
b=[]
b_err=[]
Sep=[]
for f in folder:
    b.append(interpolate.interp1d(f.column('T'),f.column('Voff')))
    #b_err.append(interpolate.interp1d(f.column('T'),f.column('Beta err')))
    Sep.append(Seperation[int(f['Sample ID'].split('_')[1])])



T1 = numpy.arange(10.,70.,5.)
T2a = numpy.arange(70.,100.,10.)
T2 = numpy.arange(100.,200.,20.)
T3 = numpy.array([200.,225.,250.])
T = numpy.concatenate((T1,T2a,T2,T3),axis=0)
print T


decay = workfile()
decay.template=SPF.JTBPlotStyle
decay.figure(1)

f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


plot_T = [10.0,250.0]
# Loop over temperature range and fit for spin diffusion length and alph at each temp
for t in T:
  print t
  beta = []
  #beta_err=[]
  S = []
  for i in range(len(Sep)):
      if Sep[i]<1.2e-6:
          S.append(Sep[i])
          beta.append(b[i](t))
          #beta_err.append(b_err[i](t))

  if t in plot_T:
     decay.add_column(beta,r'$\beta$'+str(t))
     #decay.add_column(beta_err,r'$\beta$_err'+str(t))

decay.add_column(S,'L (m)')
decay.multiply('L (m)',1e6,replace=True,header=r'L ($\mu$m)')

# Plot Lambda and alpha

for t in plot_T:
    decay.plot_xy(r'L ($\mu$m)',r'$\beta$'+str(t),linestyle='',marker='o',markersize=6,label=str(t)+' K')
    decay.ylabel=r"$\frac{R_{s}^P + R_{s}^{AP}}{2}\ $ (mV/A)"
plt.tight_layout()
plt.legend(loc='best')
#plt.semilogy()

