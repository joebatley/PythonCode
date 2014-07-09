

import numpy
from Stoner.Folders import DataFolder
import pylab as plt
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
import Stoner.Analysis as Analysis 



####### IMPORT DATA ######


pattern = '*.txt'
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/Cu Resistivity',pattern = pattern)
folder.sort()
for f in folder:
  
  f=Analysis.AnalyseFile(f)
  f.subtract(r'$\rho (\Omega$m)',min(f.column(r'$\rho (\Omega$m)')),replace=True,header=r'$\rho (\Omega$m)')
  #print f.column_headers
  #f.rename('DeltaR err','Error')
  #f.rename('Sample Temp','Temperature (K)')
  #if f.column('Resistance')[0]<0:
  #  f.mulitply('Resistance',-1.0,replace=True,header=r'Resistance')
  
  #f.subtract('$Mean\\alpha^{\\plus}$','$Mean\\alpha^{\\minus}$',replace=False,header='Diff')  
  
  #diff = (max(f.column('Diff'))-min(f.column('Diff')))*100

  #print f['Sample ID'],diff  
  
  #print f.column_headers
  p=SP.PlotFile(f)
  print p.column_headers
  #p.setas="y....x"
  p.template=SPF.JTBPlotStyle
  title = r' '
  label = p['Sample ID']
  p.plot_xy('T (K)',r'$\rho (\Omega$m)',label=label,figure=1,title=title)
  


