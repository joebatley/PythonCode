import re
import numpy
from scipy import interpolate
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize

fig_width_pt = 800.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 28,
          'axes.linewidth':2,
          'text.fontsize': 28,
          'title.fontsize':28,
          'legend.fontsize': 24,
          'xtick.labelsize': 28,
          'ytick.labelsize': 28,
          'xtick.direction': 'in',
          'ytick.direction': 'in',
          'xtick.major.size':10,
          'xtick.major.width':2,
          'ytick.major.size':10,
          'ytick.major.width':2,
          'figure.figsize': fig_size,
         'font.family':'Arial',
         'xtick.major.pad':20,
         'ytick.major.pad':20,
         'font.size':25,
         'lines.linewidth':4,
         'lines.markersize':15}
 
plt.rcParams.update(params)



################ READ FILE INFO ########################
def func(x):
  return numpy.mean(x)

def quad(x,a,b,c):
  return a*x*x+b*x+c
  
def heat(x,i,R,Ks,As,dz,Kcu,Acu,dx,Td,Ts): 
  y=(i**2)*R - (Ks*As/dz)*(x-Ts) - (Kcu*Acu/dx)*(x-Td) 
  return y

def IV_group_Avg(folder,keys):
  avg = Analysis.AnalyseFile(folder[0])
  avg.del_column('Voltage')
  avg.del_column('Current')
  avg.del_column('Column 2')
  for f in folder:
    avg.add_column(f.Voltage,str(f.metadata['iterator']))
  avg.apply(func, 1, replace = False, header = 'Mean NLVoltage')
  avg.add_column(folder[1].column('Current'),'Current')
  return avg






#################### DELTA R VS TEMP ####################

def DeltaRvT(folder,keys):
  APiterator = [5,10]
  AP = Analysis.AnalyseFile()
  P = Analysis.AnalyseFile()
  tsum = 0.0
  for f in folder:
    if f['iterator'] in APiterator:
      AP.add_column(f.column('Voltage'),str(f['iterator']))
    else:
      P.add_column(f.column('Voltage'),str(f['iterator']))
    tsum = tsum + f['Sample Temp']
    
  AP.apply(func,0,replace=False,header='Mean NLV')
  AP.add_column(f.Current,column_header = 'Current')
  P.apply(func,0,replace=False,header='Mean NLV')
  P.add_column(f.Current,column_header = 'Current')
  
  APfit= AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
  Pfit = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
  
  DeltaR = Pfit[2] - APfit[2]
  ErrDeltaR = numpy.sqrt((Pfit[3]**2)+(APfit[3]**2))
  
  Spinsig.append(DeltaR)
  Spinsig_error.append(ErrDeltaR)
  Temp.append(tsum/10)
  
  plt.hold(True)
  plt.title('$\Delta$R$_s$ vs T from linear coef of\nNLIV fit for '+f['Sample ID'],verticalalignment='bottom')
  plt.xlabel('Temperture (K)')
  plt.ylabel('$\Delta$R$_s$ (mV)')
  plt.errorbar(f['IVtemp'],1e3*DeltaR,1e3*ErrDeltaR,ecolor='k',marker='o',mfc='r', mec='k')
  #plt.plot(f['IVtemp'],ErrDeltaR,'ok')
  return Temp, Spinsig
  


#################### DELTA R VS TEMP ####################

