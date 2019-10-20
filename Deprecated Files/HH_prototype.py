import numpy as np
import pandas as pd 
import csv as cs
import matplotlib.pyplot as pl 
import pyhht as hht
import pyhht.visualization as vis
import pyhht.utils as hut
import scipy.signal as si

da = ''

with open('./Data/dataset1.txt','r') as fil:
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

# with open('cleanedData.csv','w') as fil:
#     csvwriter = cs.writer(fil)
#     csvwriter.writerows(splitdata)

#data[:,0] is the time column (in units of Hours)
# pl.plot(data[:,0],data[:,1])
#pl.show()

#this function computes the derivative of one array wrt another
def diff(y,x):
    if len(x)==len(y):
        q=[0]
        for i in range(2,len(y)):
            q.append((y[i]-y[i-1])/(x[i]-x[i-1]))
        q.append(0)
        return np.array(q)
    else:
        print("Error: Invalid shape. x and y must be the same length")

#computing the derivative of column 1 wrt time
differ=(diff(data[:,1],data[:,0]))    
#pl.plot(data[:,0],differ)

imfs=np.array([])
# spectrum = hilbert(denoised)
# phase = np.unwrap(np.angle(spectrum))
# freq = (np.diff(phase)/(2.0*np.pi))*744
#vis.plot_imfs(data[:,0]+data[:,3],imfs,data[:,0])

#crosscor=correlate(data[:,1],data[:,2],mode='same')/len(data[:,1])

# for i in range(1,18):
#     ax= pl.subplot(18,1,i)
#     ax.plot(data[:,0],data[:,i])

# pl.show()
# for i in range(1,27):
#     ax2=pl.subplot(26,1,i)
#     decomposer=hht.EMD(data[:,i]+data[:,0])
#     m=decomposer.decompose()[2]
#     envelope=np.abs(hilbert(m))
#     ax2.plot(data[:,0],m)
#     ax2.plot(data[:,0],envelope)

Fourier=[]

for b in range(1,27):
    Four=si.stft(data[:,b], nperseg=30, noverlap=9)
    Fourier.append(np.array(Four))
Fourier=np.array(Fourier)
def find_nearest(a, a0):
    "Element in nd array `a` closest to the scalar value `a0`"
    idx = np.abs(a - a0).argmin()
    return a.flat[idx],idx
def score_fourier(time_1,Fourier,column):
    score=0
    t=Fourier[0,:][1]
    j=find_nearest(t,time_1)[1]

    for i in range(0,26):
        if column!=i:
            score = score + np.abs(Fourier[i][2]-Fourier[column][2])

    return np.sum(score[:,j])

k=[]
for j in range(0,744):
    p=[]
    for i in range(0,26):
        p.append(score_fourier(j,Fourier,i))
    k.append(p/np.max(p))
pl.imshow(np.array(k).T,aspect=744/26)
pl.show()
    # ax=pl.subplot(27,1,b)
    # ax.pcolormesh(t,f,np.abs(zxx),vmin=0)
    
    # Fourier.append(zxx[2])
    # print ("Below is Plot #",b,".")
    # pl.plot(sum(Fourier))
    # pl.show()


# for i in range(1,27):
#     ax2=pl.subplot(27,1,i)
#     ax2.plot(data[:,0],data[:,i])
# pl.show()
# print(Fourier.shape)


