

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

filedir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/ISHE_Otani/6221-2182 DC IV/'
filename = 'ISHE_Otani 6221-2182 DC IV Magnet Power Supply Multi-segment 0086 0.00 9.529100K ISHE DCR 500uA 500mT.txt'
d = Stoner.DataFile(False)

a=Analysis.AnalyseFile(d)
#a.sort('Sample Temp')
print a.column_headers


#a.del_rows(0)
#a.del_rows('b',lambda x,y: x<0.0001)

###### Average UP and DOWN sweeps
'''
updown = split_up_down(a,'Control')

up = updown['rising'][0]
down = updown['falling'][0]

b_up = up.column('r')
b_down = down.column('r')
b_down = b_down[::-1]
b_down_interp = numpy.interp(up.column('Control'),down.column('Control'),b_down)
b_mean = 1e3*(b_up+b_down_interp)/2

avg = Analysis.AnalyseFile()
avg.add_column(b_mean,r'R$_s$ (mV/A)')
avg.add_column(up.column('Control'),r'$\mu_o$H (T)')


'''

mean = (max(a.column('b'))+min(a.column('b')))/2
print mean

P = a.mean('b',bounds = lambda x:x>mean)
Perr = numpy.std(a.search('b',lambda x,y:x>mean,columns='b'))/numpy.sqrt(len(a.search('b',lambda x,y:x>mean,columns='b')))
AP = a.mean('b',bounds = lambda x:x<mean)
APerr = numpy.std(a.search('b',lambda x,y:x<mean,columns='b'))/numpy.sqrt(len(a.search('b',lambda x,y:x<mean,columns='b')))

DR = P-AP
print DR
print numpy.sqrt((Perr**2)+(APerr**2))

##### Rename for plot
a.rename('b',r'R$_s$ (V/A)')
a.multiply(r'R$_s$ (V/A)',1e3,header = r'R$_s$ (mV/A)')
a.rename('Control',r'$\mu_o$H (T)')


p=SP.PlotFile(a)
print p.column_headers
#p.setas="...y.e.....x"
p.template=SPF.JTBPlotStyle
label = 'Py/Co/Cu'
title = 'T = 2 K, L = 400 nm'
p.plot_xy(r'$\mu_o$H (T)',r'R$_s$ (mV/A)',label = label,title=title,figure=1,linestyle='-',marker='')


#p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_5A_rhovT_.txt')





