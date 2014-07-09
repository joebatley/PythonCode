import re
import numpy
from scipy import interpolate
import pylab as plt
import Stoner
from Stoner.Folders import DataFolder
import Stoner.Analysis as Analysis
import scipy.optimize


'''
pattern = re.compile('_(?P<state>\d*)_(?P<IVtemp>\d*)K_(?P<Inj>\w*)_NLIV_300uA_')
folder = DataFolder('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/NLIVvsHvsT_BOTH',pattern = pattern)
folder.group(['Inj','IVtemp'])
print folder


def something(folder,keys):
'''

file1 = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/NLIVvsHvsT_BOTH/SC004_3_T_6221-2182 DC IV_Magnet Power Supply Multi-segment_1_25K_Py_NLIV_300uA_.txt')  
file2 = Stoner.DataFile('/Volumes/data/Projects/Spincurrents/Joe Batley/Measurements/SC004/Transport/SC004_3_T/NLIVvsHvsT_BOTH/SC004_3_T_6221-2182 DC IV_Magnet Power Supply Multi-segment_1_25K_V_NLIV_300uA_.txt')


#plt.plot(file1.Current,((file1.Voltage-file1.Voltage[0])/48.0))
#plt.plot(file1.Current,((file2.Voltage-file2.Voltage[0])/420.0))
plt.plot(file1.Current,((file1.Voltage-file1.Voltage[0])/48.0)-((file2.Voltage-file2.Voltage[0])/420.0))
plt.show()