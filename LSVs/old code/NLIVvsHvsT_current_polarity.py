# -*- coding: utf-8 -*-
"""
Created on Fri Mar  7 12:31:35 2014

@author: py07jtb
"""

import re
import numpy
from scipy import interpolate
from scipy.interpolate import splrep, splev

from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP



########### Functions to call in main script ########
def quad(x,a,b,c):
  return a*x*x+b*x+c

def avg(x):
  return numpy.mean(x)





########### Function sto anallyse data #############

def Alpha_vs_T_PandN_Current(folder):
  ''' Function to fit  NLIV at each temperature and plot Alpha for posative and negative currents. '''
    
  folder.group('IVtemp')
  folder.sort('IVtemp')
  APiterator = [5,10]
  
  T=[]
  AlphaPosP=[]
  AlphaPosAP=[]
  AlphaNegP=[]
  AlphaNegAP=[]
  AlphaPosPerr=[]
  AlphaPosAPerr=[]
  AlphaNegPerr=[]
  AlphaNegAPerr=[] 
  
  
  for key in folder.groups.keys():
      
    AP = Analysis.AnalyseFile()
    P = Analysis.AnalyseFile()
    tsum = 0.0
    
    for f in folder.groups[key]:
      if f['iterator'] in APiterator:
        AP.add_column(f.column('Voltage'),str(f['iterator']))
      else:
        P.add_column(f.column('Voltage'),str(f['iterator']))
      tsum = tsum + f['Sample Temp']
      
    AP.apply(avg,0,replace=False,header='Mean NLV')
    AP.add_column(f.Current,column_header = 'Current')
    P.apply(avg,0,replace=False,header='Mean NLV')
    P.add_column(f.Current,column_header = 'Current')
    
    APfitPOS = AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x>0,result=True,header='Fit',asrow=True)
    APfitNEG = AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x<0,result=True,header='Fit',asrow=True)
    PfitPOS = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x>0,result=True,header='Fit',asrow=True)
    PfitNEG = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x<0,result=True,header='Fit',asrow=True)
    
    
    T.append(tsum/len(folder.groups[key]))
    AlphaPosP.append(PfitPOS[2])
    AlphaPosAP.append(APfitPOS[2])
    AlphaNegP.append(PfitNEG[2])
    AlphaNegAP.append(APfitNEG[2])
    AlphaPosPerr.append(PfitPOS[3])
    AlphaPosAPerr.append(APfitPOS[3])
    AlphaNegPerr.append(PfitNEG[3])
    AlphaNegAPerr.append(APfitNEG[3])
    
  results = Analysis.AnalyseFile()
  results.add_column(AlphaPosP,column_header=r'$\alpha_{P}^{\plus}$')
  results.add_column(AlphaPosPerr,column_header=r'err$\alpha_{P}^{\plus}$')
  results.add_column(AlphaPosAP,column_header=r'$\alpha_{AP}^{\plus}$')
  results.add_column(AlphaPosAPerr,column_header=r'err$\alpha_{AP}^{\plus}$')
  results.add_column(AlphaNegP,column_header=r'$\alpha_{P}^{\minus}$')
  results.add_column(AlphaNegPerr,column_header=r'err$\alpha_{P}^{\minus}$')
  results.add_column(AlphaNegAP,column_header=r'$\alpha_{AP}^{\minus}$')
  results.add_column(AlphaNegAPerr,column_header=r'err$\alpha_{AP}^{\minus}$')
  results.add_column(T,column_header=r'Temperature (K)')
  results.sort('Temp')
  
  results.subtract(r'$\alpha_{P}^{\plus}$',r'$\alpha_{P}^{\minus}$',header=r'$\alpha_{P}^{diff}$',replace=False)
  results.add_column(numpy.sqrt(results.column(r'err$\alpha_{P}^{\plus}$')**2+results.column(r'err$\alpha_{P}^{\minus}$')**2),column_header=r'err$\alpha_{P}^{diff}$')
  results.subtract(r'$\alpha_{AP}^{\plus}$',r'$\alpha_{AP}^{\minus}$',header=r'$\alpha_{AP}^{diff}$',replace=False)
  results.add_column(numpy.sqrt(results.column(r'err$\alpha_{AP}^{\plus}$')**2+results.column(r'err$\alpha_{AP}^{\minus}$')**2),column_header=r'err$\alpha_{AP}^{diff}$')
  
  

  p=SP.PlotFile(results)
  print p.column_headers
  #p.setas="y.........xe."
  p.template=SPF.JTBPlotStyle
  label = r'$\alpha_{P}^{diff}$'
  title = ' '
  #p.plot(label = label,title=title,figure=2)  
  p.plot_xy('Temp',[r'$\alpha_{P}^{\plus}$',r'$\alpha_{AP}^{\plus}$',r'$\alpha_{P}^{\minus}$',r'$\alpha_{AP}^{\minus}$'],label = label,title=title,figure=2)
  #p.plot_xy('Temp',[r'$\alpha_{P}^{diff}$',r'$\alpha_{AP}^{diff}$'],label = label,title=title,figure=2)
  return p



