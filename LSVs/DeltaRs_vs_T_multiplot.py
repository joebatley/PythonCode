"""

File to plot \Delta R_s as a function of T for multipul seperations on one graph

"""

import numpy
import Stoner.Analysis as Analysis
import matplotlib.pyplot as plt # pylab imports numpy namespace as well, use pyplot in scripts
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
from Stoner.Folders import DataFolder


class workfile(Analysis.AnalyseFile,SP.PlotFile):
    """A class that combines AnalyseFile and PlotFile together"""
    pass

####### Define seperation lengths for labels######
<<<<<<< HEAD
sc004 = {1:'325 nm',2:'425 nm',3:'525 nm',4:'625 nm', 5:'725 nm', 6:'925 nm',7:'1125 nm', 8:'1325 nm', 9:'1525 nm',} 
=======
<<<<<<< HEAD
sc004 = {1:'325 nm',2:'425 nm',3:'525 nm',4:'625 nm', 5:'725 nm', 6:'925 nm',7:'1125 nm', 8:'1325 nm', 9:'1525 nm',} 
=======
sc004 = {1:325e-9,2:425e-9,3:525e-9,4:625e-9, 5:725e-9, 6:925e-9,7:1125e-9, 8:1325e-9, 9:1525e-9,} 
>>>>>>> FETCH_HEAD
>>>>>>> FETCH_HEAD
sc020 = {'1A':300e-9,'1B':400e-9,'2A':500e-9,'2B':600e-9,'3A':700e-9,'3B':800e-9,'5A':1200e-9,'5B':1400e-9,}
       
              
####### IMPORT DATA ######
<<<<<<< HEAD
FileDir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaRvsT/'
=======
<<<<<<< HEAD
FileDir = '/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/DeltaRvsT/'
=======
FileDir = '/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/DeltaRvsT/'
>>>>>>> FETCH_HEAD
>>>>>>> FETCH_HEAD
pattern = '*DeltaRsvsT.txt'
folder = DataFolder(FileDir,pattern = pattern,type=workfile)
folder.sort()


####### Iterate through files ######
for f in folder:
  f.template=SPF.JTBPlotStyle
  ID = f['Sample ID'].split('_')
  #f.divide('DR mV',f.max('DR mV')[0],replace=False,header='DRnorm')
  f.labels=[r'T (K)',r'$R_s(P)$ (mV/A)','Perr',r'$R_s(AP)$ (mV/A)','APerr',r'$\Delta R_s$ (mV/A)','DRerr mV',r'$R_s$ offset (mV/A)',"Test Columns"] 
  #f.plot_xy('T','Voff',label=Seperation[ID[1]+ID[2]],title=ID[0],linestyle='--',marker='o')
  if ID[0]=='SC004':
<<<<<<< HEAD
      f.plot_xy('T','DR mV',label=sc004[int(ID[1])],figure=1,title=ID[0],linestyle='',marker='o')
  else:
      f.plot_xy('T','DR mV',label=sc020[ID[1]+ID[2]],figure=1,title=ID[0],linestyle='',marker='o')
=======
<<<<<<< HEAD
      f.plot_xy('T','DR mV',label=sc004[int(ID[1])],figure=1,title=ID[0],linestyle='',marker='o')
  else:
      f.plot_xy('T','DR mV',label=sc020[ID[1]+ID[2]],figure=1,title=ID[0],linestyle='',marker='o')
=======
      f.plot_xy('T','DR mV',label=sc004[int(ID[1])],figure=1,title=ID[0],linestyle='--',marker='o')
  else:
      f.plot_xy('T','DR mV',label=sc020[ID[1]+ID[2]],figure=1,title=ID[0],linestyle='--',marker='o')
>>>>>>> FETCH_HEAD
>>>>>>> FETCH_HEAD
