

import numpy
import Stoner.Analysis as Analysis
import pylab as plt
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
from Stoner.Folders import DataFolder

def lin(x,a):
  return x*a

####### IMPORT DATA ######
sample = 'SC021_2_A'


filedir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample.split('_')[0]+'/Transport/'+sample+'/6221-2182 DC IV/NLRvsHvsT/'
filename = '*_NLRvsH.txt'
folder = DataFolder(filedir, pattern = filename)

PRs = []
PRserr = []
APRs = []
APRserr =[]
DR = []
DRerr = []
Rmean = []
T = []

for f in folder:
  a=Analysis.AnalyseFile(f.clone)
  print a['Sample Temp']
  mean = (a.max('b')[0]+a.min('b')[0])/2
  
  P = a.mean('b',bounds = lambda x:x>mean)
  Perr = numpy.std(a.search('b',lambda x,y:x>mean,columns='b'))/numpy.sqrt(len(a.search('b',lambda x,y:x>mean,columns='b')))
  AP = a.mean('b',bounds = lambda x:x<mean)
  APerr = numpy.std(a.search('b',lambda x,y:x<mean,columns='b'))/numpy.sqrt(len(a.search('b',lambda x,y:x<mean,columns='b')))
  
  PRs.append(P)
  PRserr.append(Perr)
  APRs.append(AP)
  APRserr.append(APerr)
  DR.append(P-AP)
  DRerr.append(numpy.sqrt((Perr**2)+(APerr**2)))
  Rmean.append(mean)
  T.append(a['Sample Temp'])
  
alpha = 1e3
DeltaR = Analysis.AnalyseFile()
DeltaR['Sample ID'] = f['Sample ID']

# TEMPERATURE
DeltaR.add_column(T,'T (K)')

# PARALLEL Rs
DeltaR.add_column(PRs,r'$R_s(P)$ (V/A)')
DeltaR.mulitply(r'$R_s(P)$ (V/A)',alpha,header=r'$R_s(P)$ (mV/A)')
DeltaR.subtract(r'$R_s(P)$ (V/A)',numpy.array(Rmean),replace=False,header='Ptest')
# PARALLEL Rs ERROR
DeltaR.add_column(PRserr,'Perr')
DeltaR.mulitply('Perr',alpha,header='Perr mV')

# ANTIPARALLEL Rs
DeltaR.add_column(APRs,r'$R_s(AP)$ (V/A)')
DeltaR.mulitply(r'$R_s(AP)$ (V/A)',alpha,header=r'$R_s(AP)$ (mV/A)')
DeltaR.subtract(r'$R_s(AP)$ (V/A)',numpy.array(Rmean),replace=False,header='APtest')
# ANTIPARALLEL Rs ERROR
DeltaR.add_column(APRserr,'APerr')
DeltaR.mulitply('APerr',alpha,header='APerr mV')

# DELTA R
DeltaR.add_column(DR,r'$\Delta R_s$ (V/A)')
#DeltaR.add_column((DR/max(DR)),r'$\Delta R_s$ (V/A)')
DeltaR.mulitply(r'$\Delta R_s$ (V/A)',alpha,header=r'$\Delta R_s$ (mV/A)')
# ERROR IN DELTA R
DeltaR.add_column(DRerr,'DRerr')
DeltaR.mulitply('DRerr',alpha,header = 'DRerr mV')

# RS OFFSET
DeltaR.add_column(Rmean,r'$R_s$ offset (V/A)')
DeltaR.mulitply(r'$R_s$ offset (V/A)',alpha,header = r'$R_s$ offset (mV/A)')


DeltaR.sort('T (K)')

  


p=SP.PlotFile(DeltaR)
print p.column_headers
p.template=SPF.JTBPlotStyle
label = str(p['Sample ID'])
title = ' '
p.plot_xy('T (K)',r'$\Delta R_s$ (mV/A)',plotter=plt.errorbar,yerr='DRerr mV',label = label,title=title,figure=1)
p.plot_xy('T (K)',r'$R_s$ offset (mV/A)',label = label,title=title,figure=2)
p.plot_xy('T (K)',r'$R_s(P)$ (mV/A)',plotter=plt.errorbar,yerr='Perr mV',label = 'P',title=title,figure=3)
p.plot_xy('T (K)',r'$R_s(AP)$ (mV/A)',plotter=plt.errorbar,yerr='APerr mV',label = 'AP',title=title,figure=3)
p.plot_xy('T (K)','Ptest',label = 'P',title=title,figure=4)
p.plot_xy('T (K)','APtest',label = 'AP',title=title,figure=4)
#p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/'+sample.split('_')[0]+'/Transport/DeltaRvsT/' + str(p['Sample ID']) + 'DeltaRsvsT.txt')





