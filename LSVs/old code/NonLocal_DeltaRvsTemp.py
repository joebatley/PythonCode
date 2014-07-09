
import numpy
import tkFileDialog
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.Plot as plot


################ READ FILE INFO ########################
def func(x):
  return numpy.mean(x)*1e6

#filename = tkFileDialog.askopenfilename(message = 'Pick first file', title = 'Pick file ')
#workingpath = filename.rpartition('/')[0]
  
####### IMPORT DATA ######

folder = DataFolder('/Users/Joe/PhD/Measurements/RN0151_4T/NLIVvH/FieldSweep', pattern = '*.txt') 
print folder
Field=numpy.zeros(len(folder))
offset=numpy.zeros(len(folder))
linear=numpy.zeros(len(folder))
quad=numpy.zeros(len(folder))

for f in folder:
  b=Analysis.AnalyseFile(f)
  fit = b.polyfit('Current','Voltage',2,bounds=lambda x, y:abs(x)>150e-6)

  offset[f.metadata['iterator']-2] = fit[2]
  linear[f.metadata['iterator']-2] = fit[1]
  quad[f.metadata['iterator']-2] = fit[0]  
  Field[f.metadata['iterator']-2] = f.metadata['Control:Magnet Output']

d=Stoner.DataFile()
d.add_column(Field,'Field')
d.add_column(linear*1e6,'NL Voltage Linear Fit')
d.add_column(quad,'NL Voltage quad Fit')
print d
p=plot.PlotFile(d)
p.plot_xy('Field','NL Voltage quad Fit',title='Quad Fit to NL IV vs Field at 1.5K',save_filename='Quad Fit to NL IV vs Field at 1_5K')

#plt.title('Detector DC AMR 50uA, 3 probe')
#plt.xlabel('Field (B)')
#plt.ylabel('Resistance (Ohms)')
#plt.ticklabel_format(style = 'sci', useOffset = False)
#plt.tick_params(axis='both', which='minor')
#plt.plot(Field, linear)
#plt.show()
 


