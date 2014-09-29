

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

class workfile(Analysis.AnalyseFile,SP.PlotFile):
    """A class that combines AnalyseFile and PlotFile together"""
    pass

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
p=workfile(split['falling'][0])
q=workfile(split['rising'][0])


p.multiply('r',1e3,replace=True,header='r')
q.multiply('r',1e3,replace=True,header='r')

p.add_column(q.column('r')[::-1],column_header='q',replace=False)
p.add('r','q',replace=False,header='sum')
p.divide('sum',2.0,replace=True,header='avg')

p.template=SPF.JTBPlotStyle
q.template=SPF.JTBPlotStyle

q.plot_xy('Control','r',label = None,title=None,figure=1,linestyle='-',color='r')
p.plot_xy('Control','r',label = None,title=None,figure=1,linestyle='-',color='k')
p.xlabel = r'$\mu_o$H (T)'
p.ylabel = r'R (m$\Omega$)'
p.plot_xy('Control','avg',label = None,title=None,figure=2,linestyle='-',color='k')
p.xlabel = r'$\mu_o$H (T)'
p.ylabel = r'R (m$\Omega$)'





