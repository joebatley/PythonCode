import re
import numpy
from scipy import interpolate
import pylab as plt
#import matplotlib.pyplot as plt
import Stoner
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
          #'axes.color_cycle':['b','r','k','g','p','c'],
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


S_Cu = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/Heat_Transport_Data/Thermopower_Copper.txt',1,2,',',',')
S_Py = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/Heat_Transport_Data/Thermopower_Permalloy.txt',1,2,',',',')
K_Cu = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/Heat_Transport_Data/Themalconductivity_Copper.txt',1,2,',',',')
K_Si = Stoner.CSVFile('/Volumes//data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/Heat_Transport_Data/Themalconductivity_Si.txt',1,2,',',',')
R = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/RN0151_4T_6221-2182 DC IV_Timed interval_0000_1.75_Cuspacer_RvT.txt')


NewS_Cu = interpolate.interp1d(S_Cu[:,0],S_Cu[:,1])
NewS_Py = interpolate.interp1d(S_Py[:,0],S_Py[:,1])
NewK_Cu = interpolate.interp1d(K_Cu[:,0],K_Cu[:,1])
NewK_Si = interpolate.interp1d(K_Si[:,0],K_Si[:,1])
Res = -1.0*R.column('Resistance')
NewR = interpolate.interp1d(R.column('Sample Temp')[::-1],Res[::-1])


Acu = 100e-9*50e-9
Asi = 100e-9*10e-6
dz = 100e-9
dx = 500e-9


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
  
  coef = Stoner.DataFile()
  for f in folder:
    
    
    a=Analysis.AnalyseFile()
    a['IVtemp'] = f['IVtemp']
    a['state'] = f['state']
    a.add_column(f.column('Current'),'Current')
    a.add_column(f.column('Mean'),'NLV')
    
    fit, fitVar= a.curve_fit(quad,'Current','NLV',bounds=lambda x,y:abs(x)>200e-6,result=True,header='Fit') 
    
    coef['state'] = a['state']
  
    '''
    plt.title(r'')
    plt.xlabel(r'Temperature (K)')
    plt.ylabel(r'$\Delta$Temp (K)')
    plt.ticklabel_format(style='plain', scilimits=(3 ,3))
    plt.hold(True)
    '''
    
    if f['state'] == 'P':
      KCu = NewK_Cu(f['IVtemp'])*1e2  
      KSi = NewK_Si(f['IVtemp'])
      denom =  (KCu*Acu/dx) + (KSi*Asi/dz) 
      Scu = NewS_Cu(f['IVtemp'])*1e-6
      Spy = NewS_Py(f['IVtemp'])*1e-6
      SpcBulk = Spy - Scu
      Spc = ((-0.01411*f['IVtemp'])-0.11185)*1e-6
      T_d = fit[0]*(300e-6*300e-6)/Spc
      T_dBulk = fit[0]*(300e-6*300e-6)/SpcBulk
      res = 200*NewR(f['IVtemp'])/min(Res)
      T_i = (res*(300e-6*300e-6)+(KSi*Asi*f['IVtemp']/dz)+(KCu*Acu*T_d/dx))/denom
      Alpha = (denom*fit[0])/(-1.0*Spc*res)
      col = list(fit)
      col.append(T_d)
      print col
      coef.add_column(col,str(a['IVtemp']))
      #plt.plot(f['IVtemp'],1e6*Spc,'ro')
      #plt.plot(f['IVtemp'],1e6*(Spy-Scu),'bo')
      #plt.plot(f['IVtemp'],T_d,'ro')
      #plt.plot(f['IVtemp'],T_dBulk,'bo')
      #plt.plot(f['IVtemp'],T_i,'bo')
      #plt.plot(f['IVtemp'],T_i-T_d,'bo')
      #print fitVar
      #plt.errorbar(f['IVtemp'],fit[0],numpy.sqrt(fitVar[0,0]),ecolor='k',marker='o',mfc='red', mec='red',ms=15.0)
      #print 'p'
      
    if f['state'] == 'AP':
      #print 'ap'
      KCu = NewK_Cu(f['IVtemp'])*1e2  
      KSi = NewK_Si(f['IVtemp'])
      denom =  (KCu*Acu/dx) + (KSi*Asi/dz) 
      Scu = NewS_Cu(f['IVtemp'])*1e-6
      Spy = NewS_Py(f['IVtemp'])*1e-6
      Spc = ((-0.01411*f['IVtemp'])-0.11185)*1e-6
      T_d = fit[0]*(300e-6*300e-6)/Spc
      res = 200*NewR(f['IVtemp'])/min(Res)
      T_i = (res*(300e-6*300e-6)+(KSi*Asi*f['IVtemp']/dz)+(KCu*Acu*T_d/dx))/denom
      Alpha = (denom*fit[0])/(-1.0*Spc*res)
      col = list(fit)
      col.append(T_d)
      print col
      coef.add_column(col,str(a['IVtemp']))
      #plt.plot(f['IVtemp'],1e6*Spc,'ro')
      #plt.plot(f['IVtemp'],1e6*(Spy-Scu),'bo')
      #plt.plot(f['IVtemp'],T_d,'ro')
      #plt.plot(f['IVtemp'],T_i,'bo')
      #plt.plot(f['IVtemp'],T_i-T_d,'bo')
      #plt.errorbar(f['IVtemp'],fit[0],numpy.sqrt(fitVar[0,0]),ecolor='k',marker='o',mfc='blue', mec='blue',ms=15.0)
      #plt.plot(f['IVtemp'],fit[0],'bx')
  #plt.legend().draggable()
  #plt.show()
  print coef
  return coef
  