def Delta_Alpha_vs_T_PandN_Current(folder):
  ''' Function to fit  NLIV at each temperature and plot  Delta Alpha independently for posative and negative currents. '''
    
  folder.group('IVtemp')
  folder.sort('IVtemp')
  APiterator = [5,10]
  
  T=[]
  DelatAlphaPos=[]
  DeltaAlphaNeg=[]
  errDelatAlphaPos=[]
  errDeltaAlphaNeg=[]
  
  for key in folder.groups.keys():
      
    AP = Analysis.AnalyseFile()
    P = Analysis.AnalyseFile()
    tsum = 0.0
    
    for f in folder.groups[key]:
      if f['iterator'] in APiterator:
        AP.add_column(f.column('Voltage'),str(f['iterator']))
      else:
        P.add_column(f.column('Voltage'),str(f['iterator']))
      tsum = tsum + f['Sample Temp']
      
    AP.apply(avg,0,replace=False,header='Mean NLV')
    AP.add_column(f.Current,column_header = 'Current')
    P.apply(avg,0,replace=False,header='Mean NLV')
    P.add_column(f.Current,column_header = 'Current')
    
    APfitPOS = AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x>0,result=True,header='Fit',asrow=True)
    APfitNEG = AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x<0,result=True,header='Fit',asrow=True)
    PfitPOS = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x>0,result=True,header='Fit',asrow=True)
    PfitNEG = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x<0,result=True,header='Fit',asrow=True)
    
    
    T.append(tsum/len(folder.groups[key]))
    DelatAlphaPos.append(PfitPOS[2]-APfitPOS[2])
    DeltaAlphaNeg.append(PfitNEG[2]-APfitNEG[2])
    errDelatAlphaPos.append(numpy.sqrt(PfitPOS[3]**2+APfitPOS[3]**2))
    errDeltaAlphaNeg.append(numpy.sqrt(PfitNEG[3]**2+APfitNEG[3]**2))
    
  results = Analysis.AnalyseFile()
  results.add_column(DelatAlphaPos,column_header=r'$\Delta\alpha^{\plus}$')
  results.add_column(errDelatAlphaPos,column_header=r'err$\Delta\alpha^{\plus}$')
  results.add_column(DeltaAlphaNeg,column_header=r'$\Delta\alpha^{\minus}$')
  results.add_column(errDeltaAlphaNeg,column_header=r'$\Delta\alpha^{\minus}$')
  results.add_column(T,column_header=r'Temperature (K)')
  results.sort('Temp')
  print results

  p=SP.PlotFile(results)
  print p.column_headers
  p.setas="ye..x"
  p.template=SPF.JTBPlotStyle
  label = None
  title = ' '
  #p.plot_xy('Temp',[r'$\Delta\alpha^{\plus}$',r'$\Delta\alpha^{\minus}$'],label = label,title=title,figure=2)
  p.plot(label = label,title=title,figure=2)
  return p




def Delta_Alpha_vs_T(folder):
  ''' Function to fit  NLIV at each temperature and plot Delta Alpha for posative and negative currents. '''
    
  folder.group('IVtemp')
  folder.sort('IVtemp')
  APiterator = [5,10]
  
  T=[]
  DelatAlpha=[]
  
  
  for key in folder.groups.keys():
      
    AP = Analysis.AnalyseFile()
    P = Analysis.AnalyseFile()
    tsum = 0.0
    
    for f in folder.groups[key]:
      if f['iterator'] in APiterator:
        AP.add_column(f.column('Voltage'),str(f['iterator']))
      else:
        P.add_column(f.column('Voltage'),str(f['iterator']))
      tsum = tsum + f['Sample Temp']
      
    AP.apply(avg,0,replace=False,header='Mean NLV')
    AP.add_column(f.Current,column_header = 'Current')
    P.apply(avg,0,replace=False,header='Mean NLV')
    P.add_column(f.Current,column_header = 'Current')
    
    APfit = AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
    Pfit = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x,result=True,header='Fit',asrow=True)
    
    
    T.append(tsum/len(folder.groups[key]))
    DelatAlpha.append(Pfit[2]-APfit[2])
    
    
  results = Analysis.AnalyseFile()
  results.add_column(DelatAlpha,column_header=r'$\Delta\alpha$')
  #results.subtract(r'$\Delta\alpha$',max(results.column(r'$\Delta\alpha$')),header='test')
  results.add_column(T,column_header=r'Temperature (K)')
  results.sort('Temp')
  print results

  p=SP.PlotFile(results)
  print p.column_headers
  #p.setas="yyyyx"
  p.template=SPF.JTBPlotStyle
  label = None
  title = ' '
  p.plot_xy('Temp',[r'$\Delta\alpha$',r'$\Delta\alpha$'],label = label,title=title,figure=2)
  #p.plot_xy('Temp','test',label = label,title=title,figure=2)
  return p




