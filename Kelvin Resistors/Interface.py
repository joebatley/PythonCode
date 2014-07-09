import re
import numpy
import Stoner
from Stoner.Folders import DataFolder
import pylab as plt

fig_width_pt = 1000.0 # Get this from LaTeX using \showthe\columnwidth
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


################ READ FILE INFO ########################



pattern = re.compile('_(?P<Width>\d*).0nm')
folder = DataFolder('/Users/py07jtb/Desktop/untitled folder/',pattern = pattern)


for f in folder:
    
    Area = float(f['Width'])**2 
    
    HighTempR = numpy.mean(f.search('temperature',lambda x,y: x>275 and x<285,'Resistance'))
    if HighTempR<0:
        HighTempR = -HighTempR
    HighTempRerr = numpy.std(f.search('temperature',lambda x,y: x>275 and x<285,'Resistance'))/len(f.search('temperature',lambda x,y: x>275 and x<285,'Resistance'))
    
    LowTempR = numpy.mean(f.search('temperature',lambda x,y: x>4 and x<15,'Resistance'))
    if LowTempR<0:
        LowTempR = -LowTempR
    LowTempRerr = numpy.std(f.search('temperature',lambda x,y: x>4 and x<15,'Resistance'))/len(f.search('temperature',lambda x,y: x>4 and x<15,'Resistance'))
    
    plt.title(r'Interface')
    plt.xlabel(r'Temperature (K)')
    plt.ylabel(r'R ')
    plt.ticklabel_format(style='plain', scilimits=(3 ,3))
    plt.hold(True)
    plt.plot(Area,HighTempR)
    #plt.errorbar(Area,HighTempR,HighTempRerr,ecolor='k',marker='o',mfc='red', mec='red')
    #plt.errorbar(Area,LowTempR,LowTempRerr,ecolor='k',marker='o',mfc='blue', mec='blue')
    #plt.legend()    
    plt.grid(False)
plt.show()





