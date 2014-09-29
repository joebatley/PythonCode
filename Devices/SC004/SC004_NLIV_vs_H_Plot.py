"""
Code to plot Rs vs H from NLIV vs H data.

Assumes file name format 

<Sample ID>_6221-2182 DC IV_Magnet Power Supply Multi-segment_<Iterator>_<Temp>K_<Injector Mat>_NLIV_<Max Current>uA_.txt

e.g. SC004_5_B_6221-2182 DC IV_Magnet Power Supply Multi-segment_1_200K_Py_NLIV_300uA_.txt

@author: py07jtb
"""

import numpy
import re
import Stoner.Analysis as Analysis
import matplotlib.pyplot as plt # pylab imports numpy namespace as well, use pyplot in scripts
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
from Stoner.Folders import DataFolder
from lmfit import minimize, Parameters, Parameter, report_fit

class workfile(Analysis.AnalyseFile,SP.PlotFile):
    """A class that combines AnalyseFile and PlotFile together"""
    pass
 
def quad(x,a,b,c):
  return (a*x**2)+(b*x)+c


folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_2_T/NLIVvsHat5K/', pattern = '*.txt',type=workfile) 


############ Calculate Delta R with error ############

Rs = []
Rserr = []
F = []
folder.sort('iterator')
for f in folder:
  fit = f.curve_fit(quad,'Current','Voltage',p0=[20.0,1e-7,0.0], result=True, replace=False, header="fit",asrow=True)
  Rs.append(-fit[0])
  F.append(f['Magnet Output']*1e-9)
  Rserr.append(fit[1])
  
Mean = (max(Rs)+min(Rs))/2
offset = (max(Rs)+min(Rs))/2

RS = workfile()
RS.add_column(F,'field')
RS.add_column(Rs,'Rs')
RS.add_column(Rserr,'Rserr')

#RS.subtract('R$_s$ (V/A)',offset,replace=True,header=r'$\alpha$ (V/A)')
#RS.multiply(r'$\alpha$ (V/A)',1e3,replace=True,header=r'$R_s$ (mV/A)')
#RS.multiply('Rserr',1e3,replace=True,header='Rserr')

'''
AP = RS.search(r'$\alpha$ (mV/A)',lambda x,y: x<Mean,r'$\alpha$ (mV/A)')
P = RS.search(r'$\alpha$ (mV/A)',lambda x,y: x>Mean,r'$\alpha$ (mV/A)')

DR = numpy.mean(P)-numpy.mean(AP)
DRerr = (numpy.std(P)**2+numpy.std(AP)**2)**0.5

print DR,DRerr
'''


################ plot Data ##################


RS.template=SPF.JTBPlotStyle
RS.figure() # Creating new figures like this means we don;t reuse windows from run to run
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


RS.title = ''
RS.plot_xy("field","Rs",yerr = 'Rserr',label = None,linestyle='-',marker='o',markersize=5,linewidth=1) 
#RS.ylabel=r"R$_s$ (mV/A)"
RS.ylabel=r"$\beta$ (V/A$^2$)"
RS.xlabel=r'$\mu_o$H (mT)'
plt.legend(loc='best')
plt.tight_layout()



















