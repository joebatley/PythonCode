
import numpy
import tkFileDialog
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.Plot as plot


################ READ FILE INFO ########################
def func(x):
  return numpy.mean(x)*1e6
def quad(x,a,b):
  return a*x*x+b


folder1 = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/HeatTransport/NoSpinInjectionIVs/IVs', pattern = '*.txt') 
a=Analysis.AnalyseFile()

for f in folder1:
  a.add_column(f.Voltage,f.metadata['iterator'])
a.apply(func, 0, replace = False, header = 'NLVoltage (microV)')
a.add_column(folder1[1].column('Current'),'Current')
#a.curve_fit(quad,'Current','NLVoltage (microV)',result=True, replace=False, header="parabolic")
fit=a.polyfit('Current','NLVoltage (microV)',2,bounds=lambda x,y:abs(x)>100e-6)
a.add_column(a.column('Current')*fit[1],'Linear Fit')
#a.subtract('NLVoltage (microV)','parabolic',replace=False,header='minus background')

folder2 = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/HeatTransport/SpinInjectionIVs', pattern = '*.txt') 
b=Analysis.AnalyseFile()

for d in folder2:
  b.add_column(d.Voltage,d.metadata['iterator'])
b.apply(func, 0, replace = False, header = 'NLVoltage (microV)')
b.add_column(folder2[1].column('Current'),'Current')
#b.curve_fit(quad,'Current','NLVoltage (microV)',result=True, replace=False, header="parabolic")
#b.subtract('NLVoltage (microV)','parabolic',replace=False,header='minus background')
fit=b.polyfit('Current','NLVoltage (microV)',2,bounds=lambda x,y:abs(x)>100e-6)
b.add_column(a.column('Current')*fit[1],'Linear Fit')


p1=plot.PlotFile(a)
p1.plot_xy('Current','Linear Fit','b-',title='Nonlocal Voltage vs Current')

p2=plot.PlotFile(b)
p2.plot_xy('Current','Linear Fit','k--',title='Nonlocal Voltage vs Current',figure=p1.fig,save_filename='Nonlocal Voltage vs Current - Just Linear component') 


