

import numpy
import Stoner
import Stoner.Analysis as Analysis
import pylab as plt

 

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


####### IMPORT DATA ######



a = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/James Witt/Blatand/Noise standard 19_9_12/6221-Lockinnew stick new head R vs freq.txt') 
b = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/James Witt/Blatand/Noise standard 19_9_12/6221-Lockinnew stick new head R vs freq(2).txt')
c = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/James Witt/Blatand/Noise standard 19_9_12/6221-Lockinnew stick new head R vs freq(3).txt')
a.mask = lambda x: x[0]<10
c.mask = lambda x: x[0]>1e4


plt.title('')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Lock-in Signal (V)')
#plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.hold(True)
plt.loglog(a.column(0),a.column(3),'-ob')
plt.loglog(b.column(0),b.column(3),'-ob')
plt.loglog(c.column(0),c.column(3),'-ob')
plt.show()



