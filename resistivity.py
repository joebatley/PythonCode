'''
import and average MR files from Serban's rig
'''

'''
Note:
debug in Pythonwin.exe
from command window open folder	to check and change directory use
	os.curdir    #retrieves current directory `.' for windows
	os.getcwd()  #retrieves current working directory
	PathName = 'y:\\Python\\NAP\\DWsensor'
	os.chdir(PathName)  #change directory
then to run use:
	execfile('DWsensor.py')
	#import DWsensor.py
runs better from pylab or other environments
'''

import os
import sys
import numpy
import time
import matplotlib
#matplotlib.use('Agg')
import pylab as plt
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
from scipy import *
from scipy.interpolate import interp1d
import tkFileDialog
import Stoner

################ READ FILE INFO ########################

d = 105e-10 #thickness
f = 0.59 #fudgefactor


filename1 = tkFileDialog.askopenfilename(message = 'Pick file', title =  'Curve one')
workingpath1 = filename1.rpartition('/')[0]
extension1 = '.' + filename1.rpartition('/')[2].rpartition('.')[2]
os.chdir(workingpath1)
data1 = Stoner.DataFile(filename1)

filename2 = tkFileDialog.askopenfilename(message = 'Pick file', title = 'Curve one') 
workingpath2 = filename2.rpartition('/')[0]
extension2 = '.' + filename2.rpartition('/')[2].rpartition('.')[2]
os.chdir(workingpath2)
data2 = Stoner.DataFile(filename2)

savename = filename1.rpartition('/')[2]

print savename
####### IMPORT DATA ######

#plt.plot(data1[1:,0],data1[1:,1],data2[1:,0],data2[1:,1])
#plt.show()

X1 = data1.column('temperature')
Y1 = data1.column('Resistance')


size1 = size(X1)
if X1[0]>X1[size1-1]:
  X1 = X1[::-1]
  Y1 = Y1[::-1]  


  X2 = data2.column('temperature')
Y2 = data2.column('Resistance')


size2 = size(X2)
if X2[0]>X2[size2-1]:
  X2 = X2[::-1]
  Y2 = Y2[::-1]
  


"""
x1min = min(X1)
x2min = min(X2)

if x1min > x2min:
  xmin = 0.5 + min(X1)
else:
  xmin = 0.5 + min(X2)
  print xmin

x1max = max(X1)
x2max = max(X2)

if x1max<x2max:
  xmax = max(X1) - 0.5
else:
  xmax = max(X2) - 0.5
  print xmax
"""
#spline_fit_1 = interp1d(X1,Y1,bounds_error=False)


#spline_fit_2 = interp1d(X2,Y2,bounds_error=False)
#xx = numpy.arange(xmin , xmax , (xmax-xmin)/200)


#yy1 = spline_fit_1(X2)
#yy2 = spline_fit_2(xx) 
#print yy2
yy1 = numpy.interp(X2,X1,Y1)
print yy1
print Y1
print Y2

res = (pi*d*(yy1+Y2)*f)/(2*log(2))

print res

File = open( savename[:8] +'_res.txt', 'wb') # will create a new file if does not exist, 'a' to append 'w' to write
File.write('Resistivity' + '\t' + 'Temp' + chr(13)+ chr(10))

for pp in range(0, size(X2)):
    File.write(str(res[pp])  + '\t' + str(X2[pp]) + chr(13)+ chr(10))
File.close()


plt.title('Resistivity vs T')
plt.xlabel('Temperature (K)')
plt.ylabel('Resistivity (Ohm m)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.plot(X2,res)
matplotlib.pyplot.grid(True)
plt.show()





#I[0:size/2],V[0:size/2],'b',I[size/2:size],V[size/2:size],'r'


#+ filename.rpartition('/')[2]
  
  

