

import numpy
import re
import Stoner
import Stoner.Analysis as Analysis
import pylab as plt
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
 


####### IMPORT DATA ######


RS=Analysis.AnalyseFile(False)
print RS[0]
#RS.del_rows(0)
#RS.sort('T (K)')



p=SP.PlotFile(RS)
print p.column_headers
p.template=SPF.JTBPlotStyle
label = 'Py/Co/Cu'
title = ' '
p.plot_xy('T',r'DR mV',plotter=plt.errorbar,yerr='DRerr',label = label,title=title,figure=2)
p.ylabel = r'$\Delta R_s$ (mV/A)'
p.xlabel = 'T (K)'




