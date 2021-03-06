

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

filedir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC021/Transport/SC021_1_B/6221-2182 DC IV/'
filename = 'SC021_1_B_6221-2182 DC IV_Timed interval_0000 3.53_CuBar_RvT.txt'
d = Stoner.DataFile(filedir+filename)


a=Analysis.AnalyseFile(d.clone)


a.del_rows(0)
a.del_rows('Temp',lambda x,y:x>9.1 and x < 10.1)
a.rename('emp','T (K)')
a.sort('T (K)')

#a.rename('Resistance',r'R ($\Omega$)')



# CALCULATE RESISTIVITY OF CU BAR

w = 150e-9
t = 120e-9
l = 270e-9
res = w*t/l
a.multiply('Resistance',res,replace=False,header='res')

'''
print a.column_headers
for col in a.column_headers:
    if col==r'$\rho$ ($\Omega$ m)':
        a.rename(r'$\rho$ ($\Omega$ m)',r'$\rho (\Omega$m)')
        a.divide(r'$\rho (\Omega$m)',min(a.column(r'$\rho (\Omega$m)')),replace=False,header=r'R/R$_{min}$')
'''    

p=SP.PlotFile(a)
print p.column_headers
p.template=SPF.JTBPlotStyle
label = ''#str(a['Sample ID'])
title = ' '
p.plot_xy('T (K)','res',label = label,title=title,figure=2)


p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC021/Transport/Scattering Analysis/'+ p['Sample ID']+'_Cu_resistivity_vs_T.txt')






                                                                                                                                                                                                                                                                                                   