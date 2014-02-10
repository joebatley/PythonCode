

import numpy
from Stoner.Folders import DataFolder
import pylab as plt
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
 



####### IMPORT DATA ######



folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Beta_vs_sep/Normalised Data',pattern = '*.txt')

for f in folder:
  f.rename('Beta',r'$\beta$/R$_{Inj}$')
  p=SP.PlotFile(f)
  p.setas="y.x"
  p.template=SPF.DefaultPlotStyle
  title = r'$\beta$/R$_{Inj}$ vs temperature'
  p.plot(label=p['Sample ID'],figure=1,title=title)
  


