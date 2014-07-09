import re
import numpy
from scipy import interpolate
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import Stoner.Plot as plot
 
fig_width_pt = 1000.0 # Get this from LaTeX using \showthe\columnwidth
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


KcuT = numpy.array([[0.000000,0.000000],
[0.382157,28.619795],
[1.528139,124.002874],
[3.626817,343.315756],
[9.738884,848.850946],
[15.472227,1259.100486],
[20.065475,1459.682625],
[23.322399,1536.286247],
[26.391433,1536.675963],
[29.270123,1508.470242],
[34.070394,1413.842238],
[41.950001,1119.606386],
[48.866119,910.961990],
[56.354247,769.056521],
[64.225023,646.247153],
[74.780223,542.826174],
[89.552890,487.559523],
[100.871424,460.425522],
[112.188976,452.338907],
[132.522305,435.873391],
[149.401990,438.016831],
[158.033647,439.112908]])


KsiT = numpy.array([[0.000000,0.000000],
[10.870843,0.125540],
[18.141268,0.142927],
[25.408667,0.168962],
[31.943880,0.207962],
[37.752959,0.242628],
[45.009768,0.298934],
[53.720360,0.359582],
[68.964653,0.463554],
[84.933567,0.576184],
[99.450212,0.680147],
[113.246773,0.762479],
[129.952412,0.849172],
[144.479647,0.922865],
[163.371254,1.000936],
[178.630674,1.061665],
[197.525307,1.131088],
[223.696415,1.200600],
[244.777016,1.261401],
[267.314425,1.317896],
[292.765450,1.365778],
[315.308910,1.404975],
[336.400100,1.435506],
[350.947001,1.452983]])


KpyT = numpy.array([[0.000000,0.000000],
[3.958429,0.028413*100],
[6.229083,0.044313*100],
[11.525169,0.081001*100],
[18.936559,0.131795*100],
[28.847812,0.197021*100],
[40.738735,0.262104*100],
[56.292526,0.330660*100],
[71.336817,0.371246*100],
[90.391287,0.408038*100],
[115.751669,0.434364*100],
[140.463192,0.452781*100],
[176.009793,0.461964*100],
[220.539335,0.466345*100],
[288.378023,0.446276*100],
[361.169300,0.413750*100],
[472.102722,0.371459*100],
[578.573822,0.330074*100],
[716.628327,0.287109*100],
[897.568718,0.269031*100]])


ScuT = numpy.array([[0.000000,0.000010],
[21.516088,0.302055],
[25.651305,0.572288],
[29.100301,0.775845],
[33.240838,1.007481],
[35.658327,1.126813],
[39.114093,1.281247],
[42.225057,1.414624],
[46.040618,1.481344],
[49.514761,1.502445],
[53.686731,1.506012],
[58.209791,1.485023],
[62.388048,1.442977],
[65.871379,1.397412],
[72.489854,1.309785],
[78.760625,1.222154],
[82.593111,1.166068],
[91.300231,1.060927],
[100.697924,0.990884],
[108.698995,0.962926],
[120.872037,0.938536],
[136.171517,0.935242],
[151.814350,0.963531],
[165.023251,0.991787],
[178.925143,1.037596],
[194.910845,1.100978],
[207.419984,1.160802],
[223.750972,1.241733],
[237.301775,1.312099],
[247.377467,1.368380]])

SpyTbulk = numpy.array([[0.000000,0.000000],
[5.336256,-0.345924],
[10.778056,-0.736119],
[16.223007,-1.301498],
[21.669533,-1.954469],
[25.155624,-2.389889],
[29.078856,-2.956379],
[33.655828,-3.609984],
[36.707930,-4.089517],
[41.068301,-4.787077],
[48.262599,-5.920533],
[53.057747,-6.617775],
[58.725600,-7.489567],
[62.214842,-8.100170],
[68.972787,-9.146351],
[78.783622,-10.715861],
[88.375494,-12.197938],
[97.750765,-13.723970],
[106.690471,-15.206523],
[113.887919,-16.515162],
[118.467254,-17.300155],
[300.467254,-20.00155]])

SpyTfilm = numpy.array([[0.0,0.0],
[79.072566,-0.387860],
[89.264971,-0.561244],
[99.463140,-0.911618],
[109.658428,-1.173497],
[115.606399,-1.348383],
[124.529798,-1.654960],
[130.482093,-1.962589],
[143.655689,-2.444653]])

CcuT = numpy.array([[0.0,0.0],
[3.649252,0.072063],
[14.728275,0.651193],
[22.210554,1.303439],
[33.368338,2.100335],
[40.903124,2.897758],
[44.788658,3.623118],
[52.349698,4.493129],
[56.392754,5.654021],
[56.839065,6.888027],
[60.960882,8.266684],
[68.653190,9.499638],
[72.827514,11.023473],
[76.870570,12.184365],
[84.615385,13.562496],
[88.632187,14.650799],
[96.245734,15.665987],
[104.095563,17.334473],
[115.358362,18.421724],
[130.217905,19.435860],
[145.077448,20.449997],
[167.182988,21.463081],
[192.832765,22.257874],
[229.404043,23.196265],
[265.870307,23.844303],
[295.064321,24.420803]])

