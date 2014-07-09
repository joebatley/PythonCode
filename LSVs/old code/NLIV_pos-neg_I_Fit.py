# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 17:06:29 2014

@author: py07jtb
"""

import re
import numpy
from scipy import interpolate
from scipy.interpolate import splrep, splev
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize

import Stoner.PlotFormats as SPF
import Stoner.Plot as SP

def poly4(x,a,b,c,d,e):
  return a*x**4 + b*x**3 + c*x**2 + d*x + e 
def quad(x,a,b,c):
  return a*x*x+b*x+c
  
def lin(x,m,c):
  return m*x+c


AP = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/NLIV_FITTING/SC004_3_T_NLIVat254K/SC004_3_T_254K_NLIV_AP.txt')
P = Analysis.AnalyseFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/NLIV_FITTING/SC004_3_T_NLIVat254K/SC004_3_T_254K_NLIV_P.txt')


both = Analysis.AnalyseFile()
both.add_column(P.I,column_header='I (A)')

both.add_column(P.V,column_header=r'V$_P$')
both.add_column(AP.V,column_header=r'V$_{AP}$')
both.subtract(r'V$_P$',r'V$_{AP}$',header=r'$\Delta$V')
both.curve_fit(lin,'I',r'$\Delta$V',result=True,header=r'$\Delta$Vfit')
both.subtract(r'$\Delta$V',r'$\Delta$Vfit',header=r'$\Delta$V-Linear')
both.sort('I')
both=SP.PlotFile(both)                #PLOT
both.template=SPF.JTBPlotStyle
title = None
both.plot_xy('I',r'$\Delta$V',label=None,figure=1,title=title)
both.plot_xy('I',[r'V$_P$',r'V$_{AP}$'],label='AP',figure=2,title=title)
both.plot_xy('I',r'$\Delta$V-Linear',label=None,figure=3,title=title)




########## FULL IV FIT ###################

''' Fit to both posative and negative current at the same tim then subtract quadratic term '''
'''

# ANTIPARALLEL

fitAP = AP.curve_fit(quad,'I','V',asrow=True)                 #Fit quadratic to the raw NLIV
AP.subtract('V',fitAP[0]*AP.I*AP.I,header='Linear')           #Subtract the I squared part
AP.curve_fit(lin,'I','Linear',result=True,header='Lin Fit')   #Fit linear to the remaining part
AP.subtract('Linear','Lin Fit',header='remainder')            #subtract fit from linear
AP.sort('I')
APinterp = splrep(AP.column('I'),AP.column('V'),k=5,s=3)      #Interpolate NL IV and smooth
AP.add_column(splev(AP.column('I'),APinterp),column_header='spline')  #Splin the data and add to DataFile
APderiv = splev(AP.column('I'),APinterp,der=2)                        #Calculate the derivative
AP.add_column(APderiv,column_header=r'$\frac{d^2V}{dI^2}$')           #Add derivative to DataFile
dvfit = AP.curve_fit(quad,'I',r'$\frac{d^2V}{dI^2}$',result=True,header='dVfit',asrow=True)

ap=SP.PlotFile(AP)                #PLOT
#ap.setas=".......x.y"
ap.template=SPF.JTBPlotStyle
title = None
ap.plot_xy('I','remainder',label='AP',figure=2,title=title)


# PARALLEL

fitP = P.curve_fit(poly4,'I','V',asrow=True)
print fitP
P.subtract('V',fitP[0]*P.I*P.I,header='Linear')
P.curve_fit(lin,'I','Linear',result=True,header='Lin Fit')
P.subtract('Linear','Lin Fit',header='remainder')
P.sort('I')
Pinterp = splrep(P.column('I'),P.column('V'),k=5,s=3)
P.add_column(splev(P.column('I'),Pinterp),column_header='spline')
Pderiv = splev(P.column('I'),Pinterp,der=2)
P.add_column(Pderiv,column_header=r'$\frac{d^2V}{dI^2}$')
dvfitP = P.curve_fit(quad,'I',r'$\frac{d^2V}{dI^2}$',result=True,header='dVfit',asrow=True)
print dvfitP
p=SP.PlotFile(P)                  #PLOT
#p.setas="y............x"
p.template=SPF.JTBPlotStyle
title = None
p.plot_xy('I',r'$\frac{d^2V}{dI^2}$',label='P',figure=2,title=title)

'''


############## FIT POS/NEG CURRENT ##############
''' Fit posative and negative currents in the NL IV seperately '''

'''


APpos = AP.curve_fit(quad,'I','V',bounds=lambda x,y:x<0,asrow=True,result=True,header='posfit')
APneg = AP.curve_fit(quad,'I','V',bounds=lambda x,y:x>0,asrow=True,result=True,header='negfit')
fit = AP.curve_fit(quad,'I','V',bounds=lambda x,y:x,asrow=True,result=True,header='fit')
AP.subtract('V','fit',header='V-fit')
print APpos
print ''
print APneg
print ''
print fit
print ''
AP.sort('I')
plot=SP.PlotFile(AP)
print plot.column_headers
plot.template=SPF.JTBPlotStyle
title = None
plot.plot_xy('I','fit',label=None,figure=2,title=title)


pos = AP.search('I',lambda x,y:x<0,['I','V'])
POS = Analysis.AnalyseFile()
POS.data = pos
POS.column_headers = ['I','V']
POSfit=POS.curve_fit(quad,'I','V',bounds=lambda x,y:x,asrow=True,result=True,header='fit')
POS.subtract('V','fit',header='V-fit')
print POS
#POS.sort('I')


neg = AP.search('I',lambda x,y:x>0,['I','V'])
NEG = Analysis.AnalyseFile()
NEG.data = neg
NEG.column_headers = ['I','V']
NEGfit=NEG.curve_fit(quad,'I','V',bounds=lambda x,y:x,asrow=True,result=True,header='fit')
NEG.subtract('V','fit',header='V-fit')
#NEG.sort('I')


print APpos
print POSfit
print ''
print APneg
print NEGfit
print ''


ap=SP.PlotFile(POS)
print ap.column_headers
ap.template=SPF.JTBPlotStyle
title = None
ap.plot_xy('I','fit',label=None,figure=2,title=title)

apn=SP.PlotFile(NEG)
print apn.column_headers
apn.template=SPF.JTBPlotStyle
title = None
apn.plot_xy('I','fit',label=None,figure=2,title=title)

'''