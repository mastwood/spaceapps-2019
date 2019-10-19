import pandas as pd 
import csv as cs
import matplotlib.pyplot as pl 
import pyhht as hht
import pyhht.visualization as vis
import numpy as np
import scipy
da = ''

b=1

with open('dataset1.txt','r') as fil:
        da=fil.readlines()
splitdata=[]
for i in range(1,len(da)):
    splitdata.append(da[i].split('\t\t\t\t'))
for i in range(1,len(splitdata)):
    splitdata[i][len(splitdata[i])-1] = splitdata[i][len(splitdata[i])-1].split('\t\t')[0]
for i in range(1, len(splitdata)):
    if not (splitdata[i][0].split('-')[0] == '\n' or splitdata[i][0].split('-')[0] == ''):
        splitdata[i][0] = (float(splitdata[i][0].split('-')[0]) - 1) * 24 + float(splitdata[i][0].split('-')[1])
#This is the data array.
data=np.array(splitdata[3:len(splitdata)]).astype(float)
for b in range(1,27):
    ProtoFourier=scipy.signal.stft(data[:,b], nperseg=10, noverlap=9)
    Fourier=(ProtoFourier[2])
    #print(Fourier)
    print ("Below is Plot #",b,".")
    pl.plot(Fourier.T)
    pl.show()
    b=b+1

#ProtoFourier=scipy.signal.stft(data[:,2], nperseg=10, noverlap=9)
#Fourier=(ProtoFourier[2])
#print(Fourier)

#pl.plot(Fourier)
#pl.show()

