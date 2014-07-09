# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 17:34:54 2014

@author: Joe
"""


import numpy
from scipy import interpolate
from scipy.interpolate import splrep, splev
from scipy.integrate import quad
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize
from lmfit import minimize, Parameters, Parameter, report_fit
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP


filename_1 = '/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_1A/20140611/6221-2182 DC IV/SC018_1A_6221-2182 DC IV_Timed interval_0000 46.73_RvsT_B.txt'
filename_2 = '/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_1A/20140611/6221-2182 DC IV/SC018_1A_6221-2182 DC IV_Timed interval_0000 285.15_RvsT_B.txt'

a = Analysis.AnalyseFile(filename_1)
b = Analysis.AnalyseFile(filename_2)

a.del_rows(0)
b.del_rows(0)

a.del_rows('temperature',lambda x,y:x>35)
a.del_rows('esistance',lambda x,y:x<0.2493)

print len(b.data)
a.insert_rows(len(a.data),b.data)


q=SP.PlotFile(a.clone)              
q.template=SPF.JTBPlotStyle
title = None
label = ''
q.plot_xy('temperature','esistance',label=label,figure=2,title=title)

a.save('/Volumes/stonerlab.leeds.ac.uk - -storage/data/Projects/Spincurrents/Joe Batley/Measurements/SC018/Transport/Dip Probe/SC018_1A/20140611/6221-2182 DC IV/SC018_1A_6221-2182 DC IV_Timed interval_0000 Stitch_RvsT_B.txt')
