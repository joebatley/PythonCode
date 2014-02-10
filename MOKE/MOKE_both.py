"""

IMPORT MOKE FILES, AVERAGE THEM AND PLOT.

"""


import os
import sys
import numpy
import time
import matplotlib
import pylab as plt
import scipy

import Stoner
from Stoner.Folders import DataFolder


fig_width_pt = 700.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 42,
          'axes.color_cycle':['b','r','k','g','p','c'],
          'axes.formatter.limits' : [-7, 7],
          'text.fontsize': 36,
          'legend.fontsize': 24,
          'xtick.labelsize': 28,
          'ytick.labelsize': 28,
          'xtick.direction': 'in',
          'ytick.direction': 'in',
          'xtick.major.size':10,
          'ytick.major.size':10,
          'xtick.major.width':1,
          'ytick.major.width':1,
          'figure.figsize': fig_size,
         'font.family':'Arial',
         'xtick.major.pad':20,
         'ytick.major.pad':20,
         'font.size':32,
         'lines.linewidth':2,
         'lines.markersize':10,
         }
         
 
plt.rcParams.update(params)


####################  IPMORT DATA  ####################



filename = '/Volumes/stonerlab.leeds.ac.uk/data/Projects/Spincurrents/Joe Batley/Measurements/RN0128/MOKE/Jamie/RN0128_1/RN0128_1_20s_2000max_0.1set_repeat__1.txt'
workingpath = filename.rpartition('/')[0]
extension = '.' + filename.rpartition('/')[2].rpartition('.')[2]
os.chdir(workingpath)

list_of_files = [file for file in os.listdir(workingpath) if file.endswith(extension)]
print list_of_files
file_counter = 0

for file in list_of_files:  # read in: field (Oe), R (ohms)
  numData=numpy.genfromtxt(file, delimiter=',')
  print  'numData = ' + str(numData)
  Field = numData[:,0]
  KerrV = numData[:,1]

  print 'Field = ' + str(Field)
  ##  NORMALISE DATA  ##

  KerrNorm= KerrV - (((max(KerrV) - min(KerrV))/2) + min(KerrV))
  
  
  if file_counter == 0:
    AvgKerr = KerrNorm
  else:
    AvgKerr = AvgKerr + KerrNorm
  
  #print KerrV
  file_counter += 1


convert = 4 * numpy.pi * 80 * 1e-7
######################  PLOT DATA  ##########################


plt.title('')
plt.xlabel('B (T)')
plt.ylabel('Normalised Kerr Voltage')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.plot(Field*convert, -1*AvgKerr/max(AvgKerr),'ob')
plt.plot(Field*convert, -1*AvgKerr/max(AvgKerr))
matplotlib.pyplot.grid(False)
plt.show()









