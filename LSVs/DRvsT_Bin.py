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
 

sample = 'SC020_5_B'

####### IMPORT DATA ######

filedir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/SC020_5_B/6221-2182 DC IV/NLRvsHvsT/'
filename_P = 'SC020_5_B_6221-2182 DC IV_Timed interval_0000 0.00_2.863500K_NLRvsT_n100mT.txt'
filename_AP = 'SC020_5_B_6221-2182 DC IV_Timed interval_0000 0.00_214.978000K_NLRvsT_n20mT.txt'
#A = Stoner.DataFile(False)


bin = 10.0
t = numpy.arange(5.0,280.0,10.0)

p=Analysis.AnalyseFile(filedir+filename_P)
p.del_rows(0)
Rs = []
Rs_err = []
for i in t:
    rs_raw = []
    index = []
    for j in range(len(p.column('Sample Temp'))):
        if p.column('Sample Temp')[j]<(i+bin/2):
            if p.column('Sample Temp')[j]>(i-bin/2):
                rs_raw.append(p.column('Resistance')[j])
    print rs_raw
    Rs.append(numpy.mean(rs_raw))
    Rs_err.append(numpy.std(rs_raw)/numpy.sqrt(len(rs_raw)))
P = Analysis.AnalyseFile()
P.add_column(t,'T (K)')
P.add_column(Rs,r'$R_s(P)$ (V/A)')
P.add_column(Rs_err,r'$R_s(P)_err$ (V/A)')

    
ap=Analysis.AnalyseFile(filedir+filename_AP)
ap.del_rows(0)
Rs = []
Rs_err = []
for i in t:
    rs_raw = []
    index = []
    for j in range(len(ap.column('Sample Temp'))):
        if ap.column('Sample Temp')[j]<(i+bin/2):
            if ap.column('Sample Temp')[j]>(i-bin/2):
                rs_raw.append(ap.column('Resistance')[j])
    print rs_raw
    Rs.append(numpy.mean(rs_raw))
    Rs_err.append(numpy.std(rs_raw)/numpy.sqrt(len(rs_raw)))
P.add_column(Rs,r'$R_s(AP)$ (V/A)')
P.add_column(Rs_err,r'$R_s(AP)_err$ (V/A)')    
    
    
P.subtract(r'$R_s(P)$ (V/A)',r'$R_s(AP)$ (V/A)',replace=False,header=r'$\Delta R_s$ (V/A)')
DRerr = numpy.sqrt(P.column(r'$R_s(P)_err$ (V/A)')**2 + P.column(r'$R_s(AP)_err$ (V/A)')**2)
P.add_column(DRerr,'DRerr')
print P


p=SP.PlotFile(P)
print p.column_headers
#p.setas="...y.e.....x"
p.template=SPF.JTBPlotStyle
label = ''
title = ' '
p.plot_xy('T (K)',r'$\Delta R_s$ (V/A)',plotter=plt.errorbar,yerr='DRerr',label = label,title=title,figure=1)
p.plot_xy('T (K)',[r'$R_s(P)$ (V/A)',r'$R_s(AP)$ (V/A)'],plotter=plt.errorbar,yerr=[r'$R_s(P)_err$ (V/A)',r'$R_s(AP)_err$ (V/A)'],label = label,title=title,figure=2)
p['Sample ID'] = sample
p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample.split('_')[0]+'/Transport/DeltaRvsT/' + sample + 'DeltaRsvsT.txt')



