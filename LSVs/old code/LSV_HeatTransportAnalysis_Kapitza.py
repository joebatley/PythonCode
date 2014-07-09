import re
import numpy
from scipy import interpolate
import pylab as plt
#import matplotlib.pyplot as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize

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
         'lines.markersize':15,
         }
 
plt.rcParams.update(params)


K_Cu = Stoner.CSVFile('/Users/Joe/PhD/Measurements/RN0151/Transport/Heat_Transport_Data/Themalconductivity_Copper.txt',1,2,',',',')
K_Si = Stoner.CSVFile('/Users/Joe/PhD/Measurements/RN0151/Transport/Heat_Transport_Data/Themalconductivity_Si.txt',1,2,',',',')
R = Stoner.DataFile('/Users/Joe/PhD/Measurements/RN0151/Transport/RN0151_4T/RN0151_4T_6221-2182 DC IV_Timed interval_0000_1.75_Cuspacer_RvT.txt')

NewK_Cu = interpolate.interp1d(K_Cu[:,0],K_Cu[:,1])
NewK_Si = interpolate.interp1d(K_Si[:,0],K_Si[:,1])
Res = -1.0*R.column('Resistance')
NewR = interpolate.interp1d(R.column('Sample Temp')[::-1],Res[::-1])


Acu = 100e-9*50e-9
AsCu = 100e-9*500e-9
Asi = 100e-9*10e-6
dz = 100e-9
dx = 500e-9
sig = 5.67e-8
emis = 0.05
i=300e-6

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
  print '1'
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
  
    def heat(x,i,R,Ks,As,dz,Kcu,Acu,dx,sig,emis,Asc,Td,Ts): 
        
        alpha = (15*Ks)/(dz*x**3)        
        Tk = (x+alpha*Ts)/(alpha + 1)
        y=(i**2)*R - (Ks*As/dz)*(Tk-Ts) - (Kcu*Acu/dx)*(x-Td) - As*sig*emis*(x**4-Ts**4) - Asc*sig*emis*0.2*(Td**5-x**5) - Asc*sig*emis*Ts**4
        print x-Tk        
        return y
        
    if f['state'] == 'P':
      KCu = NewK_Cu(f['IVtemp'])*1e2  
      KSi = NewK_Si(f['IVtemp'])
      denom =  (KCu*Acu/dx) + (KSi*Asi/dz) 
      Spc = ((-0.01411*f['IVtemp'])-0.11185)*1e-6
      res = 200*NewR(f['IVtemp'])/min(Res)
      
      T_d = abs(fit[0])*(i**2)/abs(Spc)
      T_i = scipy.optimize.fsolve(heat, 10,args=(i,res,KSi,Asi,dz,KCu,Acu,dx,sig,emis,AsCu,T_d,f['IVtemp']))
      print'fin'
      col = list(fit)
      col.append(T_i-T_d)
      col.append(T_i)
      col.append(T_d)
      col.append(fit[0])
      col.append(Spc)
      coef.add_column(col,str(a['IVtemp']))
    
      
    if f['state'] == 'AP':
      KCu = NewK_Cu(f['IVtemp'])*1e2  
      KSi = NewK_Si(f['IVtemp'])
      denom =  (KCu*Acu/dx) + (KSi*Asi/dz) 
      Spc = ((-0.01411*f['IVtemp'])-0.11185)*1e-6
      res = 200*NewR(f['IVtemp'])/min(Res)
        
      T_d = abs(fit[0])*(i**2)/abs(Spc)
      T_i = scipy.optimize.fsolve(heat, 10,args=(i,res,KSi,Asi,dz,KCu,Acu,dx,sig,emis,AsCu,T_d,f['IVtemp']))
      print 'fin'
      col = list(fit)
      col.append(T_i-T_d)
      col.append(T_i)
      col.append(T_d)
      col.append(fit[0])
      col.append(Spc)
      print col
      coef.add_column(col,str(a['IVtemp']))
      
  
  return coef
  
pattern = re.compile('_(?P<IVtemp>\d*)K_NLDCIV_300uA_DigFilt10rep_(?P<state>\w*)_')
folder = DataFolder('/Users/Joe/PhD/Measurements/RN0151/Transport/RN0151_4T/NLIVvsT/Both/',pattern = pattern)
folder.group(['state','IVtemp'])
folder.walk_groups(IV_group_Avg,group=True,replace_terminal=True)
folder.walk_groups(P_AP,group=True,replace_terminal=True)


fig, ax1 = plt.subplots()
ax1.set_xlabel('Substrate Temperature (K)')
plt.hold(True)

for column in folder['P'].column_headers:
  #print column
  #print folder['AP'].column_headers
  if column == '60':
    Delta = 1e6*(((folder['AP'].column('61')[1]-folder['P'].column(column)[1])/2)+folder['P'].column(column)[1])
        
    ax1.plot(int(column),Delta,'ko')
    #ax1.plot(int(column),folder['P'].column(column)[3],'ro',label='T$_i$')
    #ax1.plot(int(column),folder['P'].column(column)[5],'bo',label = 'T$_d$')
    ax1.set_ylabel('NL background', color='k')
    for tl in ax1.get_yticklabels():
        tl.set_color('k')
    plt.legend(loc='upper right')    
    ax2 = ax1.twinx()
    ax2.plot(int(column),folder['P'].column(column)[3],'ro')
    ax2.set_ylabel('$\Delta$T', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
  else:
      if column in folder['AP'].column_headers:
        
        Delta = 1e6*(((folder['AP'].column(column)[1]-folder['P'].column(column)[1])/2)+folder['P'].column(column)[1])
        ax1.plot(int(column),Delta,'ko')
        #ax1.plot(int(column),folder['P'].column(column)[4],'ro')
        #ax1.plot(int(column),folder['P'].column(column)[3],'bo')
        ax1.set_ylabel('NL background', color='k')
        for tl in ax1.get_yticklabels():
            tl.set_color('k')
        ax2 = ax1.twinx()
        ax2.plot(int(column),folder['AP'].column(column)[3],'ro')
        ax2.plot(int(column),folder['P'].column(column)[5],'bo',label = 'T$_d$')
        ax2.set_ylabel('$\Delta$T', color='r')
        for tl in ax2.get_yticklabels():
            tl.set_color('r')
plt.show()












