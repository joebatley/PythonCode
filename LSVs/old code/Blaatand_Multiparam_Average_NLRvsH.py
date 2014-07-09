
import numpy
import matplotlib
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import pylab as plt

 

fig_width_pt = 700.0 # Get this from LaTeX using \showthe\columnwidth
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

#filename = tkFileDialog.askopenfilename(message = 'Pick first file', title = 'Pick file ')
#workingpath = filename.rpartition('/')[0]
#print workingpath   
####### IMPORT DATA ######

folder = DataFolder('C:\Users\Jo\Documents\Joe\Measurments\RN0151\Transport\RN0151_4T\NLDCRvH_200uA_1.5K\untitled folder',pattern='*.txt') 
a=Analysis.AnalyseFile()
print folder

for f in folder:
  a.add_column(f.Resistance,str(f.metadata['multi[1]:iterator']))
  
print a.column_headers
a.apply(func, 1, replace = False, header = 'Rs (microOhms)')
a.add_column(folder[1].column('Control:Magnet Output'),'Field')

data = Analysis.AnalyseFile()
data.add_column(a.column('Field'),'Field')
data.add_column(a.column('Rs (microOhms)'),'Rs (microOhms)')

data.mask=lambda x:x[1]>115 or x[1]<25
#data.mask=lambda x:x[1]<25 

Ref = ((max(a.column('Rs'))-min(a.column('Rs')))/2)+min(a.column('Rs'))

P = a.mean('Rs',bounds = lambda x: x>Ref)
AP = a.mean('Rs',bounds = lambda x: x<Ref)
DeltaR = P-AP

print DeltaR

Perr = (numpy.std(a.search('Rs',lambda x,y:x>Ref,'Rs')))/numpy.sqrt(len(a.search('Rs',lambda x,y:x>Ref,'Rs'))) # error in average value for P state
APerr = (numpy.std(a.search('Rs',lambda x,y:x<Ref,'Rs')))/numpy.sqrt(len(a.search('Rs',lambda x,y:x<Ref,'Rs')))
DeltaRerr = numpy.sqrt((Perr*Perr)+(APerr*APerr)) #calculate error in Delta R in micro Ohms

print DeltaRerr


plt.title('')
plt.xlabel('B (T)')
plt.ylabel(r'R$_s$ ($\mu$V/A)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.plot(data.column('Field'),data.column('Rs (microOhms)'),'ob')
plt.plot(data.column('Field'),data.column('Rs (microOhms)'),'b')
matplotlib.pyplot.grid(False)
plt.show()



 


