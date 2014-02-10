

import numpy
import Stoner
import Stoner.Analysis as Analysis
import pylab as plt
import Stoner.PlotFormats as SPF
import Stoner.Plot as SP
 


####### IMPORT DATA ######


#file = Stoner.CSVFile(False,1,2,',',',')
<<<<<<< HEAD
file = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Cu spacer resistance/SC004_8_T_6221-2182 DC IV_Timed interval_0_RvT_CuSpacer_100uA_.txt') 
=======
file = Stoner.DataFile('/Volumes/stonerlab.leeds.ac.uk 6/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_2_T/SC004_2_T_6221-2182 DC IV_Magnet Power Supply Multi-segment_176_281K_PyInj_DCAMR_300uA_.txt') 
>>>>>>> c83caf2dbe110d65a701c002d0b9d627254d2f47
a=Analysis.AnalyseFile(file)
print a.column_headers
 
a.del_rows(0)
<<<<<<< HEAD
a.del_rows('Temp',lambda x,y:x<1)


res = (158e-9*130e-9*a.column('Resistance'))/1380e-9
a.add_column(res,column_header ='Resistivity')
a.save('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/Reference Data/Cu spacer resistance/Resistivity/'+a['Sample ID']+'_Cu_resistivity_vs_T.txt')

#plt.title(a['Sample ID'] + ' - ' + a['Notes'])# + ' at ' + str.format("{0:.1f}",a['Sample Temp']) + ' K')
plt.xlabel('T (K)',labelpad=15)
plt.ylabel(r'R ($\Omega$)',labelpad=15)
plt.ticklabel_format(style = 'sci', useOffset = False)
plt.tick_params(axis='both', which='minor')
plt.plot(a.column('Temp'),res*1e8,'-',label = a['Sample ID'])
plt.tight_layout(pad=0.1, w_pad=0.0, h_pad=0.0)
plt.legend().draggable()
plt.show()
=======
a.rename('Resistance','R ($\Omega$)')
a.mulitply('Magnet', 1e-12, replace=True, header='$\mu_o$H (T)')

p=SP.PlotFile(a)
p.setas="..y....x"
p.template=SPF.JTBPlotStyle
p.plot(title='DC AMR Injector at 280 K')


>>>>>>> c83caf2dbe110d65a701c002d0b9d627254d2f47



