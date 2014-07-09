

import numpy
import re
import Stoner
import Stoner.Analysis as Analysis
import pylab as plt
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
from Stoner.Util import split_up_down
from scipy.interpolate import interp1d

def lin(x,a):
  return x*a


Seperation = {1:325e-9,
              2:425e-9,
              3:525e-9,
              4:625e-9,
              5:725e-9,
              6:925e-9,
              7:1125e-9,
              8:1325e-9,
              9:1525e-9,}
####### IMPORT DATA ######

filedir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaR_vs_Sep/Plot/'

folder = Stoner.DataFolder(filedir, pattern = '*.txt')

dRs = []
dRserr = []
L = []

for f in folder:
  maxDRerr = f.search('DeltaR',lambda x,y:x==max(f.column('DeltaR')),'DeltaR err')
  minDRerr = f.column('DeltaR err')[0]
  print maxDRerr
  dRserr = (f.column('DeltaR')[0]/max(f.column('DeltaR')))*numpy.sqrt((maxDRerr/max(f.column('DeltaR')))**2 + (minDRerr/f.column('DeltaR')[0])**2)
  dRs.append((max(f.column('DeltaR'))-f.column('DeltaR')[0])/max(f.column('DeltaR')))
  key = f['Sample ID'].split('_') 
  L.append(Seperation[int(key[1])])



p=SP.PlotFile()
p.add_column(L,column_header='L (m)')
p.add_column(dRs,column_header='$\delta R_s$')
p.add_column(dRserr,column_header='$\delta R_s err$')
p.sort('L (m)')
print p.column_headers
p.setas="xye"
p.template=SPF.JTBPlotStyle
label = ''
title = ' '
p.plot(label = label,title=title,figure=1)