def Mean_Alpha_vs_T_PandN_Current(folder):
  ''' Function to fit  NLIV at each temperature and plot  Mean Alpha independently for posative and negative currents. '''
  
  ID = folder[0]['Sample ID']  
  folder.group('IVtemp')
  folder.sort('IVtemp')
  APiterator = [5,10]
  
  T=[]
  MeanAlphaPos=[]
  MeanAlphaNeg=[]
  errMeanAlphaPos=[]
  errMeanAlphaNeg=[]
  
  for key in folder.groups.keys():
      
    AP = Analysis.AnalyseFile()
    P = Analysis.AnalyseFile()
    tsum = 0.0
    
    for f in folder.groups[key]:
      if f['iterator'] in APiterator:
        AP.add_column(f.column('Voltage'),str(f['iterator']))
      else:
        P.add_column(f.column('Voltage'),str(f['iterator']))
      tsum = tsum + f['Sample Temp']
      
    AP.apply(avg,0,replace=False,header='Mean NLV')
    AP.add_column(f.Current,column_header = 'Current')
    P.apply(avg,0,replace=False,header='Mean NLV')
    P.add_column(f.Current,column_header = 'Current')
    
    APfitPOS = AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x>0,result=True,header='Fit',asrow=True)
    APfitNEG = AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x<0,result=True,header='Fit',asrow=True)
    PfitPOS = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x>0,result=True,header='Fit',asrow=True)
    PfitNEG = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x<0,result=True,header='Fit',asrow=True)
    
    
    T.append(tsum/len(folder.groups[key]))
    MeanAlphaPos.append((PfitPOS[2]+APfitPOS[2])/2)
    MeanAlphaNeg.append((PfitNEG[2]+APfitNEG[2])/2)
    errMeanAlphaPos.append(numpy.sqrt(PfitPOS[3]**2+APfitPOS[3]**2))
    errMeanAlphaNeg.append(numpy.sqrt(PfitNEG[3]**2+APfitNEG[3]**2))
    
  results = Analysis.AnalyseFile()
  results.add_column(MeanAlphaPos,column_header=r'$Mean\alpha^{\plus}$')
  results.add_column(errMeanAlphaPos,column_header=r'err$Mean\alpha^{\plus}$')
  results.add_column(MeanAlphaNeg,column_header=r'$Mean\alpha^{\minus}$')
  results.add_column(errMeanAlphaNeg,column_header=r'$Mean\alpha^{\minus}$')
  results.add_column(T,column_header=r'Temperature (K)')
  results.sort('Temp')
  

  p=SP.PlotFile(results)
  print p.column_headers
  p.setas="yeyex"
  p.template=SPF.JTBPlotStyle
  label = None
  title = ' '
  #p.plot_xy('Temp',[r'$\Delta\alpha^{\plus}$',r'$\Delta\alpha^{\minus}$'],label = label,title=title,figure=2)
  p.plot(label = label,title=title,figure=2)
  p['Sample ID'] = ID
  
  return p



