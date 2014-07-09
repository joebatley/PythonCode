#from scipy import *

import Stoner.Analysis as Analysis
import pylab as plt
import numpy


fig_width_pt = 1000.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 42,
          #'axes.color_cycle':['b','r','k','g','p','c'],
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


### IMPORT DATA ###

a=Analysis.AnalyseFile(False)   #import a single data file ready to use the Analysis class
b=Analysis.AnalyseFile(False)



###arrange###
a.sort('Sample Temp')
b.sort('Sample Temp')

###interpolate###
#binter.data=b.interpolate(a.column('Sample Temp'),'linear',3)
aResnew = numpy.interp(b.column(3),a.column(3),a.column(2))
###calculation###

deltaR=aResnew-b.Resistance # soustraction
offset = b.Resistance+(deltaR/2)

#print (deltaR) 

#binter.add_column(deltaR,'DeltaR')

###Plot###
plt.title(r'')
plt.xlabel('Temperature (K)')
plt.ylabel(r'R$_s$ ($\mu$V/A)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.hold(True)
plt.plot(b.column(3),offset,'-or',label='Parallel')

c=Analysis.AnalyseFile(False)
plt.plot(c.column('Temp'),c.column('Res')-0.01,'-ob')

#plt.plot(b.column(3)**5,b.Resistance*1e6,'-ob',label='Antiparallel')

#plt.plot(b.column(3),deltaR*1e6,'ob')
#plt.plot(b.column(3),deltaR*1e6,'b')
#plt.legend()
plt.show()

