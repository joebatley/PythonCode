"""
Code to average NLIV data for sample SC004 and plot.

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

def func(x):
  return numpy.mean(x)

def quad(x,a,b,c,d,e):
  return (a*x**2)+(b*x)+c+(d*x**4)+(e*x**3)

####### IMPORT DATA ######

Sample_Temp = '11'

pattern = '*.txt'
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/SC020_3_A/6221-2182 DC IV/1p6K_NLIV_Data',pattern = pattern,type=workfile)

RvH = workfile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/SC020_3_A/6221-2182 DC IV/NLRvsHvsT/SC020_3_A_6221-2182 DC IV_Magnet Power Supply Multi-segment_0056 0.00_1.467200_NLRvH.txt')
avg = (max(RvH.column('b'))+min(RvH.column('b')))/2

# Create workfile to add all IV data to
P = workfile()
P.metadata=folder[0].metadata
AP = workfile()
AP.metadata=folder[0].metadata

for f in folder:        # Loop over files and combine voltage data in to one file
  fit = f.curve_fit(quad,'Current','Voltage', result=True, replace=False, header="fit",asrow=True)
  
  if fit[2]<avg:
    AP.add_column(f.Voltage,str(f.metadata['iterator']))
  else:
    P.add_column(f.Voltage,str(f.metadata['iterator']))
  
# Average voltage data

P.apply(func, 1, replace = False, header = 'Mean NLVoltage')
P.add_column(folder[1].column('Current'),'Current')
AP.apply(func, 1, replace = False, header = 'Mean NLVoltage')
AP.add_column(folder[1].column('Current'),'Current')  


# Fit Data

Pfit=P.curve_fit(quad,'Current','Mean NLVoltage',result=True,replace=False,header='fit',asrow=True)
APfit=AP.curve_fit(quad,'Current','Mean NLVoltage',result=True,replace=False,header='fit',asrow=True)
print Pfit
Pquad = Pfit[0]*P.column('Current')**2+Pfit[4]
APquad = APfit[0]*AP.column('Current')**2+APfit[4]

print P.column_headers

###Plot###

IV = workfile()
IV.metadata=P.metadata
IV.add_column(P.Current,'Current')
IV.add_column(P.column('Mean NLVoltage'),'P NLV')
IV.add_column(P.column('fit'),'P Fit')
IV.add_column(AP.column('Mean NLVoltage'),'AP NLV')
IV.add_column(AP.column('fit'),'AP Fit')

IV.template=SPF.JTBPlotStyle
IV.figure() # Creating new figures like this means we don;t reuse windows from run to run
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


IV.title = ''
IV.plot_xy("Current","P NLV",label = 'P',linestyle='-',marker='',linewidth=2) 
IV.plot_xy("Current","AP NLV",label = 'AP',linestyle='-',marker='',linewidth=2)
IV.plot_xy("Current","P Fit",label = 'P Fit',linestyle='--',marker='',linewidth=1) 
IV.plot_xy("Current","AP Fit",label = 'AP Fit',linestyle='--',marker='',linewidth=1)
IV.ylabel=r"$V_{NL}$ (V)"
IV.xlabel=r"I (A)"
plt.legend(loc='best')
plt.tight_layout()


