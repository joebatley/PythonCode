

import numpy
from Stoner.Folders import DataFolder
import pylab as plt
import re
 
fig_width_pt = 700.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
params = {'backend': 'ps',
          'axes.labelsize': 42,
          #'axes.color_cycle':['b','r','k','g','p','c'],
          #'axes.formatter.limits' : [-7, 7],
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


####### IMPORT DATA ######


pattern = re.compile('_(?P<Width>\d*).0nm')
folder = DataFolder('/Users/Joe/Desktop/untitled folder/',pattern = pattern)

InvrsA = numpy.zeros(len(folder))
HTRes = numpy.zeros(len(folder))
LTRes = numpy.zeros(len(folder))
i=0



plt.hold(True)
for f in folder:
    #if f['Width']==400:
    #    f['Width']=250
    Area = (float(f['Width'])*1e-9)**2 
    
    HighTempR = numpy.mean(f.search('temperature',lambda x,y: x>275 and x<285,'Resistance'))
    if HighTempR<0:
        HighTempR = -HighTempR
    HighTempRerr = numpy.std(f.search('temperature',lambda x,y: x>275 and x<285,'Resistance'))#/len(f.search('temperature',lambda x,y: x>275 and x<285,'Resistance'))
    
    LowTempR = numpy.mean(f.search('temperature',lambda x,y: x>10 and x<20,'Resistance'))
    if LowTempR<0:
        LowTempR = -LowTempR
    LowTempRerr = numpy.std(f.search('temperature',lambda x,y: x>10 and x<20,'Resistance'))#/len(f.search('temperature',lambda x,y: x>10 and x<20,'Resistance'))
 
    HRA = HighTempR/(((float(f['Width']))*1e-9)*((float(f['Width']))*1e-9))
    LRA = LowTempR/(((float(f['Width']))*1e-9)*((float(f['Width']))*1e-9))
    
     
    if f['Width']==150:
        InvrsA[i] = 0.0      
        HTRes[i] = 0.0
        LTRes[i] = 0.0
    else:
        InvrsA[i] = 1/Area      
        HTRes[i] = HighTempR
        LTRes[i] = LowTempR 
    print f['Width'], Area, InvrsA[i]          
    i=i+1
                         
    plt.title('')
    plt.xlabel(r'1/Area (m$^{-2}$)')
    plt.ylabel(r'Interface Resistance ($\Omega$)')
    #plt.ticklabel_format(style = 'sci', useOffset = False)
    plt.tick_params(axis='both', which='minor')
    
    #plt.errorbar(f['Width'],LowTempR,LowTempRerr,ecolor='k',marker='o',mfc='blue', mec='black')
    #plt.errorbar(f['Width'],HighTempR,HighTempRerr,ecolor='k',marker='o',mfc='red', mec='black')

    plt.plot(1/Area,HighTempR,'or')
    plt.plot(1/Area,LowTempR,'ob')
    #plt.plot(f['Width'],HRA,'or')
    #plt.plot(f['Width'],LRA,'ob')
    
    '''
    if f.column('Resistance')[0]<0:
        plt.plot(f.column('temp'),-f.column('Resistance'),'-o',label=f['Width'])
    else:
        plt.plot(f.column('temp'),f.column('Resistance'),'-o',label=f['Width'])
   '''
   
pH = numpy.polyfit(InvrsA,HTRes,1)
fitH = pH[1]+pH[0]*InvrsA
print pH[0]
plt.plot(InvrsA,fitH,'k',label='RA = ' + "%g" % round(pH[0]*1e12, 3) + r' $\Omega\mu$m$^2$') 




pL ,pLV= numpy.polyfit(InvrsA,LTRes,1,cov=True)
fitL = pL[1]+pL[0]*InvrsA
print pL[0],numpy.sqrt(pLV[0,0])
plt.plot(InvrsA,fitL,'g',label='RA = ' + "%g" % round(pL[0]*1e12, 3) +r' $\Omega\mu$m$^2$')
   
plt.legend(loc=2)
plt.show()



