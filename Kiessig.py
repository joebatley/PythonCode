 # A very quick and dirty Kiessig Fringe Analysis code
 # Gavin Burnell 28/12/2010
 # $log$
 #
 # TODO: Imp,ement an error bar on the uncertainity by understanding the significance of the covariance terms
 
import Stoner
import numpy as np
import matplotlib.pyplot as pyplot

filename=False
sensitivity=100

critical_edge=0.8
<<<<<<< HEAD

d=Stoner.AnalyseFile(Stoner.XRDFile(filename)) #Load the low angle scan
=======
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e

#d=Stoner.AnalyseFile(Stoner.XRDFile(filename)) #Load the low angle scan
d=Stoner.AnalyseFile(Stoner.CSVFile(filename,37,37,',',','))
#Now get the section of the data file that has the peak positions
# This is really doing the hard work
# We differentiate the data using a Savitsky-Golay filter with a 5 point window fitting quartics.
# This has proved most succesful for me looking at some MdV data.
# We then threshold for zero crossing of the derivative
# And check the second derivative to see whether we like the peak as signficant. This is the significance parameter
# and seems to be largely empirical
# Finally we interpolate back to the complete data set to make sure we get the angle as well as the counts.
d.add_column(lambda x:np.log(x[1]), 'log(Counts)')
<<<<<<< HEAD
t=Stoner.AnalyseFile(d.interpolate(d.peaks('Counts',4,sensitivity,poly=4)))
=======
t=Stoner.AnalyseFile(d.interpolate(d.peaks(1,4,sensitivity,poly=4)))
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e
t.del_rows(0, lambda x,y: x<critical_edge)
p2=Stoner.PlotFile(t.clone)
pp=p2.plot_xy(0, 1, 'ro',  plotter=pyplot.semilogy, figure=None,ms=10)
p1=Stoner.PlotFile(d.clone)
<<<<<<< HEAD
p1.plot_xy(0, 1, figure=p2.fig, plotter=pyplot.semilogy,title='Reflectivity of V (TF=3, Target = 30 nm)')
=======
p1.plot_xy(0, 1, figure=p2.fig, plotter=pyplot.semilogy,title='Reflectivity of Cu (Kcell), SlimShady Calib')
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e
p1.show()
#Now convert the angle to sin^2
t.apply(lambda x: np.sin((x[0]/2)*(np.pi/180))**2, 0)
# Now create the m^2 order
m=np.arange(len(t))+1
m=m**2
#And add it to t
t.add_column(m, 'm^2')
#Now we can it a straight line
def linear(x, m, c):
    return m*x+c
p, pcov=t.curve_fit(linear, 'm^2', 0)
<<<<<<< HEAD
perr=Stoner.cov2corr(pcov)
print pcov
#Get the square root of the gradient of the line
g=np.sqrt(p[0])
#gerr=.5*(1-perr[0, 0])
x=np.sqrt(pcov[0,0])
gerr = (x*0.5)/(p[0]**.5)
=======
perr=np.sqrt(pcov)
print perr
#Get the square root of the gradient of the line
g=np.sqrt(p[0])
gerr=.5*(1-perr[0, 0])
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e
# Get the wavelength from the metadata
l=float(d['Lambda'])
print l
print g,  gerr
# Calculate thickness and report
th=l/(2*g)
therr=th*(gerr)
print "Thickness is:"+str(th)+"+-"+str(therr)+"Angstroms - please round correctly before telling Bryan"

t.add_column(lambda x:linear(x[3], p[0], p[1]))
<<<<<<< HEAD
t.column_headers=['sin$^2$(theta)', 'Counts','log(Counts)', 'm$^2$', 'fit']
#print t

=======
t.column_headers=['sin^s(theta)', 1,'log(Counts)', 'm^2', 'fit']
>>>>>>> 06a0d462a8c55800620358997e4eca37608b599e
t=Stoner.PlotFile(t)
print t.fit
pyplot.axes([0.5, 0.6, 0.35, 0.25])
t.plot_xy(0, 3, 'ro', figure=p2.fig,title="Thickness is: "+str.format("{0:.0f}", th)+" A")
t.plot_xy('fit', 3, 'b-', figure=p2.fig)
t.show()

