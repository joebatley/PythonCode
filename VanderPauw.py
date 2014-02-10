
<<<<<<< HEAD

import numpy
import matplotlib
=======
'''

Import two RvT data sets in different van der Pauw geometries and find the resistivity.

'''



import numpy
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e
import pylab as plt
from scipy.interpolate import interp1d
import scipy.optimize
import Stoner
from pylab import arange,pi,sin,cos,sqrt
 
fig_width_pt = 1000.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 36,
          'text.fontsize': 36,
          'legend.fontsize': 24,
          'xtick.labelsize': 28,
          'ytick.labelsize': 28,
          'xtick.direction': 'out',
          'ytick.direction': 'out',
          'figure.figsize': fig_size,
         'font.family':'Arial',
         'xtick.major.pad':20,
         'ytick.major.pad':20,
         'font.size':32,
         'lines.linewidth':4}
 
plt.rcParams.update(params)


d = 223e-10 #thickness

####### IMPORT DATA ######
data1 = Stoner.DataFile(False)
data2 = Stoner.DataFile(False)

<<<<<<< HEAD

data1 = Stoner.DataFile(False)

data2 = Stoner.DataFile(False)


####### IMPORT DATA ######
=======

####### SET COLUMNS ######

X1 = data1.column('Temperature')
Y1 = data1.column('Resistance')
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e

X2 = data2.column('Temperature')
Y2 = data2.column('Resistance')

<<<<<<< HEAD
X1 = data1.column('Temperature')
Y1 = data1.column('Resistance')
=======
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e

######## CHECK ORDER #########
size1 = numpy.size(X1)
if X1[0]>X1[size1-1]:
  X1 = X1[::-1]
  Y1 = Y1[::-1]  

<<<<<<< HEAD

X2 = data2.column('Temperature')
Y2 = data2.column('Resistance')


size2 = numpy.size(X2)
=======
size2 = size(X2)
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e
if X2[0]>X2[size2-1]:
  X2 = X2[::-1]
  Y2 = Y2[::-1]
  
  
######### SPLINE #########
yy1 = numpy.interp(X2,X1,Y1)


######## CALCULATE RESISTIVITY #########
def f(x,r1,r2):
  y = numpy.exp(-(numpy.pi*d*r1)/x) + numpy.exp(-(numpy.pi*d*r2)/x) -1
  return y

res = numpy.zeros(numpy.size(yy1))
R = numpy.zeros(numpy.size(yy1))

for i in range(0,numpy.size( res )):
  R[i] = yy1[i]/Y2[i]
  res[i] = scipy.optimize.fsolve(f, 1e-8,args=(yy1[i],Y2[i]))
   

<<<<<<< HEAD
=======

######### SAVE RESISTIVITY DATA #########
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e
'''
File = open( savename[:8] +'_res1.txt', 'wb') # will create a new file if does not exist, 'a' to append 'w' to write
File.write('Resistivity' + '\t' + 'Temp' + chr(13)+ chr(10))

for pp in range(0, size(X2)):
    File.write(str(res[pp])  + '\t' + str(X2[pp]) + chr(13)+ chr(10))
File.close()
'''
<<<<<<< HEAD
=======

######### PLOT GRAPH #########
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e

plt.title('Resistivity vs T')
plt.xlabel('Temperature (K)')
plt.ylabel('Resistivity ($\mu$Ohm cm)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
<<<<<<< HEAD
plt.plot(X2,res*1e8)
matplotlib.pyplot.grid(True)
=======
plt.hold(True)
#plt.plot(X1,Y1)
#plt.plot(X2,Y2)
plt.plot(X2,res)
plt.grid(True)
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e
plt.show()



<<<<<<< HEAD
=======

  

>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e