def DeltaR_Background_vT(folder,keys):
  APiterator = [5,10]
  AP = Analysis.AnalyseFile()
  P = Analysis.AnalyseFile()

  for f in folder:
    if f['iterator'] in APiterator:
      AP.add_column(f.column('Voltage'),str(f['iterator']))
    else:
      P.add_column(f.column('Voltage'),str(f['iterator']))
     
  AP.apply(func,0,replace=False,header='Mean NLV')
  AP.add_column(f.Current,column_header = 'Current')
  P.apply(func,0,replace=False,header='Mean NLV')
  P.add_column(f.Current,column_header = 'Current')
  
  APfit= AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
  Pfit = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
  
  DeltaR_Bckgrnd = (Pfit[2] + APfit[2])/2
  ErrBack = numpy.sqrt((Pfit[3]**2)+(APfit[3]**2))
  
  Spinsig.append(DeltaR_Bckgrnd)
  Spinsig_error.append(ErrBack)
  Temp.append(f['IVtemp'])
  

  plt.hold(True)
  plt.title('R$_s$ vs T background from linear coef of\nNLIV fit for '+f['Sample ID'],verticalalignment='bottom')
  plt.xlabel('Temperture (K)')
  plt.ylabel('R$_s$ background (mV)')
  plt.errorbar(f['IVtemp'],1e3*DeltaR_Bckgrnd,1e3*ErrBack,ecolor='k',marker='o',mfc='k', mec='k')
  


#################### NL SPIN SIGNAL VS TEMP ####################

def RsvT(folder,keys):
  APiterator = [5,10]
  AP = Analysis.AnalyseFile()
  P = Analysis.AnalyseFile()
  APerrsum=0
  Perrsum=0

  for f in folder:
    a=Analysis.AnalyseFile(f)
    fit= a.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
   
    if f['iterator'] in APiterator:
      AP.add_column(fit,str(f['iterator']))
    else:
      P.add_column(fit,str(f['iterator']))
     
  AP.apply(func,0,replace=False,header='Mean Fit')
  P.apply(func,0,replace=False,header='Mean Fit')
    
  for i in range(len(AP.column_headers)):
      err = AP.data[3,i]/AP.data[2,i]
      APerrsum = APerrsum + err**2
  APRs = AP.column('Mean Fit')[2]
  APerr = APRs*numpy.sqrt(APerrsum)
    
  for i in range(len(P.column_headers)):
      err = P.data[3,i]/P.data[2,i]
      Perrsum = Perrsum + err**2
  PRs = P.column('Mean Fit')[2]
  Perr = PRs*numpy.sqrt(Perrsum)
      
  plt.hold(True)
  plt.title('R$_s$ vs T from linear coef of NLIV fit for '+f['Sample ID']+'\n Blue = P, Red = AP',verticalalignment='bottom')
  plt.xlabel('Temperture (K)')
  plt.ylabel('R$_s$ (mV/A)')
  plt.errorbar(f['IVtemp'],1e3*PRs,1e3*Perr,ecolor='k',marker='o',mfc='b', mec='k',label='P')
  plt.errorbar(f['IVtemp'],1e3*APRs,1e3*APerr,ecolor='k',marker='o',mfc='r', mec='k')
  
#################### PLOT AVERAGE NLIV AT GIVEN TEMP IN P AND AP ####################
   
def AvgIVplot(folder,keys):
  T = 10
  APiterator = [5,10]
  if folder[0]['IVtemp'] == T:#+1 or T-1:
    AP = Analysis.AnalyseFile()
    P = Analysis.AnalyseFile()
    
    for f in folder:
      if f['iterator'] in APiterator:
        AP.add_column(f.Voltage,str(f.metadata['iterator']))
      else:
        P.add_column(f.Voltage,str(f.metadata['iterator']))
        
    AP.apply(func,0,replace=False,header='Mean NLVoltage')
    AP.add_column(folder[1].column('Current'),'Current')
    P.apply(func,0,replace=False,header='Mean NLVoltage')
    P.add_column(folder[1].column('Current'),'Current')
    fitAP, fitVarAP= AP.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit')
    fitP, fitVarP= P.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit')
    scale = 1e6
    plt.hold(True)
    plt.title('NLIV of '+f['Sample ID']+' for P and AP at ' + str(T) + 'K',verticalalignment='bottom')
    plt.xlabel('Current ($\mu$A)')
    plt.ylabel('V$_{NL}$ ($\mu$V)')
    plt.plot(scale*P.Current,scale*P.column('Mean NLV'),'ob',label='P')
    plt.plot(scale*P.Current,scale*P.column('Fit'),'-g',label = r'$\alpha$ = ' + str.format("{0:.5f}", fitP[1]) + r' $\beta$ = ' + str.format("{0:.1f}", fitP[0]) )
    plt.plot(scale*AP.Current,scale*AP.column('Mean NLV'),'or',label='AP')
    plt.plot(scale*AP.Current,scale*AP.column('Fit'),'-k',label = r'$\alpha$ = ' + str.format("{0:.5f}", fitAP[1]) + r' $\beta$ = ' + str.format("{0:.1f}", fitAP[0]) )
    plt.legend().draggable()
  else:
    return 1  