pattern = re.compile('_(?P<IVtemp>\d*)K_NLDCIV_300uA_DigFilt10rep_(?P<state>\w*)_')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/NLIVvsT/Both/',pattern = pattern)
folder.group(['state','IVtemp'])
folder.walk_groups(IV_group_Avg,group=True,replace_terminal=True)
folder.walk_groups(P_AP,group=True,replace_terminal=True)

print folder['P']
print ''
print folder['AP']

fig, ax1 = plt.subplots()
ax1.set_xlabel('Substrate Temperature (K)')
plt.hold(True)

for column in folder['P'].column_headers:
  #print column
  #print folder['AP'].column_headers
  if column == '60':
    Delta = 1e6*(((folder['AP'].column('61')[1]-folder['P'].column(column)[1])/2)+folder['P'].column(column)[1])
        
    ax1.plot(int(column),Delta,'ko')
    ax1.set_ylabel('NL Spin Signal offset ($\mu$V/A)', color='k')
    for tl in ax1.get_yticklabels():
        tl.set_color('k')
    ax2 = ax1.twinx()
    ax2.plot(int(column),folder['AP'].column('61')[3],'bo')
    ax2.set_ylabel('$\Delta$T', color='b')
    for tl in ax2.get_yticklabels():
        tl.set_color('b')
  if column in folder['AP'].column_headers:
    print folder['AP'].column(column)[3]
    Delta = 1e6*(((folder['AP'].column(column)[1]-folder['P'].column(column)[1])/2)+folder['P'].column(column)[1])
    
    ax1.plot(int(column),Delta,'ko')
    ax1.set_ylabel('NL Spin Signal offset ($\mu$V/A)', color='k')
    for tl in ax1.get_yticklabels():
        tl.set_color('k')
    ax2 = ax1.twinx()
    ax2.plot(int(column),folder['AP'].column(column)[3],'bo')
    ax2.set_ylabel('$\Delta$T', color='b')
    for tl in ax2.get_yticklabels():
        tl.set_color('b')
plt.show()


'''
for column in folder['P'].column_headers:
  print column
  print folder['AP'].column_headers
  if column == '60':
    Delta = ((folder['AP'].column('61')[1]-folder['P'].column(column)[1])/2)+folder['P'].column(column)[1]
    plt.hold(True)
    plt.plot(int(column),Delta,'ko')
  if column in folder['AP'].column_headers:
    print folder['AP'].column(column)
    Delta = ((folder['AP'].column(column)[1]-folder['P'].column(column)[1])/2)+folder['P'].column(column)[1]
    plt.hold(True)
    plt.plot(int(column),Delta,'ko')
plt.show()


fig, ax1 = plt.subplots()
t = np.arange(0.01, 10.0, 0.01)
s1 = np.exp(t)
ax1.plot(t, s1, 'b-')
ax1.set_xlabel('time (s)')
# Make the y-axis label and tick labels match the line color.
ax1.set_ylabel('exp', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')


ax2 = ax1.twinx()
s2 = np.sin(2*np.pi*t)
ax2.plot(t, s2, 'r.')
ax2.set_ylabel('sin', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')
plt.show()




#plt.show()

'''













