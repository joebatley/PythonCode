# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 12:34:38 2014

@author: py07jtb
"""



import numpy
import re
import Stoner
import Stoner.Analysis as Analysis
import pylab as plt
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
 

sample = 'SC021_5_A'

####### IMPORT DATA ######

filedir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC021/Transport/SC021_5_A/6221-2182 DC IV/NLRvsHvsT/'
filename_P = 'SC021_5_A_6221-2182 DC IV_Timed interval_0000 0.00_2.171300K_NLRvsT_100mT.txt'
filename_AP = 'SC021_5_A_6221-2182 DC IV_Timed interval_0000 0.00_277.834000K_NLRvsT_0mT_AP.txt'
#A = Stoner.DataFile(False)


bin = 10.0
#t = numpy.arange(.0,280.0,10.0)
T0 = numpy.arange(2.0,3.0,1.0)
T1 = numpy.arange(10.0,100.0,10.0)
T2 = numpy.arange(100.0,200.0,20.0)
T3 = numpy.arange(200.0,280.0,25.0)
t = numpy.concatenate((T0,T1,T2,T3),axis=0)

p=Analysis.AnalyseFile(filedir+filename_P)
p.del_rows(0)
P = []
P_err = []
for i in t:
    rs_raw = []
    index = []
    for j in range(len(p.column('Sample Temp'))):
        if p.column('Sample Temp')[j]<(i+bin/2):
            if p.column('Sample Temp')[j]>(i-bin/2):
                rs_raw.append(p.column('Resistance')[j])
    #print rs_raw
    P.append(numpy.mean(rs_raw))
    P_err.append(numpy.std(rs_raw)/numpy.sqrt(len(rs_raw)))

    
ap=Analysis.AnalyseFile(filedir+filename_AP)
ap.del_rows(0)
AP = []
AP_err = []
for i in t:
    rs_raw = []
    index = []
    for j in range(len(ap.column('Sample Temp'))):
        if ap.column('Sample Temp')[j]<(i+bin/2):
            if ap.column('Sample Temp')[j]>(i-bin/2):
                rs_raw.append(ap.column('Resistance')[j])
    #print rs_raw
    AP.append(numpy.mean(rs_raw))
    AP_err.append(numpy.std(rs_raw)/numpy.sqrt(len(rs_raw)))
    
DR =   (numpy.array(P)-numpy.array(AP))*1e3  
DRerr = (numpy.sqrt(numpy.array(P_err)**2 + numpy.array(AP_err)**2))*1e3 
Roff =  1e3*((numpy.array(P)+numpy.array(AP))/2) 
Ptest = numpy.array(P)-Roff
APtest = numpy.array(AP)-Roff 
    
DelR = Analysis.AnalyseFile()
DelR.metadata=p.metadata
DelR.add_column(t,'T')
DelR.add_column(P,'P')
DelR.add_column(P_err,'Perr') 
DelR.add_column(AP,'AP')
DelR.add_column(AP_err,'APerr') 
DelR.add_column(DR,'DR mV')
DelR.add_column(DRerr,'DRerr')
DelR.add_column(Roff,'Voff')
DelR.add_column(Ptest,'Ptest')
DelR.add_column(APtest,'APtest')


p=SP.PlotFile(DelR.clone)
print p.column_headers
#p.setas="...y.e.....x"
p.template=SPF.JTBPlotStyle
label = ''
title = ' '
#p.plot_xy('T (K)',r'$\Delta R_s$ (V/A)',plotter=plt.errorbar,yerr='DRerr',label = label,title=title,figure=1)
#p.plot_xy('T (K)',[r'$R_s(P)$ (V/A)',r'$R_s(AP)$ (V/A)'],plotter=plt.errorbar,yerr=[r'$R_s(P)_err$ (V/A)',r'$R_s(AP)_err$ (V/A)'],label = label,title=title,figure=2)
#p['Sample ID'] = sample
p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample.split('_')[0]+'/Transport/DeltaRvsT/' + sample + 'DeltaRsvsT.txt')



