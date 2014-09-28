# -*- coding: utf-8 -*-
"""
SC004 

Plot Rs vs T for P and AP.

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
  
Seperation = {1:'325 nm',2:'425 nm',3:'525 nm',4:'625 nm', 5:'725 nm', 6:'925 nm',7:'1125 nm', 8:'1325 nm', 9:'1525 nm',} 

### Read in Data ###  
pattern = '*DeltaRsvsT.txt'
folder = DataFolder('/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaRvsT',pattern = pattern,type=workfile)  
folder.sort('Sample ID')  
plot = [2,4,6,7]
for Rs in folder:
    if int(Rs['Sample ID'].split('_')[1]) in plot:
        print Rs.column_headers
        Rs.template=SPF.JTBPlotStyle
        Rs.figure(1) # Creating new figures like this means we don;t reuse windows from run to run
        f=plt.gcf()
        f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday
    
        #Rs.title = ''
        label = Seperation[int(Rs['Sample ID'].split('_')[1])]
        Rs.plot_xy("T","Voff",label =label ,linestyle='',marker='o',linewidth=2,markersize=5)
        #Rs.ylabel = r"$\Delta R_s$ (mV/A)"
        Rs.ylabel=r"$\frac{R_{s}^P + R_{s}^{AP}}{2}\ $ (mV/A)"
        Rs.xlabel=r"T (K)"
    
        plt.legend(loc='best')
plt.tight_layout()
  
  
  
  
  
