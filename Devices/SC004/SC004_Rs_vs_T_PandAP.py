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
  


### Read in Data ###  
pattern = 'SC004_2_TDeltaRsvsT.txt'
folder = DataFolder('/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaRvsT',pattern = pattern,type=workfile)  
  
Rs = folder[0]

Rs.template=SPF.JTBPlotStyle
Rs.figure() # Creating new figures like this means we don;t reuse windows from run to run
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


Rs.title = ''
Rs.plot_xy("T","P",label = 'P',linestyle='',marker='o',linewidth=2,markersize=5) 
Rs.plot_xy("T","AP",label = 'AP',linestyle='',marker='o',linewidth=2,markersize=5) 

Rs.ylabel=r"$R_{s}$ (mV/A)"
Rs.xlabel=r"T (K)"
plt.legend(loc='best')
plt.tight_layout()
  
  
  
  
  
