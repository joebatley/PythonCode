# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 18:21:53 2014

@author: py07jtb
"""
import re
import numpy
from scipy import interpolate
import pylab as plt
from Stoner.Util import format_error
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize
from lmfit import minimize, Parameters, Parameter, report_fit
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP



Lambda_N = 1.5e-14/CuR(t)
print Lambda_N
P = 0.5
Pi=0.1
print P
LF = 5e-9
L = numpy.arange(300e-9,1.5e-6,10e-9)
Wpy = 150e-9
Wcu = 150e-9
Tcu = 130e-9
Lambda_F = LF*(PyR(10)/PyR(t))    
print Lambda_F
PyRes = PyR(t)
CuRes = CuR(t)


Rf = (PyRes*Lambda_F)/(Wpy*Wcu)
Rn = (CuRes*Lambda_N)/(Wcu*Tcu)  
Ri=1e-10 * Wpy*Wcu  
ri=Ri/((1-Pi**2)*Rn)
rf=Rf/((1-P**2)*Rn)
#model_tak = (2*P*P*Rf*Rf)/((1-(P*P))*(1-(P*P))*Rn*numpy.sinh((L/Lambda_N)))
#model_tak = (((2*Pi*ri+2*P*rf)**2)*numpy.exp(-L/Lambda_N))/((1+2*ri+2*rf)**2-numpy.exp(-2*L/Lambda_N))
model_tak = Rn*Pi*Pi*numpy.exp(-L/Lambda_N)

Rf1 = (2*PyRes*Lambda_F)/((1-(P*P))*Wpy*Wcu)
Rn1 = (2*CuRes*Lambda_N)/(Wcu*Tcu)
model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))


q=SP.PlotFile()
q.add_column(L*1e9,column_header='L (nm)')
q.add_column(model_tak*1e3,column_header=r'$\Delta \alpha$ (mV/A)')
print q.column_headers
q.setas="xy"
q.template=SPF.JTBPlotStyle
label = None
title = ' '
q.plot(label = label,title=title,figure=1)
