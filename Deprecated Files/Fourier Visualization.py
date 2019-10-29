#Fourier Visualization

import numpy as np
import scipy
import matplotlib.pyplot as plt
N=1000
T=1/1000
x=np.linspace(0,N*T,N)
y=np.sin(25*2*np.pi*x)+1.1*np.cos(35*2*np.pi*x)+0.69*np.sin(50*2*np.pi*x)
ytriv=np.sin(10*2*np.pi*x)
yFourier=scipy.fftpack.fft(y)
xFourier=np.linspace(0,1/(2*T),N/2)
ytrivFourier=scipy.fftpack.fft(ytriv)
plt.title("Nontrivial data")
plt.xlabel=("Time")
plt.ylabel=("Intensity")
plt.plot(x,y)
plt.show()

#plt.xlim(0,75)
#plt.plot(xFourier,2/N*np.abs(yFourier[:N//2]))
#plt.show()
#plt.plot(x,ytriv)
#plt.show()
#plt.xlim(0,20)
#plt.plot(xFourier,2/N*np.abs(ytrivFourier[:N//2]))
#plt.show()

