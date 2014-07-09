import re
import numpy
from scipy import interpolate
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize

import Stoner.PlotFormats as SPF
import Stoner.Plot as SP

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



#################### NORM DELTA R VS TEMP ####################

def NormDeltaRvT(folder,keys):
  if folder[0]['IVtemp']<250 and folder[0]['IVtemp']>5:
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
    Spinsig.append(DeltaR/Res_Cu(tsum/10))
    Spinsig_error.append(ErrDeltaR)
    
    Temp.append(tsum/10)
    
    plt.hold(True)
    plt.title('$\Delta$R$_s$ vs T from linear coef of\nNLIV fit for '+f['Sample ID'],verticalalignment='bottom')
    plt.xlabel('Temperture (K)')
    plt.ylabel(r'$\Delta$R$_s$/$\rho$')
    plt.errorbar(f['IVtemp'],1e3*DeltaR,1e3*ErrDeltaR,ecolor='k',marker='o',mfc='r', mec='k')
    #plt.plot(f['IVtemp'],ErrDeltaR,'ok')
    return Temp, Spinsig


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
  
  Spinsig.append(DeltaR*1e3)
  Spinsig_error.append(ErrDeltaR)
  Temp.append(tsum/10)
  '''
  plt.hold(True)
  plt.title('$\Delta$R$_s$ vs T from linear coef of\nNLIV fit for '+f['Sample ID'],verticalalignment='bottom')
  plt.xlabel('Temperture (K)')
  plt.ylabel('$\Delta$R$_s$ (mV)')
  plt.errorbar(f['IVtemp'],1e3*DeltaR,1e3*ErrDeltaR,ecolor='k',marker='o',mfc='r', mec='k')
  #plt.plot(f['IVtemp'],ErrDeltaR,'ok')
  '''
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
  
  Spinsig.append(DeltaR_Bckgrnd*1e3)
  Spinsig_error.append(ErrBack)
  
  Temp.append(f['IVtemp'])
  
  '''
  plt.hold(True)
  plt.title('R$_s$ vs T background from linear coef of\nNLIV fit for '+f['Sample ID'],verticalalignment='bottom')
  plt.xlabel('Temperture (K)')
  plt.ylabel('R$_s$ background (mV)')
  plt.errorbar(f['IVtemp'],1e3*DeltaR_Bckgrnd,1e3*ErrBack,ecolor='k',marker='o',mfc='k', mec='k')
  '''  


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
  APRs = 1e3*AP.column('Mean Fit')[2]
  APerr = APRs*numpy.sqrt(APerrsum)
    
  for i in range(len(P.column_headers)):
      err = P.data[3,i]/P.data[2,i]
      Perrsum = Perrsum + err**2
  PRs = 1e3*P.column('Mean Fit')[2]
  Perr = PRs*numpy.sqrt(Perrsum)
  
  RSP.append(PRs)
  RSAP.append(APRs)  
  Temp.append(f['IVtemp'])
      
  '''
  plt.hold(True)
  plt.title('R$_s$ vs T from linear coef of NLIV fit for '+f['Sample ID']+'\n Blue = P, Red = AP',verticalalignment='bottom')
  plt.xlabel('Temperture (K)')
  plt.ylabel('R$_s$ (mV/A)')
  plt.errorbar(f['IVtemp'],1e3*PRs,1e3*Perr,ecolor='k',marker='o',mfc='b', mec='k',label='P')
  plt.errorbar(f['IVtemp'],1e3*APRs,1e3*APerr,ecolor='k',marker='o',mfc='r', mec='k')
  '''
#################### PLOT AVERAGE NLIV AT GIVEN TEMP IN P AND AP ####################
   
