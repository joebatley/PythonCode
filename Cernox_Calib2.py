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

filename1 = tkFileDialog.askopenfilename(message = 'Pick file', title =  'Curve one') 
workingpath1 = filename1.rpartition('/')[0]
extension1 = '.' + filename1.rpartition('/')[2].rpartition('.')[2]
os.chdir(workingpath1)
#print(filename1, workingpath1, extension1)
data1 = Stoner.DataFile(filename1)
#print(data1.column_headers)
  
filename2 = tkFileDialog.askopenfilename(message = 'Pick file', title = 'Curve two') 
workingpath2 = filename2.rpartition('/')[0]
extension2 = '.' + filename2.rpartition('/')[2].rpartition('.')[2]
os.chdir(workingpath2)
#print(filename2, workingpath2, extension2)
data2 = Stoner.DataFile(filename2)
#print(data2.column_headers)
  
####### IMPORT DATA ######

spline_temp_data = tkFileDialog.askopenfilename(message = 'Pick file', title = 'calib values')
LSTemp = genfromtxt(spline_temp_data)
xx = LSTemp[:,2]
#print size(xx)
#print LSTemp

####### IMPORT DATA 1 ######
X1 = data1.column('CX1050AA_Temp')
Y1 = data1.column('CX1050SD_Sensor')
######## CHECK ORDER #########
size1 = size(X1)
if X1[0]>X1[size1-1]:
  X1 = X1[::-1]
  Y1 = Y1[::-1]
######### SPLINE 1 #########
spline_fit_1 = interp1d(X1,Y1,kind=1,bounds_error=False)
yy1 = spline_fit_1(xx)
#print yy1


####### IMPORT DATA 2 ######
X2 = data2.column('CX1050AA_Temp')
Y2 = data2.column('CX1050SD_Sensor')
######## CHECK ORDER #########
size2 = size(X2)
if X2[0]>X2[size2-1]:
  X2 = X2[::-1]
  Y2 = Y2[::-1]
######### SPLINE 2 #########
spline_fit_2 = interp1d(X2,Y2,kind=1,bounds_error=False)
yy2 = spline_fit_2(xx)
#print yy2




data = numpy.zeros([size(xx),2])
data[:,0] = xx
data[:,1] = ((yy1+yy2)/2)

fit = numpy.polyfit(data[-4:,0],data[-4:,1],1)
fitx = numpy.arange(0,5,0.1)
fity = fit[1] + fitx*fit[0]

calib = numpy.zeros([size(xx)+3,2])
for i in range(0,len(xx)+3):
  if i<len(xx):
    calib[i,0]=data[i,0]
    calib[i,1]=data[i,1]
  else:
    calib[i,0]=calib[i-1,0]-0.1
    calib[i,1]=fit[1]+fit[0]*calib[i,0]
  
print fitx,fity,fit

######### WRITE TO FILE #########

File = open('X8446.dat', 'wb') # will create a new file if does not exist, 'a' to append 'w' to write
File.write('Sensor Model:   CX-1070-SD-HT' + chr(13)+ chr(10)+ 'Serial Number:  X8446' + chr(13)+ chr(10)+ 'Data Format:    4      (Log Ohms/Kelvin)' + chr(13)+ chr(10)+ 'SetPoint Limit: 302.5     (Kelvin)' + chr(13)+ chr(10)+ 'Temperature coefficient:  1 (Negative)' + chr(13)+ chr(10)+ 'Number of Breakpoints:   145' + chr(13)+ chr(10) + chr(13)+ chr(10) + 'No.   Units      Temperature (K)' + chr(13) + chr(10) + chr(13)+ chr(10) + chr(13)+ chr(10))

for pp in range(0, size(xx)+3):
    File.write(str(pp+1)  + '\t' + str.format("{0:.5f}",log10(calib[pp,1])) + '\t'+ str.format("{0:.1f}",calib[pp,0]) + chr(13)+ chr(10))
File.close()


plt.title('R vs T of X84446 Cernox')
plt.xlabel('Temperature (K)')
plt.ylabel('Log Resistance (Ohms)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.plot(xx,data[:,1],'gx',fitx,fity,calib[:,0],calib[:,1])
matplotlib.pyplot.grid(True)
plt.show()





#I[0:size/2],V[0:size/2],'b',I[size/2:size],V[size/2:size],'r'


#+ filename.rpartition('/')[2]
  
  

