# -*- coding: utf-8 -*-
"""
Code to generate \Delta R_s vs Temperature from a folder containing nonlocal IVs at different fields and temperatures.

Assumes data is in a single folder with file name format:

<Sample ID>_<X-Y Measurement>_<2nd Parameter>_<iterator>_<Sample Temp>_<Injector Material>_<Max Current>_.txt

e.g. SC004_2_T_6221-2182 DC IV_Magnet Power Supply Multi-segment_1_5K_Py_NLIV_300uA_.txt

@author: py07jtb
"""

import numpy
import re
import Stoner.Analysis as Analysis
import matplotlib.pyplot as plt # pylab imports numpy namespace as well, use pyplot in scripts
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
from Stoner.Folders import DataFolder


class workfile(Analysis.AnalyseFile,SP.PlotFile):
    """A class that combines AnalyseFile and PlotFile together"""
    pass

def quad(x,a,b,c):
    return a*x**2 + b*x + c
 
def RsvsH(folder,keys):
    tmp = Analysis.AnalyseFile()
    tmp.column_headers=["T","P","Perr","AP","APerr","DR mV","DRerr","Voff","Ptest","APtest"]
    fit = Analysis.AnalyseFile()
    fit.column_headers = ['a','a_err','b','b_err','c','c_err','T']
    for f in folder:
        row_fit = numpy.append(f.curve_fit(quad,'Current','Voltage',result=True,header='Fit',asrow=True),f['Sample Temp'])        
        fit+=row_fit
    mid = (max(fit.column('b'))+min(fit.column('b')))/2
    P = fit.mean('b',bounds=lambda x:x>mid)
    Perr=0.0
    for i in fit.search('b',lambda x,y:x>mid,columns='b_err'):
        Perr+=i**2
    Perr = numpy.sqrt(Perr)
    AP = fit.mean('b',bounds = lambda x:x<mid)
    APerr=0.0
    for i in fit.search('b',lambda x,y:x<mid,columns='b_err'):
        APerr+=i**2
    APerr = numpy.sqrt(APerr)
    temperature = fit.mean('T')
    
    alpha = 1e3
    row = numpy.array([temperature,P*alpha,Perr*alpha,AP*alpha,APerr*alpha,(P-AP)*alpha,alpha*numpy.sqrt((Perr**2)+(APerr**2)),mid*alpha,P-mid,AP-mid])    
    tmp+=row
    return tmp   
    
####### IMPORT DATA ######
sample = 'SC004_8_B'

filedir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample.split('_')[0]+'/Transport/'+sample+'/NLIVvsHvsT_Py_Inj/'
filename = re.compile(sample+'_6221-2182 DC IV_Magnet Power Supply Multi-segment_(?P<iterator>\d*)_(?P<IV_Temp>\d*)K_(?P<inj>\w*)_NLIV_300uA_.txt')
folder = DataFolder(filedir, pattern = filename,type=workfile) # Use type to preset the DataFile subclass




####### CREATE OUTPUT FILE ######
DeltaR = workfile() #Avoid creating temporary python lists, use the final DataFile like object to hold the data
DeltaR.metadata=folder[0].metadata
DeltaR['Sample ID'] = folder[0]['Sample ID']
DeltaR.column_headers=["T","P","Perr","AP","APerr","DR mV","DRerr","Voff","Ptest","APtest"]
#Use the labels attribute to store plot labels that are differnt from column names
DeltaR.labels=[r'T (K)',r'$R_s(P)$ (mV/A)','Perr',r'$R_s(AP)$ (mV/A)','APerr',r'$\Delta R_s$ (mV/A)','DRerr mV',r'$R_s$ offset (mV/A)',"Test Columns"]


####### Group into Temp - walk group and colapse each temp into one file ######
folder.group('IV_Temp')
folder.walk_groups(RsvsH,group=True,replace_terminal=True)


###### Combine different tempertures into one file #######
for a in folder:
    DeltaR+=a[0]
  
DeltaR.sort("T")
DeltaR.template=SPF.JTBPlotStyle
DeltaR.figure() # Creating new figures like this means we don;t reuse windows from run to run
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday


###### Plot ##########
DeltaR.subplot(221)
DeltaR.title = sample
DeltaR.plot_xy("T","DR mV",yerr='DRerr',label = str(DeltaR['Sample ID']),linestyle='',marker='o') # Just having the yerr keyword will trigger the plotter to be an errorbar
DeltaR.subplot(222)
DeltaR.plot_xy("T","Voff",label = sample)
DeltaR.subplot(223)
DeltaR.plot_xy("T","P",yerr='Perr',label = 'P',linestyle='',marker='o')
DeltaR.plot_xy("T","AP",yerr='APerr',label = 'AP',linestyle='',marker='o')
DeltaR.ylabel=r"$R_s$ (mV/A)"
DeltaR.subplot(224)
DeltaR.plot_xy("T",'Ptest',label = 'P')
DeltaR.plot_xy("T",'APtest',label = 'AP')
DeltaR.ylabel="Tests"
plt.tight_layout()

###### Save File ######
DeltaR.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample.split('_')[0]+'/Transport/DeltaR_vs_Sep/' + sample + 'DeltaRsvsT.txt')


