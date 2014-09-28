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

def quad(x,a,b,c,d):
  return (a*x**4)+(b*x**2)+(c*x)+d

####### IMPORT DATA ######

Sample_Temp = '30'

pattern = re.compile(Sample_Temp + 'K_(?P<state>\w*)_NLIV_300uA_')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_2_T/NLIVvsHvsT_Py_Inj',pattern = pattern)

# Create workfile to add all IV data to
P = workfile()
P.metadata=folder[0].metadata
AP = workfile()
AP.metadata=folder[0].metadata

for f in folder:        # Loop over files and combine voltage data in to one file
  APiterator = [5,10]
  if f['iterator'] in APiterator:
    AP.add_column(f.Voltage,str(f.metadata['iterator']))
  else:
    P.add_column(f.Voltage,str(f.metadata['iterator']))
  
# Average voltage data
print P
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
IV.multiply('Current',1e6,replace=True,header='Current')
IV.add_column(P.column('Mean NLVoltage'),'P NLV')
IV.multiply('P NLV',1e6,replace=True,header='P NLV')
IV.add_column(P.column('fit'),'P Fit')
IV.add_column(AP.column('Mean NLVoltage'),'AP NLV')
IV.multiply('AP NLV',1e6,replace=True,header='AP NLV')
IV.add_column(AP.column('fit'),'AP Fit')

IV.template=SPF.JTBPlotStyle
IV.figure() # Creating new figures like this means we don;t reuse windows from run to run
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


IV.title = ''
IV.plot_xy("Current","P NLV",label = 'P',linestyle='-',marker='',linewidth=2) 
IV.plot_xy("Current","AP NLV",label = 'AP',linestyle='-',marker='',linewidth=2)
#IV.plot_xy("Current","P Fit",label = 'P Fit',linestyle='--',marker='',linewidth=1) 
#IV.plot_xy("Current","AP Fit",label = 'AP Fit',linestyle='--',marker='',linewidth=1)
IV.ylabel=r"$V_{NL}$ ($\mu$V)"
IV.xlabel=r"I ($\mu$A)"
plt.legend(loc='best')
plt.tight_layout()


