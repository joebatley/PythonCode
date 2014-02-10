import re
import numpy
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.Plot as plot

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
  return numpy.mean(x)

def quad(x,a,b,c):
  return a*x*x+b*x+c

def IV_group_Avg(folder,keys):
  folder[0].metadata['VTI-ITC']=''
  avg = Analysis.AnalyseFile(folder[0])
  avg.del_column('Voltage')
  avg.del_column('Current')
  avg.del_column('Column 2')
  for f in folder:
    avg.add_column(f.Voltage,str(f.metadata['iterator']))
  avg.apply(func, 1, replace = False, header = 'Mean NLVoltage')
  avg.add_column(folder[1].column('Current'),'Current')
  return avg


pattern = re.compile('_(?P<IVtemp>\d*)K_NLDCIV_300uA_DigFilt10rep_(?P<state>\w*)_')
folder = DataFolder('/Users/Joe/PhD/Measurements/RN0151_4T/NLIVvsT/70K-PandAP/',pattern = pattern)

print folder
folder.group(['state','IVtemp'])
folder.walk_groups(IV_group_Avg,group=True,replace_terminal=True)


p = Analysis.AnalyseFile(folder['P'][0])
fit = p.curve_fit(quad,'Current','Mean',bounds=lambda x,y:abs(x)>200e-6,result=True, replace=False, header="parabolic")
print fit[0][1]
p.subtract('Mean',p.column('Mean')[0],replace=True)
p.subtract('Mean',fit[0][0]*p.column('Current')**2,replace=False,header='minus background')
print p.column_headers
ap = Analysis.AnalyseFile()
ap.add_column(folder['AP'][0].column('Current'),'Current')
ap.add_column(folder['AP'][0].column('Mean'),'Mean')
print ap
ap.curve_fit(quad,'Current','Mean',bounds=lambda x,y:abs(x)>200e-6,result=True, replace=False, header="parabolic")
ap.subtract('Mean',ap.column('Mean')[0],replace=True)#,header='minus background')
ap.subtract('Mean',fit[0][0]*ap.column('Current')**2,replace=False,header='minus background')

#offset_p = folder['P'][0].column('Mean')[0]
#Voltage_p = folder['P'][0].column('Mean') - offset_p
#offset_ap = folder['AP'][0].column('Mean')[0]
#Voltage_ap = folder['AP'][0].column('Mean') - offset_ap


################# PLOT ###################

plt.title(r'')
plt.xlabel(r'Current ($\mu$A)')
plt.ylabel(r'Non Local Voltage ($\mu$V)')
plt.ticklabel_format(style='plain', scilimits=(3 ,3))
plt.hold(True)
#plt.plot(1e6*p.column('Current'),1e6*p.column('minus'),'-or')
plt.plot(1e6*p.column('Current'),1e6*p.column('minus'),'-or',label = 'P')
#plt.plot(1e6*ap.column('Current'),1e6*ap.column('minus'),'-ob')
plt.plot(1e6*ap.column('Current'),1e6*ap.column('minus'),'-ob',label = 'AP')
#plt.plot(1e6*p.column('Current'),1e6*(ap.column('minus')-p.column('minus')),'-b')
plt.grid(False)
plt.legend()
plt.show()



'''
def P_AP(folder,keys):
  plt.hold(True)
  for f in folder:
    f.metadata['VTI-ITC'] = 1.0
    a=Analysis.AnalyseFile(f)
    #fit, fitVar= a.curve_fit(quad,'Current','Mean NLVoltage',bounds=lambda x,y:abs(x)>150e-6,result=True,header='Fit') 
    offset = f.column('Mean')[0]
    Voltage = f.column('Mean') - offset
    plt.plot(a.column('Cur')*1e6,1e6*Voltage,label=str(f['IVtemp'])+' K')
    #print a.column_headers
    #maxVIp = numpy.max(a.search('Current',lambda x,y: x>0,'Mean NLVoltage'))
    #minVIp = numpy.min(a.search('Current',lambda x,y: x>0,'Mean NLVoltage'))
    #maxVIn = numpy.max(a.search('Current',lambda x,y: x<0,'Mean NLVoltage'))
    #minVIn = numpy.min(a.search('Current',lambda x,y: x<0,'Mean NLVoltage'))

    #current = a.Current*1e6
    #VoltagediffIp = maxVIp-minVIp
    #VoltagediffIn = maxVIn-minVIn
    
    
    plt.title(r'')
    plt.xlabel(r'Current ($\mu$A)')
    plt.ylabel(r'Non Local Voltage ($\mu$V) ')
    plt.ticklabel_format(style='plain', scilimits=(3 ,3))
    
    #plt.plot(current,maxV,label = str(a['IVtemp']))
    #print a['state'],a['IVtemp']
    #if a['state'] == 'P':
      #plt.plot(f['IVtemp'],VoltagediffIp*1e6,'ro')
      #plt.plot(f['IVtemp'],VoltagediffIn*1e6,'rx')
    #else:
      #plt.plot(f['IVtemp'],VoltagediffIp*1e6,'bo')
      #plt.plot(f['IVtemp'],VoltagediffIn*1e6,'bx')
    
  plt.legend()
  plt.show()

folder.walk_groups(P_AP,group=True,replace_terminal=False)
'''



