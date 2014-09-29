# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 09:47:07 2014

@author: py07jtb
"""

import numpy
import Stoner.Analysis as Analysis
import matplotlib.pyplot as plt # pylab imports numpy namespace as well, use pyplot in scripts
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP

def DR(L,P1,P2,Lam_FM1,Lam_FM2,rhoFM1,rhoFM2):
    
    
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> FETCH_HEAD
    Lambda_N = 300e-9
    Wpy1 = 180e-9
    Wpy2 = 140e-9
    Wcu = 220e-9
<<<<<<< HEAD
=======
    Tcu = 125e-9
    
    
    l = -1*L/Lambda_N
    
    rhoCu = 2e-8    
    
    Rf1 = (rhoFM1*Lam_FM1)/(Wpy1*Wcu)
    Rf2 = (rhoFM2*Lam_FM2)/(Wpy2*Wcu)
    Rn = (rhoCu*Lambda_N)/(Wcu*Tcu)
    
    x1 = (2.0*Rf1)/(1.0-(P1**2))
    x2 = (2.0*Rf2)/(1.0-(P2**2))
    x3 = 1.0/Rn
    
    denom = ((1.0+(x1*x3))*(1.0+(x2*x3)))-numpy.exp(2.0*l)   
    return P1*P2*x1*x2*x3*numpy.exp(l)/denom
    
def DR1(L,P1,P2,Lam_FM1,Lam_FM2,rhoFM1,rhoFM2):
    
    
    Lambda_N = 600e-9
    Wpy1 = 190e-9
    Wpy2 = 140e-9
    Wcu = 170e-9
=======
    Lambda_N = 600e-9
    Wpy1 = 150e-9
    Wpy2 = 150e-9
    Wcu = 150e-9
>>>>>>> FETCH_HEAD
>>>>>>> FETCH_HEAD
    Tcu = 125e-9
    
    
    l = -1*L/Lambda_N
    
    rhoCu = 2e-8    
    
    Rf1 = (rhoFM1*Lam_FM1)/(Wpy1*Wcu)
    Rf2 = (rhoFM2*Lam_FM2)/(Wpy2*Wcu)
    Rn = (rhoCu*Lambda_N)/(Wcu*Tcu)
    
    x1 = (2.0*Rf1)/(1.0-(P1**2))
    x2 = (2.0*Rf2)/(1.0-(P2**2))
    x3 = 1.0/Rn
    
    denom = ((1.0+(x1*x3))*(1.0+(x2*x3)))-numpy.exp(2.0*l)   
<<<<<<< HEAD
    return P1*P2*x1*x2*x3*numpy.exp(l)/denom    
=======
    return P1*P2*x1*x2*x3*numpy.exp(l)/denom
>>>>>>> FETCH_HEAD
    
def DR1(L,P1,P2,Lam_FM1,Lam_FM2,rhoFM1,rhoFM2):
    
    
    Lambda_N = 600e-9
    Wpy1 = 190e-9
    Wpy2 = 140e-9
    Wcu = 170e-9
    Tcu = 125e-9
    
    
    l = -1*L/Lambda_N
    
    rhoCu = 2e-8    
    
    Rf1 = (rhoFM1*Lam_FM1)/(Wpy1*Wcu)
    Rf2 = (rhoFM2*Lam_FM2)/(Wpy2*Wcu)
    Rn = (rhoCu*Lambda_N)/(Wcu*Tcu)
    
    x1 = (2.0*Rf1)/(1.0-(P1**2))
    x2 = (2.0*Rf2)/(1.0-(P2**2))
    x3 = 1.0/Rn
    
    denom = ((1.0+(x1*x3))*(1.0+(x2*x3)))-numpy.exp(2.0*l)   
    return P1*P2*x1*x2*x3*numpy.exp(l)/denom    
    
    
L = numpy.arange(200e-9,2e-6,10e-9)
    
p = SP.PlotFile()

p.add_column(L,'L (m)')
p.add_column(DR(L,0.45,0.45,5e-9,5e-9,20e-8,20e-8),'DR_PP')
<<<<<<< HEAD
p.add_column(DR1(L,0.45,0.45,5e-9,5e-9,20e-8,20e-8),'DR1_PP')
#p.add_column(DR(L,0.35,0.45,50e-9,5e-9,10e-8,30e-8),'DR_CP')
#p.add_column(DR(L,0.35,0.35,50e-9,50e-9,10e-8,10e-8),'DR_CC')
=======
<<<<<<< HEAD
p.add_column(DR1(L,0.45,0.45,5e-9,5e-9,20e-8,20e-8),'DR1_PP')
#p.add_column(DR(L,0.35,0.45,50e-9,5e-9,10e-8,30e-8),'DR_CP')
#p.add_column(DR(L,0.35,0.35,50e-9,50e-9,10e-8,10e-8),'DR_CC')
=======
p.add_column(DR(L,0.35,0.45,50e-9,5e-9,10e-8,30e-8),'DR_CP')
p.add_column(DR(L,0.35,0.35,50e-9,50e-9,10e-8,10e-8),'DR_CC')
>>>>>>> FETCH_HEAD
>>>>>>> FETCH_HEAD


p.figure()
p.template=SPF.JTBPlotStyle
p.plot_xy('L','DR_PP',label = 'Py-Py',linestyle='-',marker='')
<<<<<<< HEAD
p.plot_xy('L','DR1_PP',label = '1Py-Py',linestyle='-',marker='')
#p.plot_xy('L','DR_CP',label = 'Co-Py',linestyle='-',marker='')
#p.plot_xy('L','DR_CC',label = 'Co-Co',linestyle='-',marker='')
=======
<<<<<<< HEAD
p.plot_xy('L','DR1_PP',label = '1Py-Py',linestyle='-',marker='')
#p.plot_xy('L','DR_CP',label = 'Co-Py',linestyle='-',marker='')
#p.plot_xy('L','DR_CC',label = 'Co-Co',linestyle='-',marker='')
=======
p.plot_xy('L','DR_CP',label = 'Co-Py',linestyle='-',marker='')
p.plot_xy('L','DR_CC',label = 'Co-Co',linestyle='-',marker='')
>>>>>>> FETCH_HEAD
>>>>>>> FETCH_HEAD
p.ylabel = r'$\Delta R_s$ (V/A)'
