# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 12:47:30 2014

@author: py07jtb
"""
import Stoner
import Stoner.Analysis as Analysis
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import splrep, splev


def G(x,a,b,c,d):
  return (a*np.exp(-1*((x-b)**2)/(2*c**2)))+d

d = Stoner.CSVFile("/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Images/SEM/SC004_2_T_.txt",header_line=1, data_line=2, data_delim='\t', header_delim='\t')
d = Analysis.AnalyseFile(d)

width = 40
sensitivity=5

t=d.peaks('y', 4, sensitivity , xcol='x', peaks=True, troughs=False, poly=4,  sort=False)

for i in t:
  r = d.search('x',lambda x,y: x>i-width and x<i+width)
  temp = Analysis.AnalyseFile()
  temp.data = r
  f = splrep(temp.column(0),temp.column(1),k=5,s=1000)
  x_new = np.arange(min(temp.column(0)),max(temp.column(0)),0.1)
  y_new = splev(x_new,f)
  
  temp2 = Analysis.AnalyseFile()
  temp2.add_column(x_new,column_header='x')  
  temp2.add_column(y_new,column_header='y')
  
  fit = temp2.curve_fit(G,'x','y',p0=[125,200,10,0],bounds=lambda x,y:x,result=True,header='Fit',asrow=False)
  print fit
  plt.plot(temp2.column(0),temp2.column(1),'k')
  plt.plot(temp.column(0),temp.column(1))
  #plt.plot(temp2.column(0),temp2.Fit,'r')

'''
f = splrep(d.x,d.y,k=4,s=10000)
plt.plot(t,splev(t,f),'or')

plt.plot(d.x,d.y)






x = np.arange(0,400,.1)
a = 125
b = 205
c = 10
d = 0

G = (a*np.exp(-1*((x-b)**2)/(2*c**2)))+d
plt.plot(x,G)
'''





'''
data = np.loadtxt("/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Images/SEM/SC004_2_T_.txt")

x,y = data[:,0], data[:,1]

f = splrep(x,y,k=4,s=10000)

plt.plot(x, y, label="noisy data")
plt.plot(x, splev(x,f), label="fitted")
plt.plot(x, splev(x,f,der=1)/10, label="1st derivative")
#plt.plot(x, splev(x,f,der=2)/100, label="2nd derivative")
plt.legend(loc=0)
plt.show()
'''