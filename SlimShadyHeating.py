
import numpy
import Stoner
import Stoner.Analysis as Analysis
import pylab as plt

 

fig_width_pt = 700.0 # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (numpy.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]
 
params = {'backend': 'ps',
          'axes.labelsize': 36,
          'text.fontsize': 36,
          'legend.fontsize': 24,
          'xtick.labelsize': 28,
          'ytick.labelsize': 28,
          'xtick.direction': 'in',
          'ytick.direction': 'in',
          'xtick.major.size':10,
          'ytick.major.size':10,
          'figure.figsize': fig_size,
         'font.family':'Arial',
         'xtick.major.pad':20,
         'ytick.major.pad':20,
         'font.size':32,
         'lines.linewidth':4}
 
plt.rcParams.update(params)

######## Import Heating Curve #########  
heating = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Slim Shady/Heating/Heating.txt',1,2,',',',')
#heating1 = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Slim Shady/Heating/Heating_wBraid.txt',1,2,',',',')
heating = Analysis.AnalyseFile(heating)
#heating1 = Analysis.AnalyseFile(heating1)

######## Convert to Kelvin #########
heating.add(1,272.0,replace=True,header = 'Temp')
#heating1.add(1,272.0,replace=True,header = 'Temp')
######## Define Heating function #########
def heat(x,a,b,c):
    return b*(1.0-numpy.exp(a*x)) +c

######## Fit Data #########
fitH,fitVaHr= heating.curve_fit(heat,'Time','Temp',p0=[-0.1,50.0,300.0])#,bounds=lambda x, y:x<240)
#fitH2,fitVaHr2= heating.curve_fit(heat,'Time','Temp',p0=[-0.0001,20.0,300.0],bounds=lambda x, y:x>240)
#print fitH


######## Create Fit Curve to Plot #########
SimH = fitH[1]*(1.0-numpy.exp(fitH[0]*heating.column(0)))+fitH[2]

#heat1 = heating.search('Time',lambda x,y: x<2400000,'Time')
#SimH = fitH[1]*(1.0-numpy.exp(fitH[0]*heating.column('Time')))+fitH[2]
#heat2 = heating.search('Time',lambda x,y: x>240)# and x<22.0*60.0,'Time')
#SimH2 = fitH2[1]*(1.0-numpy.exp(fitH2[0]*heat2))+fitH2[2]


###### Power changes #######
'''
P1 = numpy.zeros(len(heating.column(1))) + 3.5*60.0
plt.plot(P1,heating.column(1))
P2 = numpy.zeros(len(heating.column(1))) + 4.5*60.0
plt.plot(P2,heating.column(1))
P3 = numpy.zeros(len(heating.column(1))) + 7.0*60.0
plt.plot(P3,heating.column(1))
P4 = numpy.zeros(len(heating.column(1))) + 22.0*60.0
plt.plot(P4,heating.column(1))
'''

######### unit multiplications ########
alpha = 1
beta = 1

######### Plot Heating ##########
plt.title('')
plt.hold(True)
plt.xlabel(r'Time (s)')
plt.ylabel(r'Temperature (K)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.plot(heating.column(0),heating.column(1),'--or')
#plt.plot(heating1.column(0),heating1.column(1),'--xr')
plt.plot(heating.column(0),SimH,'k',label = r'$\tau_h$ = ' + str(-1.0/fitH[0]))
#plt.plot(heating.column(0),SimH,'b',label = r'$\tau_h$ = ' + str(-1.0/fitH[0]))
#plt.plot(heat2,SimH2,'k',label = r'$\tau_h$ = ' + str(-1.0/fitH2[0]))





######## Import Cooling Curve #########  
cooling = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Slim Shady/Heating/Cooling.txt',1,2,',',',')
#cooling1 = Stoner.CSVFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Slim Shady/Heating/Cooling_wBraid.txt',1,2,',',',')
cooling = Analysis.AnalyseFile(cooling)
#cooling1 = Analysis.AnalyseFile(cooling1)
######## Convert to Kelvin #########

cooling.add(1,272.0,replace=True,header = 'Temp')
#cooling.add(0,max(heating.column(0)),replace=True,header = 'Time')
#cooling1.add(1,272.0,replace=True,header = 'Temp')
#cooling1.add(0,max(heating1.column(0)),replace=True,header = 'Time')



######## Define Cooling function #########
def cool(x,a,b,c):
    return b*numpy.exp(a*x)+c
    
######## Fit Data #########    
fitC,fitVarC= cooling.curve_fit(cool,'Time','Temp',p0=[-0.01,300.0,300.0])
print fitC

######## Create Fit Curve to Plot #########
SimC = (fitC[1]*numpy.exp(fitC[0]*cooling.column('Time')))+fitC[2]

######### unit multiplications ########
alpha = 1
beta = 1

######### Plot Cooling ##########
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.plot((cooling.column(0)+max(heating.column(0))),cooling.column(1),'--ob')
#plt.plot(cooling1.column(0),cooling1.column(1)/cooling1.column(1).max(),'--xb')
plt.plot((cooling.column(0)+max(heating.column(0))),SimC,'g',label = r'$\tau_c$ = ' + str(-1.0/fitC[0]))
plt.legend().draggable()


plt.show()
