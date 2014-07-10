

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

filedir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Blaatand/SC018_2/SC018_2_WA_1/20140612/6221-2182 DC IV/'
filename = 'SC018_2_WA_1_6221-2182 DC IV_Timed interval_0000 0.00_RvsT_!0000.txt'
d = Stoner.DataFile(False)


a=Analysis.AnalyseFile(d.clone)

'''
a.del_rows(0)
a.rename('emp','T (K)')
a.sort('T (K)')

#a.rename('Resistance',r'R ($\Omega$)')



# CALCULATE RESISTIVITY OF CU BAR

w = 1130e-9
t = 100e-9
l = 30e-6
res = w*t/l
a.mulitply('Resistance',res,replace=False,header=r'$\rho (\Omega$m)')
'''
print a.column_headers
for col in a.column_headers:
    if col==r'$\rho$ ($\Omega$ m)':
        a.rename(r'$\rho$ ($\Omega$ m)',r'$\rho (\Omega$m)')
        
a.divide(r'$\rho (\Omega$m)',min(a.column(r'$\rho (\Omega$m)')),replace=False,header=r'R/R$_{min}$')


p=SP.PlotFile(a)
print p.column_headers
p.template=SPF.JTBPlotStyle
label = str(a['Sample ID'])
title = ' '
p.plot_xy('T (K)',r'R/R$_{min}$',label = label,title=title,figure=2)


#p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Blaatand/SC018_2/Resistivity/'+ p['Sample ID']+'_resistivity_vs_T.txt')






                                                                                                                                                                                                                                                                                                   