

import numpy
from Stoner.Folders import DataFolder
import pylab as plt

 

fig_width_pt = 1000.0 # Get this from LaTeX using \showthe\columnwidth
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


Seperation = {1:325e-9,
              'SC004_2_T':450e-9,
              'SC004_3_T':570e-9,
              'SC004_4_T':690e-9,
              'SC004_5_B':742e-9,
              'SC004_6_T':954e-9,
              'SC004_7_B':1182e-9,
              'SC004_8_T':1378e-9,
              'SC004_9':1525e-9,}

####### IMPORT DATA ######



folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Cu spacer resistance',pattern = '*.txt')

for f in folder:
    
    f.del_rows(0)
    f.del_rows('Temp',lambda x,y:x<1)
    res = (150e-9*130e-9*f.column('Resistance'))/Seperation[f['Sample ID']]
    f.add_column(res,column_header ='Resistivity')
    #f.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Cu spacer resistance/Resistivity/'+a['Sample ID']+'_Cu_resistivity_vs_T.txt')
    
    plt.title('Cu bar resistivity',verticalalignment='bottom')
    plt.xlabel('T (K)')
    plt.ylabel(r'R ($\Omega$ m)')
    plt.ticklabel_format(style = 'sci', useOffset = False)
    plt.tick_params(axis='both', which='minor')
    
    plt.plot(f.column('Temp'),f.column('Resistivity'),'-',label = f['Sample ID'])

plt.tight_layout()
plt.legend().draggable()   
plt.show()