#################### PLOT NLIV AT GIVEN TEMP IN P AND AP ####################
   
def IVplot(folder,keys):
  T = 50
  APiterator = [5,10]
  if folder[0]['IVtemp'] == T:
    scale = 1e6
    plt.hold(True)
    plt.title('NLIV in P and AP at ' + str(T) + 'K')
    plt.xlabel('Current ($\mu$A)')
    plt.ylabel('V$_{NL}$ ($\mu$V)')
    for f in folder:
      if f['iterator'] in APiterator:
        AP = Analysis.AnalyseFile(f)
        fit, fitVar= AP.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit')
        plt.plot(scale*f.Current,scale*f.column('Voltage'),'or',label=str(f.metadata['iterator'])+' '+str(fit[1]))
      else:
        P = Analysis.AnalyseFile(f)
        fit, fitVar= P.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit')
        plt.plot(scale*f.Current,scale*f.column('Voltage'),'ob',label=str(f.metadata['iterator'])+' '+str(fit[1]))
    plt.legend(loc='upper left')
  else:
    return 1  
    
    

#################### BETA COEF VS TEMP ####################
  
def DeltaBetavT(folder,keys):
  APiterator = [5,10]
  AP = Analysis.AnalyseFile()
  P = Analysis.AnalyseFile()
  APerrsum=0
  Perrsum=0

  for f in folder:
    a=Analysis.AnalyseFile(f)
    fit= a.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
   
    if f['iterator'] in APiterator:
      AP.add_column(fit,str(f['iterator']))
    else:
      P.add_column(fit,str(f['iterator']))
     
  AP.apply(func,0,replace=False,header='Mean Fit')
  P.apply(func,0,replace=False,header='Mean Fit')
    
  for i in range(len(AP.column_headers)):
      err = AP.data[1,i]/AP.data[0,i]
      APerrsum = APerrsum + err**2
  APRs = AP.column('Mean Fit')[0]
  APerr = APRs*numpy.sqrt(APerrsum)
    
  for i in range(len(P.column_headers)):
      err = P.data[1,i]/P.data[0,i]
      Perrsum = Perrsum + err**2
  PRs = P.column('Mean Fit')[0]
  Perr = PRs*numpy.sqrt(Perrsum)
  
  DeltaR = PRs-APRs
  ErrDeltaR = DeltaR*(numpy.sqrt((Perr**2)+(APerr**2)))
    
  plt.hold(True)
  plt.title(r'$\Delta \beta$ coef of NLIV vs Temp')
  plt.xlabel('Temperture (K)')
  plt.ylabel(r'$\Delta \beta$ (V/A$^2$)')
  plt.errorbar(f['IVtemp'],DeltaR,ErrDeltaR,ecolor='k',marker='o',mfc='b', mec='k')

  

  #################### AP AND P BETA COEF VS TEMP ####################
  
def BetavsT(folder,keys):
  tsum = 0.0
  avg = Analysis.AnalyseFile()
  for f in folder:
    avg.add_column(f.Voltage,str(f['iterator']))  
    tsum = tsum + f['Sample Temp']
    
  avg.apply(func,0,replace=False,header='Mean NLV')
  avg.add_column(f.Current,'Current') 
  fit= avg.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
    
  beta.append(fit[0])
  betaerr.append(fit[1])
  Temp.append(tsum/10)
  
  
  plt.hold(True)
  plt.title(r'$\beta$ coef of NLIV vs Temp for ' + f['Sample ID'],verticalalignment='bottom')
  plt.xlabel('Temperture (K)',labelpad=10)
  plt.ylabel(r'$\beta$ (V/A$^2$)',labelpad=10)
  plt.errorbar(f['IVtemp'],fit[0],fit[1],ecolor='k',marker='o',mfc='r', mec='k')
 

 #################### AP AND P BETA COEF VS TEMP ####################
  
