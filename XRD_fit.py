# -*- coding: utf-8 -*-
"""
Created on Thu May 29 11:24:02 2014

@author: py07jtb
"""

import Stoner
from Stoner.Util import format_error
import numpy as np
import matplotlib.pyplot as pyplot
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP

class Keissig(Stoner.AnalyseFile,Stoner.PlotFile):
    pass


sensitivity=2
width = 7
critical_edge=0.8


### LOAD FILE ###

Sample_ID = 'SC018_5A_Co'

filename='/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/SC018_5A_LAS_1cps.dql'
d=Keissig(filename) #Load the low angle scan
d.rename('Counts','cps')
d.rename('Angle',r'2$\theta$')
d.add_column(lambda x:np.log(x[1]), 'log(Counts)') #Add column of log(Counts)

### Find peaks in data - Create data file with just peak positions
peaks = Stoner.AnalyseFile(d.interpolate(d.peaks(1,width,sensitivity,poly=4))) 
peaks.column_headers = d.column_headers

### Remove any spurious peaks from before critical edge 
peaks.del_rows(0, lambda x,y: x<critical_edge)




### Fit Kiessig data

#Now convert the angle to sin^2
peaks.apply(lambda x: np.sin((x[0]/2)*(np.pi/180))**2, 0,replace=False,header=r'sin($^2\theta$)')

lam=float(d['Lambda'])

diff = []
m = []
for i in range(len(peaks)-1):
    diff.append(peaks.column(r'sin($^2\theta$)')[i+1]-peaks.column(r'sin($^2\theta$)')[i])
    m.append(0.25*(2*(i+1)+1)*lam**2)

kiessig = Stoner.AnalyseFile()
kiessig.add_column(diff,column_header = r'$\theta_{n+1}^2-\theta_{n}^2$')
kiessig.add_column(m,column_header = r'$\lambda^2$(2l+1)/4')

def lin(x,m,c):
  return m*x+c

fit = kiessig.curve_fit(lin,0,1, result=True, replace=False, header="fit",asrow=True)
print fit

t = np.sqrt(fit[0])
terr = np.sqrt(fit[1])

print 'Thickness is: ' +str.format("{0:.0f}", t) + r' +- ' +str.format("{0:.0f}", terr) + r" A"


### Plot XRD data and peak positions

p1=SP.PlotFile(d.clone)
p1.setas="xy"
p1.template=SPF.JTBPlotStyle
label = Sample_ID
p1.plot(label = label,title="Thickness is: "+str.format("{0:.0f}", t)+" A",figure=1,linewidth=1,plotter=pyplot.semilogy,)

p2=SP.PlotFile(peaks.clone)
p2.setas=".xy."
p2.template=SPF.JTBPlotStyle
label = None
p2.plot(label = label,figure=1,linestyle='',marker='o',markersize=3,plotter=pyplot.semilogy,)




### Plot fit in subplot

p=SP.PlotFile(kiessig.clone)
p.template=SPF.JTBPlotStyle
pyplot.axes([0.5, 0.6, 0.35, 0.25])
p._template_font_size=1
p._template_axes_labelsize=2
p._template_text_fontsize=2
p._template_xtick_labelsize=1
p._template_font_size=1
p.setas="xy."
label = None
p.plot(label = label,figure=1,linestyle='-',marker='')
p.setas="x.y"
p.plot(label = label,figure=1,linestyle='',marker='o',markersize=3)


