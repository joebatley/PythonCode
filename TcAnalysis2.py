# -*- coding: utf-8 -*-
"""
Created on Tue Oct 08 12:57:28 2013

@author: py08ns
"""

from numpy import sqrt,log10,floor
import Stoner
from Stoner.Util import split_up_down
from Stoner.FittingFuncs import Linear


class mydata(Stoner.AnalyseFile, Stoner.PlotFile):
    def find_tc(self):
            self.normalise('esistance',self.max('esistance')[0],header='Normalised Data',replace=True)
            
            self.subtract('Normalised Data', 0.5, header='Normalised Data', replace=True)
            
            self.del_rows('Normalised Data',lambda x,y: abs(x)>0.4)
            
            fit, fitVar= self.curve_fit(Linear,ycol='emperature',xcol='Normalised Data')
            err=sqrt(fitVar[1,1])
            errPower=floor(log10(err))
            err=round(err/10**errPower)*10**errPower # 1 dp in error
            tc=fit[1]
            tc=round(tc/10**errPower)*10**errPower
            return tc,err
        

####### IMPORT DATA ######
#file = Stoner.DataFile('C:\Users\py08ns\Desktop\NSatP30mT_1') 
a = mydata('C:/Users/py08ns/Desktop/CoFeSiMgONb/PSatP60mT_1')
####### Delete first (bad) datapoint #####
a.del_rows(0)

#b=a.clone

###### Analyse a ######
updown=split_up_down(a,'temperature')

for a in updown["rising"][0],updown["falling"][0]:
    fit=a.find_tc()
    print fit
    a.plot_xy('emperature', 'Normalised Data')

