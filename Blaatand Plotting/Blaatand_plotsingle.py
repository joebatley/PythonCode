

import numpy
import re
import Stoner
import Stoner.Analysis as Analysis
import pylab as plt
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
 
def lin(x,a):
  return x*a

####### IMPORT DATA ######

filename = '/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/DeltaRvsT/SC020_1_ADeltaRsvsT.txt'
#file = Stoner.CSVFile(filename,header_line=1, data_line=2, data_delim='\t', header_delim='\t')
file = Stoner.DataFile(filename)

a=Analysis.AnalyseFile(file)

print a.column_headers


#a.del_rows('Sample Temp',lambda x,y:x==0) 
#a.del_rows(0)
#a.del_rows('temp',lambda x,y: x<17.5)
#a.rename('DeltaR',r'$\Delta$R')
#a.rename('temp','T (K)')
#a.del_rows('Temperature',lambda x,y:x<7) 
#a.mulitply('Resistance',-1.0,replace=True,header=r'R ($\Omega$)')
#a.mulitply('m',1e-3,replace=True,header='m')
#a.rename('m',r'R (K$\Omega$)')
#a.rename('Control',r'$\mu_o$H (T)')


#rhoRT = numpy.pi*300e-10*(max(a.column('Resistance'))+4.07)*0.6/(2*numpy.log(2))
#rho = rhoRT/max(a.column('Resistance'))
#a.mulitply('Resistance',rho,replace=False,header=r'$\rho (\Omega$m)')
def offset(x,b,a):
    return numpy.exp((x-a)/b)

fit = a.curve_fit(offset,'Voff','T',p0=[-1.,100.],result=True,replace=False,header='fit',asrow=True)
print fit
p=SP.PlotFile(a)
print p.column_headers
p.template=SPF.JTBPlotStyle
label = ''
title = ' '
p.plot_xy('T','Voff',label = label,title=title,figure=1)
p.plot_xy('T','fit',label = label,title=title,figure=1)
#p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_5A_rhovT_.txt')






