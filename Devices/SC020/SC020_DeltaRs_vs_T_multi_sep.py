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
  
Seperation = {'1A':300e-9,'1B':400e-9,'2A':500e-9,'2B':600e-9,'3A':700e-9,'3B':800e-9,'4A':900e-9,'5A':1200e-9,'5B':1400e-9,}

### Read in Data ###  
pattern = '*.txt'
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/Polyfit Analysis',pattern = pattern,type=workfile)  
folder.sort('Sample ID')  
plot = [1,2,3,5]
for Rs in folder:
    if int(Rs['Sample ID'].split('_')[1]) in plot:
        Rs.template=SPF.JTBPlotStyle
        Rs.figure(1) # Creating new figures like this means we don;t reuse windows from run to run
        f=plt.gcf()
        f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday
    
        Rs.title = ''
        label = Seperation[str(Rs['Sample ID'].split('_')[1]+Rs['Sample ID'].split('_')[2])]
        Rs.plot_xy("T","quad",yerr='quad.err',label =Rs['Sample ID'] ,linestyle='',marker='o',linewidth=2,markersize=5) 
        #Rs.ylabel=r"$\Delta R_{s}$ (V/A)"
        #Rs.ylabel=r"$\beta$ (V/A$^2$)"
        #Rs.ylabel=r"I$^3$ Coef (V/A$^3$)"
        Rs.ylabel=r"I$^4$ Coef (V/A$^4$)"
        Rs.xlabel=r"T (K)"
    
plt.legend(loc='best')
plt.tight_layout()
  
  
  
  
  
