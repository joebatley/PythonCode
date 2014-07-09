

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
RS.del_rows(0)
RS.sort('T (K)')


p=SP.PlotFile(RS)
print p.column_headers
p.template=SPF.JTBPlotStyle
label = str(p['Sample ID'])
title = ' '
p.plot_xy('T (K)',r'$\Delta R_s$ (V/A)',plotter=plt.errorbar,yerr='DRerr',label = label,title=title,figure=2)






