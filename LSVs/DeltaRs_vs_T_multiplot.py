"""

File to plot \Delta R_s as a function of T for multipul seperations on one graph

"""

import numpy
import Stoner.Analysis as Analysis
import matplotlib.pyplot as plt # pylab imports numpy namespace as well, use pyplot in scripts
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
from Stoner.Folders import DataFolder


class workfile(Analysis.AnalyseFile,SP.PlotFile):
    """A class that combines AnalyseFile and PlotFile together"""
    pass

####### Define seperation lengths for labels######
Seperation = {'1A':'300 nm',
              '1B':'400 nm',
              '2A':'500 nm',
              '2B':'600 nm',
              '3A':'700 nm',
              '5A':r'1.2 $\mu$m',
              '5B':r'1.4 $\mu$m',}
              
              
####### IMPORT DATA ######
FileDir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC021/Transport/DeltaRvsT/'
pattern = '*DeltaRsvsT.txt'
folder = DataFolder(FileDir,pattern = pattern,type=workfile)
print folder
folder.sort()


####### Iterate through files ######
for f in folder:
  f.template=SPF.JTBPlotStyle
  ID = f['Sample ID'].split('_')
  print ID
  
  f.labels=[r'T (K)',r'$R_s(P)$ (mV/A)','Perr',r'$R_s(AP)$ (mV/A)','APerr',r'$\Delta R_s$ (mV/A)','DRerr mV',r'$R_s$ offset (mV/A)',"Test Columns"] 
  f.plot_xy('T','Voff',label=Seperation[ID[1]+ID[2]],figure=1,title=ID[0],linestyle='--',marker='o')
  f.plot_xy('T','DR mV',label=Seperation[ID[1]+ID[2]],figure=2,title=ID[0],linestyle='--',marker='o')
  