params = {'Kcu':KcuT,'Kpy':KpyT,'Ksi':KsiT,'Scu':ScuT,'Spyb':SpyTbulk,'Ccu':CcuT,'Spy':SpyTfilm}


ThermalParams = Analysis.AnalyseFile()
ThermalParams.add_column(numpy.arange(0,110,1),'Temp')


for p in params.keys():
  NewParam = interpolate.interp1d(params[p][:,0],params[p][:,1])
  newy=NewParam(ThermalParams.column('Temp'))
  ThermalParams.add_column(newy,p)
'''
print ThermalParams
plt.title(r'Heat capacity Copper')
plt.xlabel('Temperature (K)')
plt.ylabel(r'c ()')
plt.hold(True)
plt.plot(ThermalParams.Temp,ThermalParams.Ccu,'b')
#plt.plot(ThermalParams.Temp,ThermalParams.Spyb,'r')
#plt.plot(ThermalParams.Temp,ThermalParams.Scu,'g')

plt.show()

'''
Current = numpy.arange(0,700e-6,2e-6)
R=220
<<<<<<< HEAD
Tsub = numpy.arange(1,70,1)
=======
Tsub = numpy.arange(5,110,1)
>>>>>>> 39d0635790167ad69094250b1cf7676bbe5933d7
Ti = 0
Acu = 100e-9*50e-9
Asi = 100e-9*10e-6
dz = 100e-9
dx = 500e-9
Alpha = 1

#Interpolate thermal params
interKcu = interpolate.interp1d(KcuT[:,0],KcuT[:,1])
interKsi = interpolate.interp1d(KsiT[:,0],KsiT[:,1])
interKpy = interpolate.interp1d(KpyT[:,0],KpyT[:,1])
interSpyb = interpolate.interp1d(SpyTbulk[:,0],SpyTbulk[:,1])
interSpy = interpolate.interp1d(SpyTfilm[:,0],SpyTfilm[:,1])
interScu = interpolate.interp1d(ScuT[:,0],ScuT[:,1])

def inter(Ti):
  if Ti ==0:
    Ti=Tsub
  Kcu = interKcu(Ti)
  Ksi = interKsi(Ti)
  Kpy = interKpy(Ti)
  Spyb = interSpyb(Ti)
  Spy = interSpy(Ti)
  Scu = interScu(Ti)
  return Kpy,Kcu,Ksi,Spy,Scu,Spyb



for t in Tsub:
<<<<<<< HEAD
  Ti=0
  Kcu,Ksi,Spy,Scu = inter(Ti,t)
  for i in Current:
    Kcu,Ksi,Spy,Scu = inter(Ti,t)
    denom = (Ksi*Asi/dz)+(Kcu*Acu/dx)
    Spc = -Spy+Scu
    V = Spc*Alpha*((i*i*R)/denom)  
    
    coef = (Spc*Alpha*R)/denom
    print i,V
    
  plt.hold(True)
  plt.plot(t,coef,'ro')#,marker=mk[t],color=color[t])
=======
  Kpy,Kcu,Ksi,Spy,Scu,Spyb = inter(t)
  denom = (Ksi*Asi/dz)+(Kcu*Acu/dx)
  Spc = (Scu-Spyb)/1e6
  
  A = Spc*Alpha*R/denom
  print Spc,Spy,Scu
  
  plt.hold(True)
  plt.plot(t,A,'ro',ms=10)
  
plt.title(r'Quadratic coefficiant due to heat transport ($\beta$) of '+'\n nonlocal voltage with bulk Spy.'+r' $\alpha$ = 1')
plt.xlabel('Temperature (K)')
plt.ylabel(r'$\beta$ ($\Omega$/A)')
plt.tick_params(axis='both', which='minor',direction='in',width=5,length=10)
>>>>>>> 39d0635790167ad69094250b1cf7676bbe5933d7
plt.show()

plt.savefig(filename='quadvsT_sim_bulkSpy_alpha_1.eps',bbox_inches='tight',pad_inches=0.1)


'''

colour = {1:'r',2:'b',3:'g',4:'k',5:'r',6:'b',7:'g',8:'y',9:'k'}
mk = {1:'o',2:'o',3:'o',4:'o',5:'x',6:'x',7:'x',8:'o',9:'x'}
for i in Current:
  Kpy,Kcu,Ksi,Spy,Scu,Spyb = inter(Ti)
  denom = (Ksi*Asi/dz)+(Kcu*Acu/dx)+(Kpy*Acu/dx)
  Ti = ((i*i*R)/denom) +Tsub
  
  Spc = Spy+Scu
  Spcb = Spyb+Scu
  V = Spc*Alpha*((i*i*R)/denom)  
  Vb = Spcb*Alpha*((i*i*R)/denom)  
  print Spy,Spyb,Scu,Spc
  plt.hold(True)
  plt.plot(i,V,'ro')
  #plt.plot(i,Vb,'bo')#,marker=mk[t],color=colour[t])
plt.show()
'''









