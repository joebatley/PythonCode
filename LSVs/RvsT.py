

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

#filedir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/SC020_1_B/6221-2182 DC IV/'
#filename = 'SC020_1_B_6221-2182 DC IV_Timed interval_0000 1.55_Inj_RvT.txt'
#file = Stoner.DataFile(filedir+filename)


a=Analysis.AnalyseFile(False)

a.del_rows(0)
a.rename('temp','T (K)')
a.sort('T (K)')
#a.rename('Resistance',r'R ($\Omega$)')



# CALCULATE RESISTIVITY OF CU BAR

w = 600e-9
t = 30e-9
l = 30e-6
res = w*t/l
a.mulitply('Resistance',res,replace=False,header=r'$\rho (\Omega$m)')


p=SP.PlotFile(a)
print p.column_headers
p.template=SPF.JTBPlotStyle
label = str(a['Sample ID'])
title = ' '
p.plot_xy('T (K)',r'$\rho (\Omega$m)',label = label,title=title,figure=2)

p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+p['Sample ID'].split('_')[0]+'/Transport/DeltaRvsT/'+ p['Sample ID']+'_resistivity_vs_T.txt')






                                                                                                                                                                                                                                                                                                   