import numpy
import Stoner
import Stoner.Plot as plt
import pylab as plot

##################### MATERIAL PROPERTIES #####################
# Temperature

Tsub = 20

# Thermal Conductivity

Kcu = 1200
Kp = 2.8
Ksub = 0.1

# Thermal Area

Acu = 100e-9 * 50e-9
Ap = 100e-9 * 20e-9
Asub = 100e-9 * 10e-6

# Thermal Lenght

dx = 500e-9
dy = 200e-9
dz = 100e-9

# Specific Heat

Cd = 462/63.5
Ci = Cd
Md = 8930*50e-9*100e-9*2e-6 #??????????
Mi = 8930*50e-9*100e-9*10e-6
# Seebeck

Spc = 5

# Current Path

R = 220
I = 1e-6


##################### COEFFICIENTS #####################

a1 = (I*I*R*((((Ksub*Asub)/dz)+((Kp*Ap)/dy)))*Tsub)*(1/Mi*Ci)
a2 = (Kcu*Acu)/dx
a3 = -(((Ksub*Asub)/dz)+((Kcu*Acu)/dx)+((Kp*Ap)/dy))

b = (Kcu*Acu)/(Md*Cd*dx)

alpha = 0.5*(a3-b+numpy.sqrt((b*b)+(a3*a3)-(2*b*a3)-(4*b*(a2+a3))))
beta = 0.5*(a3-b-numpy.sqrt((b*b)+(a3*a3)-(2*b*a3)-(4*b*(a2+a3))))

B = (alpha/(beta-alpha))*(Tsub+(a1*(1-b))/(b*b*(a2+a3)))
A = Tsub-B+(a1*(1-b))/(b*(a2+a3))

##################### TEMPERATURE FUNCTION #####################
t=0

Ti = A*numpy.exp(alpha*t)+B*numpy.exp(beta*t)-(a1*(1-b))/(b*(a2+a3))
Td = A*(1-(alpha/b))*numpy.exp(alpha*t)+B*(1-(beta/b))*numpy.exp(beta*t)-(a1*(1-b))/(b*b*(a2+a3))

#Ti = (a1*(1-b))/(b*(a2+a3))
#Td = -(a1*(1-b))/(b*b*(a2+a3))


##################### VOLTAGE ##################### 

V = -Spc*(Tsub-Td)

print Ti,Td
#plot.plot(I,V)

#plot.show()
















