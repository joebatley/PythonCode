# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 15:29:55 2014

@author: py07jtb
"""
import numpy
import Stoner.Analysis as Analysis
import matplotlib.pyplot as plt # pylab imports numpy namespace as well, use pyplot in scripts
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP

def DR(P,Lam):
    
    L = 300e-9
    
    Wpy1 = 190e-9
    Wpy2 = 140e-9
    Wcu = 150e-9
    Tcu = 125e-9
    
    PyRes = 22e-8
    CuRes = 2.6e-8
    Lambda_F = 5e-9
    
    l = -1*L/Lambda_N
    Rf1 = (PyRes*Lambda_F)/(Wpy1*Wcu)
    Rf2 = (PyRes*Lambda_F)/(Wpy2*Wcu)
    Rn = (CuRes*Lambda_N)/(Wcu*Tcu)
    x1 = (2.0*Rf1)/(1.0-(P**2))
    x2 = (2.0*Rf2)/(1.0-(P**2))
    x3 = 1.0/Rn
    
    denom = ((1.0+(x1*x3))*(1.0+(x2*x3)))-numpy.exp(2.0*l)   
    return P*P*x1*x2*x3*numpy.exp(l)/denom

P = 0.4
Lambda_N = numpy.arange(0.,1e-6,10e-9)    
Y = DR(P,Lambda_N)    

p=SP.PlotFile()
p.figure(1)
p.add_column(Lambda_N,r'$\lambda_{Cu}$ (m)')
p.add_column(Y,r'$\Delta R_s$ (V/A)')
p.template=SPF.JTBPlotStyle
plt.subplot2grid((1,2),(0,0))
p.plot_xy(r'$\lambda_{Cu}$ (m)',r'$\Delta R_s$ (V/A)',linestyle='-',marker='')
plt.axhspan(1.35e-3, 1.62e-3, facecolor='g', alpha=0.5)


P = numpy.arange(0.,0.8,0.02)
Lambda_N = 350e-9
X = DR(P,Lambda_N) 

p=SP.PlotFile()
p.figure(1)
p.add_column(P,r'$\alpha$')
p.add_column(X,r'$\Delta R_s$ (V/A)')
p.template=SPF.JTBPlotStyle
plt.subplot2grid((1,2),(0,1))
p.plot_xy(r'$\alpha$',r'$\Delta R_s$ (V/A)',linestyle='-',marker='')
plt.axhspan(1.35e-3, 1.62e-3, facecolor='g', alpha=0.5)

plt.axvspan(0.54, 0.58, facecolor='g', alpha=0.5)
plt.tight_layout()