def BetavsT_AP_P(folder,keys):
  AP = Analysis.AnalyseFile()
  P = Analysis.AnalyseFile()
  I = 300e-6

  for f in folder:
    a=Analysis.AnalyseFile(f)
    fit= a.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
   
    if f['iterator'] == 7:
      AP.add_column(fit,str(f['iterator']))
      AP['Sample Temp'] = f['Sample Temp']
      Spc = ((-0.01411*f['Sample Temp'])-0.11185)*1e-6  
      T_d = -fit[0]*(I*I)/Spc
      AP['DeltaTemp'] = T_d
    elif f['iterator'] == 6:
      P.add_column(fit,str(f['iterator']))
      P['Sample Temp'] = f['Sample Temp']
      Spc = ((-0.01411*f['Sample Temp'])-0.11185)*1e-6  
      T_d = -fit[0]*(I*I)/Spc
      P['DeltaTemp'] = T_d
  
  
    
  plt.hold(True)
  plt.title(r'$\beta$ coef of NLIV vs Temp')
  plt.xlabel('Temperture (K)')
  plt.ylabel(r'$\beta$ (V/A$^2$)')
  plt.plot(f['IVtemp'],P['DeltaTemp']-AP['DeltaTemp'],'ok')
  #plt.plot(f['IVtemp'],AP['DeltaTemp'],'or')
  

#################### Heat Transport ####################

def Heat(folder,keys):
  Beta = Analysis.AnalyseFile()
  I = 300e-6
  
  for f in folder:
    a=Analysis.AnalyseFile(f)
    fit= a.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
    Beta.add_column(fit,column_header=str(f['iterator']))
  if f['IVtemp']<290: 
      if f['IVtemp']>4:
            
          Beta.apply(func,0,replace=False,header='Mean Fit')
        
          KCu = NewK_Cu(f['IVtemp'])*1e2  
          KSi = NewK_Si(f['IVtemp'])
          res = abs(Res_Py(f['IVtemp']))
          #denom =  (KCu*Acu/dx) + (KSi*Asi/dz) 
          Spc = ((-0.01411*f['IVtemp'])-0.11185)*1e-6
          T_d = -fit[0]*(I*I)/Spc
          #T_i = (res*(I*I)+(KSi*Asi*f['IVtemp']/dz)+(KCu*Acu*T_d/dx))/denom
          T_i = scipy.optimize.fsolve(heat, 10,args=(I,res,KSi,Asi,dz,KCu,Acu,dx,T_d,f['IVtemp']))
          
          plt.hold(True)
          plt.title(r'Temperature Difference across device')
          plt.xlabel('Temperture (K)')
          plt.ylabel(r'Temperature Diff(K)')
          plt.errorbar(f['IVtemp'],T_i-T_d,0,ecolor='k',marker='o',mfc='r', mec='k')
          #plt.errorbar(f['IVtemp'],T_d,0,ecolor='k',marker='o',mfc='b', mec='k')
          #plt.errorbar(f['IVtemp'],T_i,0,ecolor='k',marker='o',mfc='r', mec='k')

      
          
#################### DATA FOR HEAT TRANSPORT ####################
Stoner.CSVFile()
K_Cu =  numpy.array([[0,0],
[1.400009,1.092419],
[2.798056,2.418300],
[3.573732,3.275956],
[4.505982,4.133937],
[9.949443,8.503286],
[12.438929,10.376189],
[15.394212,12.716993],
[19.918499,14.671941],
[23.043431,15.456650],
[29.465558,15.158688],
[36.054719,13.615915],
[42.022816,11.449274],
[49.402035,9.052095],
[56.458955,7.743759],
[63.984288,6.592041],
[74.327290,5.523992],
[89.363573,4.932617],
[100.794744,4.800695],
[111.756194,4.667799],
[135.400750,4.483400],
[145.264225,4.581692],
[300.0,4.501692]])

