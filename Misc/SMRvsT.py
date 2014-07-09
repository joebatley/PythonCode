#from scipy import *
from scipy import interpolate
import Stoner.Analysis as Analysis
import pylab as plt
import numpy
import Stoner
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP



### IMPORT DATA ###

a=Analysis.AnalyseFile('/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SPH033_5/20140608/6221-2182 DC IV/SPH033_5_6221-2182 DC IV_Timed interval_0000 0.00_30uA_RvT_alpha_0_200mT.txt')   #import a single data file ready to use the Analysis class
a.sort('Sample Temp')
b=Analysis.AnalyseFile('/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SPH033_5/20140608/6221-2182 DC IV/SPH033_5_6221-2182 DC IV_Timed interval_0000 0.00_30uA_RvT_alpha_90_200mT.txt')   #import a single data file ready to use the Analysis class
b.sort('Sample Temp')
###arrange###

sdev_a = numpy.zeros(len(a.column('m'))/bin) 
Res_a = numpy.zeros(len(a.column('m'))/bin)
Temp_a = numpy.zeros(len(a.column('m'))/bin)

for i in range(0,len(a.column('m')),bin):
    if i<(len(a.column('m'))/bin)*bin:
        tot = 0.0
        for j in range(0,bin):
            tot = tot + a.column('m')[i+j]
        Res_a[i/bin] = tot/bin   
        Temp_a[i/bin] = ((a.column('Sample Temp')[i]-a.column('Sample Temp')[i+bin-1])/2)+a.column('Sample Temp')[i+bin-1]
        sdev=0
        for p in range(0,bin):
            sdev = sdev + (a.column('m')[i+j]-Res_a[i/bin])**2
        sdev_a[i/bin] = numpy.sqrt(sdev)/bin   
        
sdev_b = numpy.zeros(len(b.column('m'))/bin) 
Res_b = numpy.zeros(len(b.column('m'))/bin)
Temp_b = numpy.zeros(len(b.column('m'))/bin)

for i in range(0,len(b.column('m')),bin):
    if i<(len(b.column('m'))/bin)*bin:
        tot = 0.0
        for j in range(0,bin):
            tot = tot + b.column('m')[i+j]
        Res_b[i/bin] = tot/bin   
        Temp_b[i/bin] = ((b.column('Sample Temp')[i]-b.column('Sample Temp')[i+bin-1])/2)+b.column('Sample Temp')[i+bin-1]
        sdev=0
        for p in range(0,bin):
            sdev = sdev + (b.column('m')[i+j]-Res_b[i/bin])**2
        sdev_b[i/bin] = numpy.sqrt(sdev)/bin  
        
A = interpolate.interp1d(Temp_a,Res_a)
B = interpolate.interp1d(Temp_b,Res_b)
print max(Temp_b),min(Temp_b)
T = numpy.arange(5,290,1) 
print B(T)
R=Analysis.AnalyseFile()
R.add_column(T,'T (K)')
R.add_column(A(T)-B(T),r'\Delta R ($\Omega$)')
                   
p=SP.PlotFile(R.clone)               #PLOT
p.template=SPF.JTBPlotStyle
title = ''
label = r'$\alpha$ = 90'
p.plot_xy('T (K)',r'\Delta R ($\Omega$)',label=label,figure=1,title=title)
                   