def Beta_vs_T_PandN_Current(folder):
  ''' Function to fit  NLIV at each temperature and plot Alpha for posative and negative currents. '''
    
  folder.group('IVtemp')
  folder.sort('IVtemp')
  APiterator = [5,10]
  
  T=[]
  AlphaPosP=[]
  AlphaPosAP=[]
  AlphaNegP=[]
  AlphaNegAP=[]
  AlphaPosPerr=[]
  AlphaPosAPerr=[]
  AlphaNegPerr=[]
  AlphaNegAPerr=[] 
  
  
  for key in folder.groups.keys():
      
    AP = Analysis.AnalyseFile()
    P = Analysis.AnalyseFile()
    tsum = 0.0
    
    for f in folder.groups[key]:
      if f['iterator'] in APiterator:
        AP.add_column(f.column('Voltage'),str(f['iterator']))
      else:
        P.add_column(f.column('Voltage'),str(f['iterator']))
      tsum = tsum + f['Sample Temp']
      
    AP.apply(avg,0,replace=False,header='Mean NLV')
    AP.add_column(f.Current,column_header = 'Current')
    P.apply(avg,0,replace=False,header='Mean NLV')
    P.add_column(f.Current,column_header = 'Current')
    
    APfitPOS = AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x>0,result=True,header='Fit',asrow=True)
    APfitNEG = AP.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x<0,result=True,header='Fit',asrow=True)
    PfitPOS = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x>0,result=True,header='Fit',asrow=True)
    PfitNEG = P.curve_fit(quad,'Current','Mean NLV',bounds=lambda x,y:x<0,result=True,header='Fit',asrow=True)
    
    
    T.append(tsum/len(folder.groups[key]))
    AlphaPosP.append(PfitPOS[0])
    AlphaPosAP.append(APfitPOS[0])
    AlphaNegP.append(PfitNEG[0])
    AlphaNegAP.append(APfitNEG[0])
    AlphaPosPerr.append(PfitPOS[1])
    AlphaPosAPerr.append(APfitPOS[1])
    AlphaNegPerr.append(PfitNEG[1])
    AlphaNegAPerr.append(APfitNEG[1])
    
  results = Analysis.AnalyseFile()
  results.add_column(AlphaPosP,column_header=r'$\alpha_{P}^{\plus}$')
  results.add_column(AlphaPosPerr,column_header=r'err$\alpha_{P}^{\plus}$')
  results.add_column(AlphaPosAP,column_header=r'$\alpha_{AP}^{\plus}$')
  results.add_column(AlphaPosAPerr,column_header=r'err$\alpha_{AP}^{\plus}$')
  results.add_column(AlphaNegP,column_header=r'$\alpha_{P}^{\minus}$')
  results.add_column(AlphaNegPerr,column_header=r'err$\alpha_{P}^{\minus}$')
  results.add_column(AlphaNegAP,column_header=r'$\alpha_{AP}^{\minus}$')
  results.add_column(AlphaNegAPerr,column_header=r'err$\alpha_{AP}^{\minus}$')
  results.add_column(T,column_header=r'Temperature (K)')
  results.sort('Temp')
  
  results.subtract(r'$\alpha_{P}^{\plus}$',r'$\alpha_{P}^{\minus}$',header=r'$\alpha_{P}^{diff}$',replace=False)
  results.add_column(numpy.sqrt(results.column(r'err$\alpha_{P}^{\plus}$')**2+results.column(r'err$\alpha_{P}^{\minus}$')**2),column_header=r'err$\alpha_{P}^{diff}$')
  results.subtract(r'$\alpha_{AP}^{\plus}$',r'$\alpha_{AP}^{\minus}$',header=r'$\alpha_{AP}^{diff}$',replace=False)
  results.add_column(numpy.sqrt(results.column(r'err$\alpha_{AP}^{\plus}$')**2+results.column(r'err$\alpha_{AP}^{\minus}$')**2),column_header=r'err$\alpha_{AP}^{diff}$')
  
  

  p=SP.PlotFile(results)
  print p.column_headers
  #p.setas="y.........xe."
  p.template=SPF.JTBPlotStyle
  label = r'$\alpha_{P}^{diff}$'
  title = ' '
  #p.plot(label = label,title=title,figure=2)  
  p.plot_xy('Temp',[r'$\alpha_{P}^{\plus}$',r'$\alpha_{AP}^{\plus}$',r'$\alpha_{P}^{\minus}$',r'$\alpha_{AP}^{\minus}$'],label = label,title=title,figure=2)
  #p.plot_xy('Temp',[r'$\alpha_{P}^{diff}$',r'$\alpha_{AP}^{diff}$'],label = label,title=title,figure=2)
  return p

############ IMPORT DATA #############

pattern = re.compile('_(?P<state>\d*)_(?P<IVtemp>\d*)K_(?P<Inj>\w*)_NLIV_300uA_')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_2_T/NLIVvsHvsT_Py_Inj',pattern = pattern)


########## PICK FUNCTION TO APPLY TO DATA ###############

Beta_vs_T_PandN_Current(folder)
#Alpha_vs_T_PandN_Current(folder)
#Delta_Alpha_vs_T_PandN_Current(folder)
#p = Mean_Alpha_vs_T_PandN_Current(folder)
#Delta_Alpha_vs_T(folder)


#p.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Current_Polarity_Analysis/MeanRsvsT/'+ p['Sample ID'] +'_MeanRs_pnCurrent.txt')




