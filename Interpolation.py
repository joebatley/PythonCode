import Stoner.Analysis as Analysis
import pylab as plt
import numpy


a = Analysis.AnalyseFile(False)
a.sort('emp')
b = Analysis.AnalyseFile(False)
b.sort('emp')




a.data = a.interpolate(b.column('emp'),kind='linear')


b.add_column(a.column('Resistance'),'Resistanceb')


plt.hold(True)
plt.plot(b.column('emp'),b.column('Resistanceb'))
plt.plot(b.column('emp'),b.column('Resistance'))
plt.plot(b.column('emp'),a.column('Resistance'))
plt.show()