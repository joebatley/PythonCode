
import numpy
import tkFileDialog
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.Plot as plot


################ READ FILE INFO ########################
def func(x):
  return numpy.mean(x)

#filename = tkFileDialog.askopenfilename(message = 'Pick first file', title = 'Pick file ')
#workingpath = filename.rpartition('/')[0]
#print workingpath   
####### IMPORT DATA ######

folder = DataFolder('/Users/Joe/PhD/Measurements/RN0151_4T/HeatTransport/NoSpinInjectionIVs/RvsH', pattern = '*.txt') 
a=Analysis.AnalyseFile()

for f in folder:
  a.add_column(f.Resistance,f.metadata['multi[1]:iterator'])


a.apply(func, 5, replace = False, header = 'Avg')
a.add_column(folder[1].column('Control:Magnet Output'),'Field')
p=plot.PlotFile(a)
p.plot_xy('Field','Avg')

 


