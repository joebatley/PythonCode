

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
          'axes.labelsize': 36,
          'text.fontsize': 36,
          'legend.fontsize': 24,
          'xtick.labelsize': 28,
          'ytick.labelsize': 28,
          'xtick.direction': 'in',
          'ytick.direction': 'in',
          'xtick.major.size':10,
          'ytick.major.size':10,
          'figure.figsize': fig_size,
         'font.family':'Arial',
         'xtick.major.pad':20,
         'ytick.major.pad':20,
         'font.size':32,
         'lines.linewidth':4}
 
plt.rcParams.update(params)


####### IMPORT DATA ######
def lin(x,m,c):
  return m*x+c

#file = Stoner.CSVFile(False,1,2,',',',')
file = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC019/DipProbe/SC019_9_A/20140623/6221-2182 DC IV/SC019_9_A_6221-2182 DC IV_Counter_0000 1.00_299.000000K_IV.txt') 
a=Analysis.AnalyseFile(file)
print a.column(1)
fit, fitVar= a.curve_fit(lin,1,0)

print fit,fitVar
error = numpy.sqrt(fitVar[0,0])
print error
t = 96e-9
w = 1130e-9
l = 30e-6

print fit[0]*t*w/l

alpha = 1e6
beta = 1

#plt.title(a['Sample ID'] + ' - ' + a['Notes'] + ' at ' + str.format("{0:.1f}",a['Sample Temp']) + ' K')
plt.xlabel(r'Current ($\mu$A)')
plt.ylabel(r'Voltage (V)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.plot(a.column('1'),a.column('0'),'-o',label = 'R = ' + str.format("{0:.2f}", fit[0]) + r'$\pm$' + str.format("{0:.2f}", error)+ r' $\Omega$')
plt.plot(a.column('1'),(fit[1]+(a.column('1')*fit[0])),'-r',label = 'Fit')
plt.legend(loc=2)
plt.tight_layout()
plt.show()



