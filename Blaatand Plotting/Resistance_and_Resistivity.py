

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


#file = Stoner.CSVFile(False,1,2,',',',')
file = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_2_T/SC004_2_T_6221-2182 DC IV_Timed interval_RvT_CuSpacer_100uA_.txt') 
a=Analysis.AnalyseFile(file)
print a.column_headers
a.del_rows(0)


X = a.column('Temp')
Y1 = a.column('Resistance')
Y2 = (Y1*150e-9*130e-9/425e-9)*1e8

# Plot Lambda and alpha
fig, ax1 = plt.subplots()
ax1.set_xlabel('Temperature (K)',labelpad=15)
plt.hold(True)

ax1.plot(X,Y1,'-ok')
ax1.set_ylabel('R ($\Omega$)', color='k',labelpad=15)
for tl in ax1.get_yticklabels():
    tl.set_color('k')
  

ax2 = ax1.twinx()
ax2.plot(X,Y2,'-or')
ax2.set_ylabel(r'$\rho$ ($\mu \Omega$ cm)', color='r',labelpad=15)
for t2 in ax2.get_yticklabels():
    t2.set_color('r')
  
plt.tight_layout(pad=0.1, w_pad=0.0, h_pad=0.0)
#plt.legend(loc = 'upper right')
plt.show()





