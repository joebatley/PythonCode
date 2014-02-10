import re
import numpy
import pylab as plt
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis


fig_width_pt = 1000.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 42,
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
         'lines.markersize':15,
         }
 
plt.rcParams.update(params)


################ READ FILE INFO ########################
def func(x):
  return numpy.mean(x)

def quad(x,a,b,c):
  return a*x*x+b*x+c

def IV_group_Avg(folder,keys):
  #folder[0].metadata['VTI-ITC']=1.0
  avg = Analysis.AnalyseFile(folder[0])
  avg.del_column('Voltage')
  avg.del_column('Current')
  avg.del_column('Column 2')
  for f in folder:
    avg.add_column(f.Voltage,str(f.metadata['iterator']))
  avg.apply(func, 1, replace = False, header = 'Mean NLVoltage')
  avg.add_column(folder[1].column('Current'),'Current')
  return avg


def P_AP(folder,keys):
  
  for f in folder:
    
    
    a=Analysis.AnalyseFile()
    a.add_column(f.column('Current'),'Current')
    a.add_column(f.column('Mean'),'NLV')
    
    fit, fitVar= a.curve_fit(quad,'Current','NLV',bounds=lambda x,y:abs(x)>200e-6,result=True,header='Fit') 
    
    plt.title(r'')
    plt.xlabel(r'Temperature (K)')
    plt.ylabel(r'$\beta$ (V/A$^2$)')
    plt.ticklabel_format(style='plain', scilimits=(3 ,3))
    plt.hold(True)
    
    '''
    if f['IVtemp'] == 5:
      plt.plot(a.column('Current'),a.column('NLV'),'b')
      plt.plot(a.column('Current'),a.column('Fit'),'k')
      
    '''
    print f['state'],f['IVtemp']
    
    if f['state'] == 'P':
      #plt.plot(f['IVtemp'],fit[0],'ro')
      print fitVar
      plt.errorbar(f['IVtemp'],fit[0],numpy.sqrt(fitVar[0,0]),ecolor='k',marker='o',mfc='red', mec='k',ms=15.0)
      print 'p'
    if f['state'] == 'AP':
      print 'ap'
      plt.errorbar(f['IVtemp'],fit[0],numpy.sqrt(fitVar[0,0]),ecolor='k',marker='o',mfc='blue', mec='k',ms=15.0)
      #plt.plot(f['IVtemp'],fit[0],'bx')
  #plt.legend()
  plt.savefig('/Users/Joe/PhD/Talks/MMM13/beta.eps', bbox_inches=0)
  plt.show()


pattern = re.compile('_(?P<IVtemp>\d*)K_NLDCIV_300uA_DigFilt10rep_(?P<state>\w*)_')
folder = DataFolder('/Users/Joe/PhD/Measurements/RN0151_4T/NLIVvsT/Both/',pattern = pattern)
folder.group(['state','IVtemp'])
folder.walk_groups(IV_group_Avg,group=True,replace_terminal=True)
folder.walk_groups(P_AP,group=True,replace_terminal=False)