def AvgIVplot(folder,keys):
  T = 254
  APiterator = [5,10]
  ID=folder[0]['Sample ID']
  if folder[0]['IVtemp'] == T:#+1 or T-1:
    AP = Analysis.AnalyseFile()
    P = Analysis.AnalyseFile()
    
    for f in folder:
      if f['iterator'] in APiterator:
        AP.add_column(f.Voltage,str(f.metadata['iterator']))
      else:
        P.add_column(f.Voltage,str(f.metadata['iterator']))
    

    # Average IVs and multiply by prefactor for plotting. minus sign is because voltage and current leades were swapped in measurment.    
    AP.apply(func,0,replace=False,header='V$_{NL}$')
    AP.mulitply('V$_{NL}$', -1.0, replace=True, header='V$_{NL}$ (V)')
    AP.add_column(folder[1].column('Current'),'Current')
    AP.mulitply('Current', -1.0, replace=True, header='I (A)')
    P.apply(func,0,replace=False,header='V$_{NL}$')
    P.mulitply('V$_{NL}$', -1.0, replace=True, header='V$_{NL}$ (V)')
    P.add_column(folder[1].column('Current'),'Current')
    P.mulitply('Current', -1.0, replace=True, header='I (A)')
    
    fitAP, fitVarAP= AP.curve_fit(quad,'I (A)','V$_{NL}$ (V)',bounds=lambda x,y:x,result=True,header='Fit')
    fitP, fitVarP= P.curve_fit(quad,'I (A)','V$_{NL}$ (V)',bounds=lambda x,y:x,result=True,header='Fit')
    scale = 1e6
    
    p=SP.PlotFile(P)
    '''
    for i in range(len(p)):
      if i < len(p)/4:
        p[i].mask=True
      if i > len(p)*3/4:
        p[i].mask=True
    '''
    print p.column_headers
    p.setas="y.........x"
    p.template=SPF.JTBPlotStyle
    title = None
    p.plot(label=None,figure=2,title=title)
    p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/NLIV_FITTING/'+ID+'_NLIVat'+str(T)+'K/'+ID+'_'+str(T)+'K_NLIV_P.txt')    
    
    q=SP.PlotFile(AP)
    print q.column_headers
    '''
    for i in range(len(q)):
      if i < len(p)/4:
        q[i].mask=True
      if i > len(p)*3/4:
        q[i].mask=True
    '''
    q.setas="y...x"#
    q.template=SPF.JTBPlotStyle
    title = None
    q.plot(label=None,figure=2,title=title)
    q.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/NLIV_FITTING/'+ID+'_NLIVat'+str(T)+'K/'+ID+'_'+str(T)+'K_NLIV_AP.txt')
  else:
    return 1  

#################### PLOT NLIV AT GIVEN TEMP IN P AND AP ####################
   
def DRIVplot(folder,keys):
  T = 281
  APiterator = [5,10]
  AP = Analysis.AnalyseFile()
  P = Analysis.AnalyseFile()
  if folder[0]['IVtemp'] == T:
    scale = 1e6
    plt.hold(True)
    plt.title('NLIV in P and AP at ' + str(T) + 'K')
    plt.xlabel('Current ($\mu$A)')
    plt.ylabel('V$_{NL}$ ($\mu$V)')
    for f in folder:
      if f['iterator'] in APiterator:
        AP.add_column(f.Voltage,str(f['iterator']))
      else:
        P.add_column(f.Voltage,str(f['iterator']))        
    AP.apply(func,0,replace=False,header='Mean NLVoltage')
    P.apply(func,0,replace=False,header='Mean NLVoltage')    
    
    I = numpy.arange(-295e-6,295e-6,1e-6)
    
    ap = interpolate.interp1d(f.column('Current'),AP.column('Mean NLV'))    
    p = interpolate.interp1d(f.column('Current'),P.column('Mean NLV')) 
    
    print P
    plt.title(' ',verticalalignment='bottom')
    plt.xlabel('Current ($\mu$A)')
    #plt.ylabel('V$_{NL}$/|I| (V/A)')
    plt.ylabel('$\Delta$V$_{NL}$/|I| (mV/A)') 
    plt.plot(f.column('Current')*scale,1e3*(P.column('Mean NLV')-AP.column('Mean NLV'))/abs(f.column('Current')),label =''+str(T)+ ' K')
    #plt.plot(f.column('Current')*scale,1e3*(P.column('Mean NLV'))/abs(f.column('Current')),label ='P at '+str(T)+ ' K')
    #plt.plot(f.column('Current')*scale,1e3*(AP.column('Mean NLV'))/abs(f.column('Current')),label ='AP at '+str(T)+ ' K')        
    plt.legend(loc='upper left')
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
  
