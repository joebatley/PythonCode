#from scipy import *
from scipy import interpolate
import Stoner.Analysis as Analysis
import pylab as plt
import numpy
import Stoner

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


### IMPORT DATA ###

a=Analysis.AnalyseFile('/Volumes/data-1/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/NLDCRvsTat60&-30mT/6221-2182 DC IV Timed interval 0000_RvsT_60mT.txt')   #import a single data file ready to use the Analysis class
b=Analysis.AnalyseFile('/Volumes/data-1/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/NLDCRvsTat60&-30mT/6221-2182 DC IV Timed interval 0000_RvsT_-30mT!0002.txt')



###arrange###
a.sort('Sample Temp')
b.sort('Sample Temp')


fit_a = a.polyfit('Sample Temp','Res',5)
curve_a = fit_a[0]*a.column('Temp')**5 + fit_a[1]*a.column('Temp')**4 + fit_a[2]*a.column('Temp')**3 + fit_a[3]*a.column('Temp')**2 +fit_a[4]*a.column('Temp') + fit_a[5]


fit_b = b.polyfit('Sample Temp','Res',5)
curve_b = fit_b[0]*b.column('Temp')**5 + fit_b[1]*b.column('Temp')**4 + fit_b[2]*b.column('Temp')**3 + fit_b[3]*b.column('Temp')**2 +fit_b[4]*b.column('Temp') + fit_b[5]
#plt.hist((b.column('Res')-curve_b)*100,50)
#plt.show()


bin=10

sdev_a = numpy.zeros(len(a.column('Res'))/bin) 
Res_a = numpy.zeros(len(a.column('Res'))/bin)
Temp_a = numpy.zeros(len(a.column('Res'))/bin)

for i in range(0,len(a.column('Res')),bin):
    if i<(len(a.column('Res'))/bin)*bin:
        tot = 0.0
        for j in range(0,bin):
            tot = tot + a.column('Res')[i+j]
        Res_a[i/bin] = tot/bin   
        Temp_a[i/bin] = ((a.column('Temp')[i]-a.column('Temp')[i+bin-1])/2)+a.column('Temp')[i+bin-1]
        sdev=0
        for p in range(0,bin):
            sdev = sdev + (a.column('Res')[i+j]-Res_a[i/bin])**2
        sdev_a[i/bin] = numpy.sqrt(sdev)/bin        
        
        
sdev_b = numpy.zeros(len(b.column('Res'))/bin)        
Res_b = numpy.zeros(len(b.column('Res'))/bin)
Temp_b = numpy.zeros(len(b.column('Res'))/bin)

for i in range(0,len(b.column('Res')),bin):
    if i<(len(b.column('Res'))/bin)*bin:
        tot = 0.0
        for j in range(0,bin):
            tot = tot + b.column('Res')[i+j]
            
            
        Res_b[i/bin] = tot/bin   
        Temp_b[i/bin] = ((b.column('Temp')[i]-b.column('Temp')[i+bin-1])/2)+b.column('Temp')[i+bin-1]
        sdev=0
        for p in range(0,bin):
            sdev = sdev + (b.column('Res')[i+j]-Res_b[i/bin])**2
        sdev_b[i/bin] = numpy.sqrt(sdev)/bin         
                        
                                        
###interpolate###
#binter.data=b.interpolate(a.column('Sample Temp'),'linear',3)
aResnew = numpy.interp(Temp_b,Temp_a,Res_a)
###calculation###

deltaR=aResnew-Res_b # soustraction
offset = Temp_b+(deltaR/2)

#DRerr = numpy.sqrt((sdev_a*sdev_a)+(sdev_b*sdev_b))
#print (deltaR) 

#binter.add_column(deltaR,'DeltaR')

##################### FIT ################################

CuR = Analysis.AnalyseFile('/Volumes/data-1/Projects/Spincurrents/Joe Batley/Measurements/RN0151/Transport/RN0151_4T/RN0151_4T_6221-2182 DC IV_Timed interval_0000_1.75_Cuspacer_RvT.txt')
PyR = Stoner.CSVFile('/Volumes/data-1/Projects/Spincurrents/Mike Batley/RN0095/Dip Probe/RN0095_1_res.txt',1,2,',',',')

NewCuR = interpolate.interp1d(CuR.column('Temp'),CuR.column('Res'))
NewPyR = interpolate.interp1d(PyR.column('Temp'),PyR.column('Res'))
LambdaF = 5e-9
Af = 1e-14
An = 5e-13
Pf = 0.35

def Rs(x,a)
  ((4*Pf*Pf)/(1-(Pf*Pf))**2)*((NewPyR(x)*LambdaF*An)/(NewCuR(x)*a*))


###Plot###
plt.title(r'')
plt.xlabel('Temperature (K)')
plt.ylabel(r'R$_s$ ($\mu$V/A)')
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.hold(True)
#plt.plot(a.column('Temp'),1e6*a.column('Res'),'-or',label='Parallel')
#plt.plot(a.column('Temp'),1e6*curve_a,'-k',label='Parallel Fit')
#plt.plot(Temp_b,1e6*aResnew,'-or',label='Parallel')
#plt.plot(b.column('Temp'),1e6*b.column('Res'),'-ob',label='Antiparallel')
#plt.plot(b.column('Temp'),1e6*curve_b,'-k',label='Antiparallel Fit')
#plt.plot(Temp_b,1e6*Res_b,'-ob',label='Antiparallel')
#plt.errorbar(Temp_b,deltaR,DRerr,ecolor='k',marker='o',mfc='blue', mec='blue')
plt.plot(Temp_b,deltaR*1e6,'-ob')

#plt.legend(loc=2)
plt.show()

