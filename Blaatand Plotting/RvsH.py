

import numpy
import re
import Stoner
import Stoner.Analysis as Analysis
import pylab as plt
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
import Stoner.Util as U
 
def lin(x,a):
  return x*a

####### IMPORT DATA ######

filename = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_4A_rhovT_.txt'
#file = Stoner.CSVFile(filename,header_line=1, data_line=2, data_delim='\t', header_delim='\t')
file = Stoner.DataFile(False)

a=Analysis.AnalyseFile(file)

print a.column_headers

P = numpy.mean(a.search('Control',lambda x,y:x>0.3,'r'))
Perr = numpy.std(a.search('Control',lambda x,y:x>0.3,'r'))/len(a.search('Control',lambda x,y:x>0.3,'r'))
N = numpy.mean(a.search('Control',lambda x,y:x<-0.3,'r'))
Nerr = numpy.std(a.search('Control',lambda x,y:x<-0.3,'r'))/len(a.search('Control',lambda x,y:x<-0.3,'r'))
DR = P-N
DRerr = numpy.sqrt(Perr**2 + Nerr**2)
print DR
print DRerr

split = U.split_up_down(a,'Control')
print split['falling'][0].column('Control')
print split['rising'][0].column('Control')

#a.del_rows('Sample Temp',lambda x,y:x==0) 
#a.del_rows(0)
#a.del_rows('temp',lambda x,y: x<17.5)
#a.rename('DeltaR',r'$\Delta$R')
#a.rename('temp','T (K)')
#a.del_rows('Temperature',lambda x,y:x<7) 
#a.mulitply('Resistance',-1.0,replace=True,header=r'R ($\Omega$)')
#a.mulitply('m',1e-3,replace=True,header='m')
a.multiply('r',1e3,replace=True,header=r'R (m$\Omega$)')
a.rename('Control',r'$\mu_o$H (T)')

'''
rhoRT = numpy.pi*300e-10*(max(a.column('Resistance'))+4.07)*0.6/(2*numpy.log(2))
rho = rhoRT/max(a.column('Resistance'))
a.mulitply('Resistance',rho,replace=False,header=r'$\rho (\Omega$m)')
'''



p=SP.PlotFile(a)
print p.column_headers
#p.setas="...y.e.....x"
p.template=SPF.JTBPlotStyle
label = ''#str(a['Sample ID'])
title = ' '
p.plot_xy(r'$\mu_o$H (T)',r'R (m$\Omega$)',label = label,title=title,figure=1,linestyle='-')
#p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_5A_rhovT_.txt')