def NormBetavsT(folder,keys):
    
  if folder[0]['Sample ID'] == 'SC004_2_T':
    tsum = 0.0
    avg = Analysis.AnalyseFile()
    for f in folder:
      avg.add_column(f.Voltage,str(f['iterator']))  
      tsum = tsum + f['Sample Temp']
      
    avg.apply(func,0,replace=False,header='Mean NLV')
    avg.add_column(f.Current,'Current') 
    fit= avg.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
      
    beta.append(fit[0]/Inj_2(tsum/10))
    betaerr.append(fit[1])
    Temp.append(tsum/10)
    print folder[0]['Sample ID']
  else:
    tsum = 0.0
    avg = Analysis.AnalyseFile()
    for f in folder:
      avg.add_column(f.Voltage,str(f['iterator']))  
      tsum = tsum + f['Sample Temp']
      
    avg.apply(func,0,replace=False,header='Mean NLV')
    avg.add_column(f.Current,'Current') 
    fit= avg.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
      
    beta.append(fit[0]/Inj_6(tsum/10))
    betaerr.append(fit[1])
    Temp.append(tsum/10)
    
  title = r'$\beta$/inj resistance coef of NLIV vs Temp for ' + f['Sample ID']
  return title  
  '''
  plt.hold(True)
  plt.title(r'$\beta$ coef of NLIV vs Temp for ' + f['Sample ID'],verticalalignment='bottom')
  plt.xlabel('Temperture (K)',labelpad=10)
  plt.ylabel(r'$\beta$ (V/A$^2$)',labelpad=10)
  plt.errorbar(f['IVtemp'],fit[0],fit[1],ecolor='k',marker='o',mfc='r', mec='k')
  '''

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

