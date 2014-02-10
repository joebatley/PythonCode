
import numpy
import tkFileDialog
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.Plot as plot
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
def func(x):
  return numpy.mean(x)*1e6
def quad(x,a,b):
  return a*x*x+b


folder1 = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/HeatTransport/SpinInjectionIVs/', pattern = '*.txt') 
a=Analysis.AnalyseFile()

for f in folder1:
  a.add_column(f.Voltage,f.metadata['iterator'])
a.apply(func, 0, replace = False, header = 'NLVoltage (microV)')
a.add_column(folder1[1].column('Current'),'Current')
a.curve_fit(quad,'Current','NLVoltage (microV)',result=True, replace=False, header="parabolic")
#fit=a.polyfit(2,'Current','NLVoltage (microV)',bounds=lambda x,y:abs(x)>100e-6)
a.subtract('NLVoltage (microV)','parabolic',replace=False,header='minus background')

folder2 = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/HeatTransport/NoSpinInjectionIVs/IVs/', pattern = '*.txt') 
b=Analysis.AnalyseFile()

for d in folder2:
  b.add_column(d.Voltage,d.metadata['iterator'])
b.apply(func, 0, replace = False, header = 'NLVoltage (microV)')
b.add_column(folder2[1].column('Current'),'Current')
b.curve_fit(quad,'Current','NLVoltage (microV)',result=True, replace=False, header="parabolic")
b.subtract('NLVoltage (microV)','parabolic',replace=False,header='minus background')


print a.column_headers
print b.column_headers

plt.title(r'Interface')
plt.xlabel(r'Temperature (K)')
plt.ylabel(r'R ')
plt.ticklabel_format(style='plain', scilimits=(3 ,3))
plt.hold(True)
plt.plot(a.column('Current'),a.column('minus background'),'b',label = 'NSI')
plt.plot(b.column('Current'),b.column('minus background'),'r',label = 'RSI')
plt.legend()    
plt.grid(False)
plt.show()
