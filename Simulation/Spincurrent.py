
import os
import sys
import numpy
import time
import pylab as plt
from scipy import *
import tkFileDialog
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis


Tcu = 100e-9
Wcu = 150e-9
resCu = 20.0e-8

Tpy = 20e-9
Wpy = 150e-9
resPY = 2.4e-7

P = 0.4

L = 300e-9

Lambda_N = 46e-9
Lambda_F = 5e-9

Rsn = (resCu*Lambda_N)/(Tcu*Wcu)
Rsf = (resPY*Lambda_F)/(Wpy*Wcu)

spinsig = (4*(P**2)*(Rsf**2)*(exp(-L/Lambda_N)))*(Rsn*((1-(P**2))**2)*(1-exp(-2*L/Lambda_N)))


Rf1 = (2*resPY*Lambda_F)/((1-(P*P))*Wpy*Wcu)
Rn1 = (2*resCu*Lambda_N)/(Wcu*Tcu)
model_Otani = ((P*P)*(Rf1*Rf1))/((2*Rf1*numpy.exp(L/Lambda_N))+(Rn1*numpy.sinh(L/Lambda_N)))
model_Cas = (2*(P*P)*(Rn1))/(((2+(Rn1/Rf1))**2*numpy.exp(L/Lambda_N))-((Rn1/Rf1)**2*numpy.exp(-L/Lambda_N)))



print model_Cas*300e-6