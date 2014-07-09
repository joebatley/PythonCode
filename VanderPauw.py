
'''

Import two RvT data sets in different van der Pauw geometries and find the resistivity.

'''

import numpy
from scipy import interpolate
from scipy.interpolate import splrep, splev
from scipy.integrate import quad
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize
from lmfit import minimize, Parameters, Parameter, report_fit
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP



d = 1000e-10 #thickness

####### IMPORT DATA ######

dir = '/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_2A/20140611/6221-2182 DC IV'
file_A = '/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_2A/20140611/6221-2182 DC IV/SC018_2A_6221-2182 DC IV_Timed interval_0000 4.23_RvsT_A.txt'

file_B = '/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_2A/20140611/6221-2182 DC IV/SC018_2A_6221-2182 DC IV_Timed interval_0000 293.36_RvsT_B.txt'

a = Analysis.AnalyseFile(file_A)
b=Analysis.AnalyseFile(file_B)
a.del_rows(0)
b.del_rows(0)

######## CHECK ORDER #########

a.sort('temperature')
b.sort('temperature')
  
######### SPLINE #########
T = numpy.arange(5,280,1)  

X1 = a.column('temperature')
Y1 = a.column('Res')

X2 = b.column('temperature')
Y2 = b.column('Res')

yy1 = numpy.interp(X2,X1,Y1)

######## CALCULATE RESISTIVITY #########
def f(x,r1,r2):
  y = numpy.exp(-(numpy.pi*d*r1)/x) + numpy.exp(-(numpy.pi*d*r2)/x) -1
  return y

res = numpy.zeros(len(T))
R = numpy.zeros(len(T))

for i in range(len( res )):
  R[i] = yy1[i]/Y2[i]
  print R[i]
  res[i] = scipy.optimize.fsolve(f, 1e-8,args=(yy1[i],Y2[i]))
  print res[i]
   
rho = Analysis.AnalyseFile()
rho.add_column(X2,'T (K)')
rho.add_column(res,r'$\rho (\Omega)$m ')
print Y2


######### SAVE RESISTIVITY DATA #########
#rho.save(dir + a['Sample ID'] + '_res_vs_T.txt')
######### PLOT GRAPH #########

q=SP.PlotFile(rho.clone)              
q.template=SPF.JTBPlotStyle
title = None
label = ''
q.plot_xy('T (K)',r'$\rho (\Omega)$m ',label=label,figure=2,title=title)

