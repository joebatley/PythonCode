# -*- coding: utf-8 -*-
"""
Code to analyse the peak position in \DeltaR vs T.


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

###### Define dicts to link sample ID ans seperation ######
sc004 = {1:325e-9,2:425e-9,3:525e-9,4:625e-9, 5:725e-9, 6:925e-9,7:1125e-9, 8:1325e-9, 9:1525e-9,} 
sc020 = {'1A':300e-9,'1B':400e-9,'2A':500e-9,'2B':600e-9,'3A':700e-9,'3B':800e-9,'5A':1200e-9,'5B':1400e-9,}
    
####### IMPORT DATA ######
sample = 'SC021_8_B'

filedir = '/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample.split('_')[0]+'/Transport/DeltaRvsT/'
filename = '*DeltaRsvsT.txt'
folder = DataFolder(filedir, pattern = filename,type=workfile) # Use type to preset the DataFile subclass


##### Create output workfile ######
peak = workfile()
peak.column_headers = ['L','Tp','Tp_err' 'dRs_l', 'dRs_h','dRs','dRs_err']
peak.labels = ['L (m)','T$_{peak}$','Tp_err',r'$\delta R_s$LT',r'$\delta R_s$HT',r'$\delta R_s$',r'$\delta R_s$ err']


###### Loop over files - each file is a different seperation DR_s vs T #######
for f in folder:
    
    ###### Find Peak Position ######
    minDR = float(f.search('T',lambda x,y:x==min(f.column('T')),'DR mV'))   # Find DR at lowest temperature
    T_peak_max = max(f.search('DR mV',lambda x,y:x>minDR,'T'))              # Find Temp that has the same DR as minDR (other side of peak)
    t = numpy.arange(f.min('T')[0],T_peak_max,1)
    #f.plot_xy('T','DR mV')
    f.data = f.interpolate(t,kind='linear',xcol='T')
    f.add_column(t,'Tinter')
    fit = f.curve_fit(quad,'Tinter','DR mV',bounds=lambda x,y:x<T_peak_max,result=True,header='Fit',asrow=True)
    f.template=SPF.JTBPlotStyle
    #f.plot_xy('Tinter',['DR mV','Fit'])
    f.divide('DR mV',f.max('Fit')[0],replace=False,header='DRnorm')
    #f.plot_xy('T','DRnorm',figure=20)
    Tpeak = f.column('T')[f.max('Fit')[1]]
    tmp = -fit[2]/(2*fit[0]) 
    err = tmp*numpy.sqrt((fit[1]/fit[0])**2+(fit[3]/fit[2])**2)
    print Tpeak,tmp,err
    
    ####### Find dR #######
    dR_lt = (f.max('Fit')[0]-minDR)
    dR_ht = (f.max('Fit')[0]-float(f.search('T',lambda x,y:x==max(f.column('T')),'DR mV')))
    dR = dR_lt/dR_ht
    dRerr = dR*numpy.sqrt((float(f.search('T',lambda x,y:x==max(f.column('T')),'DRerr')))**2+(float(f.search('T',lambda x,y:x==min(f.column('T')),'DRerr')))**2)
    ###### Find device seperation #######
    if sample.split('_')[0] == 'SC004':
        sep = sc004[int(f['Sample ID'].split('_')[1])]
    else:
        sep = sc020[f['Sample ID'].split('_')[1]+f['Sample ID'].split('_')[2]]
    row = numpy.array([sep,Tpeak,err,dR_lt,dR_ht,dR,dRerr])
    peak+=row


peak.template=SPF.JTBPlotStyle
peak.figure() # Creating new figures like this means we don;t reuse windows from run to run
f=plt.gcf()
f.set_size_inches((5.5,3.75),forward=True) # Set for A4 - will make wrapper for this someday

plt.subplot2grid((2,2),(0,0))
peak.title = sample
peak.plot_xy('L','Tp',yerr='Tp_err',label = sample.split('_')[0],linestyle='',marker='o') 
plt.subplot2grid((2,2),(0,1))
peak.plot_xy('L','dRs_l',label = 'LT',linestyle='',marker='o')
peak.plot_xy('L','dRs_h',label = 'HT',linestyle='',marker='o')
peak.ylabel=r'$\delta R_s$'
plt.subplot2grid((2,2),(1,0),colspan=2)
peak.plot_xy('L','dRs',yerr='dRs_err',label = 'HT',linestyle='',marker='o')
peak.ylabel=r'$\delta R_s$'
plt.tight_layout()

