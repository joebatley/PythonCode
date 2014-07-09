

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

####### IMPORT DATA ######

filedir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC021/Transport/SC021_2_A/6221-2182 DC IV/NLIVvsHvsT/'
filename = 'SC021_2_A_6221-2182 DC IV_Magnet Power Supply Multi-segment_0034 0.00_250.354000K_NLRvsH.txt'
d = Stoner.DataFile(False)

a=Analysis.AnalyseFile(d)
a.sort('Sample Temp')
print a.column_headers


#a.del_rows(0)
#a.del_rows('b',lambda x,y: x<0.0001)

###### Average UP and DOWN sweeps
'''
updown = split_up_down(a,'Control')

up = updown['rising'][0]
down = updown['falling'][0]

b_up = up.column('b')
b_down = down.column('b')
b_down = b_down[::-1]
b_down_interp = numpy.interp(up.column('Control'),down.column('Control'),b_down)
b_mean = 1e3*(b_up+b_down_interp)/2

avg = Analysis.AnalyseFile()
avg.add_column(b_mean,r'R$_s$ (mV/A)')
avg.add_column(up.column('Control'),r'$\mu_o$H (T)')
'''

'''
##### Rename for plot
a.rename('b',r'R$_s$ (V/A)')
a.mulitply(r'R$_s$ (V/A)',1e3,header = r'R$_s$ (mV/A)')
a.rename('Control',r'$\mu_o$H (T)')


p=SP.PlotFile(a)
print p.column_headers
#p.setas="...y.e.....x"
p.template=SPF.JTBPlotStyle
label = str(a['Sample ID']) + ' at ' + str.format("{0:.0f}",a['Sample Temp']) + ' K'
title = ' '
p.plot_xy(r'$\mu_o$H (T)',r'R$_s$ (mV/A)',label = label,title=title,figure=1)
'''

#p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_5A_rhovT_.txt')





