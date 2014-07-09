#from scipy import *
from scipy import interpolate
import Stoner.Analysis as Analysis
import pylab as plt
import numpy
import Stoner

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

a=Analysis.AnalyseFile('/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SPH033_5/20140607/6221-2182 DC IV/SPH033_5_6221-2182 DC IV_Timed interval_0000 0.00_20uA_RvT_alpha_0_1T.txt')   #import a single data file ready to use the Analysis class


###arrange###
a.sort('Sample Temp')
a.del_rows('m',lambda x,y: x>34000)

fit_a = a.polyfit('Sample Temp','m',5)
curve_a = fit_a[0]*a.column('Sample Temp')**5 + fit_a[1]*a.column('Sample Temp')**4 + fit_a[2]*a.column('Sample Temp')**3 + fit_a[3]*a.column('Sample Temp')**2 +fit_a[4]*a.column('Sample Temp') + fit_a[5]



bin=10

sdev_a = numpy.zeros(len(a.column('m'))/bin) 
Res_a = numpy.zeros(len(a.column('m'))/bin)
Temp_a = numpy.zeros(len(a.column('m'))/bin)

for i in range(0,len(a.column('m')),bin):
    if i<(len(a.column('m'))/bin)*bin:
        tot = 0.0
        for j in range(0,bin):
            tot = tot + a.column('m')[i+j]
        Res_a[i/bin] = tot/bin   
        Temp_a[i/bin] = ((a.column('Sample Temp')[i]-a.column('Sample Temp')[i+bin-1])/2)+a.column('Sample Temp')[i+bin-1]
        sdev=0
        for p in range(0,bin):
            sdev = sdev + (a.column('m')[i+j]-Res_a[i/bin])**2
        sdev_a[i/bin] = numpy.sqrt(sdev)/bin        
        
                     
                     

###Plot###
plt.title(r'R vs T with 1 T parallel to current')
plt.xlabel('Temperature (K)')
plt.ylabel(r'R ($\Omega$)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.hold(True)
#plt.plot(a.column('Temp'),1e6*a.column('Res'),'-or',label='Parallel')
#plt.plot(a.column('Temp'),1e6*curve_a,'-k',label='Parallel Fit')
#plt.plot(Temp_b,1e6*aResnew,'-or',label='Parallel')
#plt.plot(b.column('Temp'),1e6*b.column('Res'),'-ob',label='Antiparallel')
#plt.plot(b.column('Temp'),1e6*curve_b,'-k',label='Antiparallel Fit')
#plt.plot(Temp_b,1e6*Res_b,'-ob',label='Antiparallel')
#plt.errorbar(Temp_b,deltaR,DRerr,ecolor='k',marker='o',mfc='blue', mec='blue')
plt.plot(Temp_a,Res_a,'-ob')
plt.tight_layout()
#plt.legend(loc=2)
plt.show()

