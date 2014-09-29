"""
Code to plot Rs vs H from NLIV vs H data.

Assumes file name format 

<Sample ID>_6221-2182 DC IV_Magnet Power Supply Multi-segment_<Iterator>_<Temp>K_<Injector Mat>_NLIV_<Max Current>uA_.txt

e.g. SC004_5_B_6221-2182 DC IV_Magnet Power Supply Multi-segment_1_200K_Py_NLIV_300uA_.txt

@author: py07jtb
"""

from numpy import *
import re
import Stoner.Analysis as Analysis
import matplotlib.pyplot as plt # pylab imports numpy namespace as well, use pyplot in scripts
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
from Stoner.Folders import DataFolder
from lmfit import minimize, Parameters, Parameter, report_fit

class workfile(Analysis.AnalyseFile,SP.PlotFile):
    """A class that combines AnalyseFile and PlotFile together"""
    pass
 
def quad(x,a,b,c,d,e):
  return (a*x**2)+(b*x)+c+(d*x**4)+(e*x**3)

pattern = '*NLIV.txt'
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/SC020_5_B/6221-2182 DC IV/', pattern = pattern,type=workfile) 

print folder
print folder.groups.keys()


output = workfile()
output.metadata=folder['10K-IV_Data'][0].metadata
output['Sample ID'] = folder['10K-IV_Data'][0]['Sample ID']
output.column_headers=["T","P","P.err","AP","AP.err","DR","DR.err","beta","beta.err","quad","quad.err",'tri','tri.err']
#Use the labels attribute to store plot labels that are differnt from column names
output.labels=[r'T (K)',r'$R_s(P)$ (V/A)','Perr',r'$R_s(AP)$ (V/A)','APerr',r'$\Delta R_s$ (V/A)','DRerr ',r"\beta","beta_err",r"x^4","x^4 err",r"x^3","x^3 err"]



############ Calculate Delta R with error ############


for i in folder.groups.keys():
    Rs = []
    p = []
    ap = []
    beta = []
    Q = []
    tri = []
    for f in folder.groups[i]:
        fit = f.curve_fit(quad,'Current','Voltage',p0=[20.0,1e-7,0.0,1,1], result=True, replace=False, header="fit",asrow=True)
        Rs.append(fit[2])
        beta.append(fit[0])
        Q.append(fit[6])
        tri.append(fit[8])
    avg = mean(Rs)
    for i in range(len(Rs)):
        if Rs[i]>avg:
            p.append(Rs[i])
        else:
            ap.append(Rs[i])
    
    P = mean(p)
    Perr = std(p)/len(p)
    AP = mean(ap)
    APerr = std(ap)/len(ap)
    DR = P-AP
    DRerr = sqrt(Perr**2+APerr**2)
    Beta = mean(beta)
    Betaerr = std(beta)/len(beta)
    q = mean(Q)
    qerr = std(Q)/len(Q)
    t = mean(tri)
    terr = std(tri)/len(tri)
    row=numpy.array([f['Sample Temp'],P,Perr,AP,APerr,DR,DRerr,Beta,Betaerr,q,qerr,t,terr])
    output+=row        
        



################ plot Data ##################


output.template=SPF.JTBPlotStyle
output.figure() # Creating new figures like this means we don;t reuse windows from run to run
f=plt.gcf()
f.set_size_inches((11,7.5),forward=True) # Set for A4 - will make wrapper for this someday


output.sort('T')
output.title = ''
output.subplot(221)
output.plot_xy("T","P",yerr='P.err',label = 'P',linestyle='',marker='o',markersize=5,linewidth=1)
output.plot_xy("T","AP",yerr='AP.err',label = 'AP',linestyle='',marker='o',markersize=5,linewidth=1)
output.ylabel=r"R$_s$ (V/A)"
output.xlabel=r'T (K)'
output.subplot(222)
output.plot_xy("T","beta",yerr='beta.err',label = None,linestyle='',marker='o',markersize=5,linewidth=1)
output.ylabel=r"$\beta$ (V/A$^2$)"
output.xlabel=r'T (K)'
output.subplot(223)
output.plot_xy("T","tri",yerr='tri.err',label = None,linestyle='',marker='o',markersize=5,linewidth=1)
output.ylabel=r"I$^3$ Coef (V/A$^3$)"
output.xlabel=r'T (K)'
output.subplot(224) 
output.plot_xy("T","quad",yerr='quad.err',label = None,linestyle='',marker='o',markersize=5,linewidth=1)
output.ylabel=r"I$^4$ Coef (V/A$^4$)"
output.xlabel=r'T (K)'
plt.legend(loc='best')
plt.tight_layout()


output.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC020/Transport/Polyfit Analysis/'+output['Sample ID']+'_NLIV_Polyfit_vs_T.txt')
