def HeatAnalysis(folder,keys):
  Beta = 0
  T = 0
  I = 300e-6
  
  for f in folder:
    a=Analysis.AnalyseFile(f)
    fit= a.curve_fit(quad,'Current','Voltage',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
    Beta = Beta + fit[0]
    T = T + f['Sample Temp']
  
  Beta = Beta /10
  T = T/10
  KCu = NewK_Cu(T)*1e2  
  KSi = NewK_Si(T)
  res = abs(Inj_6(T))
  #denom =  (KCu*Acu/dx) + (KSi*Asi/dz) 
  Spc = ((-0.01411*T)-0.11185)*1e-6
  T_d = -fit[0]*(I*I)/Spc
  #T_i = (res*(I*I)+(KSi*Asi*f['IVtemp']/dz)+(KCu*Acu*T_d/dx))/denom
  T_i = scipy.optimize.fsolve(heat, 10,args=(I,res,KSi,Asi,dz,KCu,Acu,dx,T_d,T))
  
  row = numpy.array([T,Beta,T_i,T_d,T_i-T_d])  
  heatdata.append(row)
  #plt.hold(True)
  #plt.title(r'Temperature rise at the detector')
  #plt.xlabel('Temperture (K)')
  #plt.ylabel(r'T$_d$ - T$_s$')
  #plt.errorbar(f['IVtemp'],T_d,0,ecolor='k',marker='o',mfc='r', mec='k',label = f['Sample ID'])
  #plt.errorbar(f['IVtemp'],T_d,0,ecolor='k',marker='o',mfc='b', mec='k')
  #plt.errorbar(f['IVtemp'],T_i,0,ecolor='k',marker='o',mfc='r', mec='k')
  #plt.tight_layout()

  
          
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

InjRvT_2_T = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Injector Resistance/SC004_2_T_6221-2182 DC IV_Timed interval_0_3K_PyInj_RvsT_300uA_.txt')
InjRvT_2_T.sort('Sample Temp')
InjRvT_6_T = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Injector Resistance/SC004_6_T_6221-2182 DC IV_Timed interval_0_RvT_PyInj_100uA_.txt')
InjRvT_6_T.sort('Sample Temp')
CuRvt = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Cu spacer resistance/Resistivity/SC004_2_T_Cu_resistivity_vs_T.txt')
#PyRvt = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Py Res/RN0094_2_res.txt')
#PyRvt.sort('Sample Temp')
CuRvt.sort('T (K)')
NewK_Cu = interpolate.interp1d(K_Cu[:,0],K_Cu[:,1])
NewK_Si = interpolate.interp1d(K_Si[:,0],K_Si[:,1])
Res_Cu = interpolate.interp1d(CuRvt[:,4],CuRvt[:,2])
#Res_Py = interpolate.interp1d(PyRvt[:,3],PyRvt[:,2])
Inj_2 = interpolate.interp1d(InjRvT_2_T[:,3],InjRvT_2_T[:,2])
Inj_6 = interpolate.interp1d(InjRvT_6_T[:,3],InjRvT_6_T[:,2])

Acu = 130e-9*150e-9
Asi = 150e-9*16e-6
dz = 1000e-9
dx = 1325e-9

Seperation = {1:325e-9,
              2:425e-9,
              3:525e-9,
              4:625e-9,
              5:725e-9,
              6:925e-9,
              7:1125e-9,
              8:1325e-9,
              9:1525e-9,}

  
  
  

#################### IMPORTDATA AND WALK GROUPS ####################

pattern = re.compile('_(?P<state>\d*)_(?P<IVtemp>\d*)K_(?P<Inj>\w*)_NLIV_300uA_')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/NLIVvsHvsT_V_Inj',pattern = pattern)
#folder.group(['IVtemp','Inj'])
print folder[0]

Spinsig = []
Spinsig_error = []
beta = []
betaerr = []
Temp = []
heatdata = []
RSP=[]
RSAP=[]

Output = Stoner.DataFile()
Output['Sample ID'] = folder[0]['Sample ID']
folder.group('IVtemp')
print folder

'''
folder.walk_groups(HeatAnalysis,group=True,replace_terminal=True)
Heat = Stoner.DataFile()
Heat.column_headers = ['T (K)','$\Beta$','T$_i$-T$_s$','T$_d$-T$_s$','T$_i$-T$_d$']
Heat['Sample ID'] = Output['Sample ID']
Heat.data = heatdata
Heat.sort('T (K)')
Heat.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Heat Analysis/' + Heat['Sample ID'] + '_TempdatavsT.txt')
print Heat

p=SP.PlotFile(Heat)
p.setas="x...y"
p.template=SPF.DefaultPlotStyle
title = r'$\Delta$R$_s$/$\rho$ vs temperature'
p.plot(label=p['Sample ID'],figure=1,title=title)
'''


#folder.walk_groups(DRIVplot,group=True,replace_terminal=True)
#folder.walk_groups(DeltaRvT,group=True,replace_terminal=True)
#folder.walk_groups(NormDeltaRvT,group=True,replace_terminal=True)
#folder.walk_groups(DeltaR_Background_vT,group=True,replace_terminal=True)
#folder.walk_groups(DeltaBetavT,group=True,replace_terminal=True)
#folder.walk_groups(BetavsT,group=True,replace_terminal=True)
#folder.walk_groups(NormBetavsT,group=True,replace_terminal=True)
#folder.walk_groups(BetavsT_AP_P,group=True,replace_terminal=True)
#folder.walk_groups(RsvT,group=True,replace_terminal=True)
folder.walk_groups(AvgIVplot,group=True,replace_terminal=True)
#folder.walk_groups(IVplot,group=True,replace_terminal=True)

#Output.add_column(Spinsig,column_header=r'Mean $\alpha$ (mV/A)')
#Output.add_column(Spinsig_error,column_header = 'DeltaR err')
#Output.add_column(beta,column_header='Beta')
#Output.add_column(betaerr,column_header='Beta err')
Output.add_column(RSP,column_header=r'$\alpha$ (mV/A)')
Output.add_column(RSAP,column_header=r'$\alpha$ (mV/A)')
#Output.add_column(Spinsig,column_header='Rs Bgrd')
#Output.add_column(Spinsig_error,column_header = 'Rs Bgrd err')
Output.add_column(Temp,column_header='Temperature (K)')

Output.sort('Temperature (K)')
print Output
#print Output.data
#Output.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaR_vs_Sep/' + Output['Sample ID'] + '_NormDeltaRvsT.txt')
##Output.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Beta_vs_Sep/' + Output['Sample ID'] + '_BetavsT.txt')
#Output.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/RsBackground_vs_Sep/' + Output['Sample ID'] + '_Rs_Background_vsT.txt')
#plt.tight_layout()
p=SP.PlotFile(Output)
p.setas="yyx"
p.template=SPF.JTBPlotStyle
title = None
p.plot(label=p['Sample ID'],figure=1,title=title)
'''
q=SP.PlotFile(Output)
q.setas=".yx"
q.template=SPF.JTBPlotStyle
title = None
q.plot(label=None,figure=1,title=title)
'''

