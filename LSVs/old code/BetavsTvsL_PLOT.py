

import numpy
import re
from Stoner.Folders import DataFolder
import pylab as plt
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
import Stoner.Analysis as Analysis 



####### IMPORT DATA ######
Seperation = {1:'325 nm',
              2:'425 nm',
              3:'525 nm',
              4:'625 nm',
              5:'725 nm',
              6:'925 nm',
              7:'1125 nm',
              8:'1325 nm',
              9:'1525 nm',}
              
Marker = {1:'325 nm',
          2:'o',
          3:'x',
          4:'s',
          5:'v',
          6:'^',
          7:'>',
          8:'D',
          9:'<',}
              

pattern = '*.txt'
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Beta_vs_sep/Normalised Data',pattern = pattern)
folder.sort()
for f in folder:
  
  f=Analysis.AnalyseFile(f)
  print f.column_headers
  #f.rename('DeltaR err','Error')
  #f.rename('Sample Temp','Temperature (K)')
  #f.mulitply('DeltaR',1e3,replace=True,header=r'$\Delta \alpha$ (mV/A)')
  
  pattern = re.compile('_')     
  label = pattern.split(f['Sample ID'])  
  
  
  p=SP.PlotFile(f)
  p.setas="y.x"
  p.template=SPF.JTBPlotStyle
  p.template.template_lines_marker='x'#Marker[int(label[1])]
  print Marker[int(label[1])]
  title = r' '
  label = Seperation[int(label[1])]
  p.plot(label=label,figure=1,title=title)
  


