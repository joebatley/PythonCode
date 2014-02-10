

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
file = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_8_T/SC004_8_T_6221-2182 DC IV_Counter_0_295K_Py_Inj_300uA_.txt') 
a=Analysis.AnalyseFile(file)

fit, fitVar= a.curve_fit(lin,'Current','Voltage')

print fit
error = numpy.sqrt(fitVar[0,0])

alpha = 1e6
beta = 1

plt.title(a['Sample ID'] + ' - ' + a['Notes'] + ' at ' + str.format("{0:.1f}",a['Sample Temp']) + ' K')
plt.xlabel(r'Current ($\mu$A)')
plt.ylabel(r'Voltage (V)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.plot(alpha*a.column('Current'),beta*a.column('Voltage'),'-o',label = 'R = ' + str.format("{0:.2f}", fit[0]) + r'$\pm$' + str.format("{0:.2f}", error)+ r' $\Omega$')
plt.plot(alpha*a.column('Current'),beta*(fit[1]+(a.column('Current')*fit[0])),'-r',label = 'Fit')
plt.legend(loc=2)
plt.show()