K_Si = numpy.array([[0.0,0.0],
[11.245201,0.127662],
[18.419407,0.145956],
[24.052527,0.173345],
[30.710408,0.203781],
[36.852840,0.243322],
[41.970511,0.279816],
[50.158083,0.340636],
[59.372169,0.398430],
[67.561494,0.453176],
[84.449457,0.574822],
[97.243634,0.666057],
[111.578022,0.751235],
[121.816870,0.812075],
[135.132632,0.872948],
[146.909937,0.933804],
[159.204444,0.979481],
[172.519329,1.043390],
[191.985413,1.116472],
[209.408110,1.162201],
[230.413528,1.232262],
[255.012185,1.290211],
[279.612595,1.342087],
[305.239520,1.390936]])

CuRvt = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/SC004_3_T_6221-2182 DC IV_Timed interval_RvT_CuBar_100uA_!0001.txt')
PyRvt = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/SC004_3_T_6221-2182 DC IV_Timed interval_0_PyInj_RvT_100uA_Full.txt')
PyRvt.sort('Sample Temp')
NewK_Cu = interpolate.interp1d(K_Cu[:,0],K_Cu[:,1])
NewK_Si = interpolate.interp1d(K_Si[:,0],K_Si[:,1])
Res_Cu = interpolate.interp1d(CuRvt[:,3],CuRvt[:,2])
Res_Py = interpolate.interp1d(PyRvt[:,3],PyRvt[:,2])

Acu = 130e-9*150e-9
Asi = 150e-9*18e-6
dz = 100e-9
dx = 500e-9



  
  
  

#################### IMPORTDATA AND WALK GROUPS ####################

pattern = re.compile('_(?P<state>\d*)_(?P<IVtemp>\d*)K_(?P<Inj>\w*)_NLIV_300uA_')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_2_T/NLIVvsHvsT_Py_Inj',pattern = pattern)
#folder.group(['IVtemp','Inj'])

print folder

Spinsig = []
Spinsig_error = []
beta = []
betaerr = []
Temp = []
Output = Stoner.DataFile()
print folder[0]
Output['Sample ID'] = folder[0]['Sample ID']
folder.group('IVtemp')

#folder.walk_groups(Heat,group=True,replace_terminal=True)
#folder.walk_groups(DeltaRvT,group=True,replace_terminal=True)
#folder.walk_groups(DeltaR_Background_vT,group=True,replace_terminal=True)
#folder.walk_groups(DeltaBetavT,group=True,replace_terminal=True)
folder.walk_groups(BetavsT,group=True,replace_terminal=True)
#folder.walk_groups(BetavsT_AP_P,group=True,replace_terminal=True)
#folder.walk_groups(RsvT,group=True,replace_terminal=True)
#folder.walk_groups(AvgIVplot,group=True,replace_terminal=True)
#folder.walk_groups(IVplot,group=True,replace_terminal=True)

#Output.add_column(Spinsig,column_header='DeltaR')
#Output.add_column(Spinsig_error,column_header = 'DeltaR err')
Output.add_column(beta,column_header='Beta')
Output.add_column(betaerr,column_header='Beta err')
#Output.add_column(Spinsig,column_header='Rs Bgrd')
#Output.add_column(Spinsig_error,column_header = 'Rs Bgrd err')
Output.add_column(Temp,column_header='Sample Temp')

Output.sort('Sample Temp')
print Output
#Output.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaR_vs_Sep/' + Output['Sample ID'] + '_DeltaRvsT.txt')
#Output.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Beta_vs_Sep/' + Output['Sample ID'] + '_BetavsT.txt')
#Output.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/RsBackground_vs_Sep/' + Output['Sample ID'] + '_Rs_Background_vsT.txt')
plt.tight_layout(pad=0.1, w_pad=0.0, h_pad=0.0)
plt.show()



