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

Sample_Temp = '11'

pattern = re.compile(Sample_Temp + 'K_(?P<state>\w*)_NLIV_300uA_')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/NLIVvsHvsT_Py_Inj',pattern = pattern)

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


# define objective function: returns the array to be minimized
def fcn2min(params, I, V):
    """ model NLIV """
    a = params['a'].value
    
    c = params['c'].value
    d = params['d'].value

    model = (a*I**2)+(c*I)+d
    return model - V

# create a set of Parameters
params = Parameters()
params.add('a',   value= -1000000)

params.add('c', value= 1e-6)
params.add('d', value= 0)


# do fit, here with leastsq model
result = minimize(fcn2min, params, args=(P.column('Current'), P.column('NLV')))

# calculate final result
final = P.column('NLV') + result.residual

# write error report
report_fit(params)



###Plot###

IV = workfile()
IV.metadata=P.metadata
IV.add_column(P.Current,'Current')
IV.add_column(P.column('Mean NLVoltage'),'P NLV')
IV.add_column(AP.column('Mean NLVoltage'),'AP NLV')

IV.template=SPF.JTBPlotStyle
IV.figure() # Creating new figures like this means we don;t reuse windows from run to run
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


IV.title = ''
IV.plot_xy("Current","P NLV",label = 'P',linestyle='-',marker='',linewidth=2) 
IV.plot_xy("Current","AP NLV",label = 'AP',linestyle='-',marker='',linewidth=2)
IV.ylabel=r"$V_{NL}$ (V)"
IV.xlabel=r"I (A)"
plt.legend(loc='best')
plt.tight_layout()


