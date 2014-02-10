import Stoner as S
from Stoner.Folders import DataFolder
import pylab as plt
import numpy

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


def func(x):
  return numpy.mean(x)


folder = DataFolder(type=S.CSVFile('',0,',',','))
d = S.DataFile()

for f in folder:
    d.add_column(f.column(1))
    
d.apply(func, 1, replace = False, header = 'Mean NLVoltage')   
d.add_column(f.column(0), 'Field')

convert = 4 * numpy.pi *80 * 1e-7
    
plt.hold(True)
plt.title(r'Title')
plt.xlabel(r'Applied Field (Oe)')
plt.ylabel(r'Voltage (V)')
plt.grid(True)
plt.ticklabel_format(style='plain', scilimits=(3 ,3))
plt.plot(d.column('Field')*convert,d.column('Mean NLVoltage'),'ro')
plt.show()

  