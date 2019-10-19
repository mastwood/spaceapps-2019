import numpy as np
import pandas as pd 
import csv as cs
import matplotlib.pyplot as pl 
import pyhht as hht
import pyhht.visualization as vis
import pyhht.utils as hut
from scipy.signal import hilbert , correlate

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

crosscor=correlate(data[:,1],data[:,2],mode='same')/len(data[:,1])
ax=pl.subplot(3,1,1)
ax.plot(crosscor)
ax2=pl.subplot(3,1,2)
ax2.plot(data[:,0],data[:,1])
ax3=pl.subplot(3,1,3)
ax3.plot(data[:,0],data[:,2])
pl.show()
for i in range(1,27):
    ax= pl.subplot(27,1,i)
    envelope=np.abs(hilbert(data[:,i]))
    ax.plot(data[:,0],data[:,i])
    ax.plot(data[:,0],envelope)

pl.show()
for i in range(1,27):
    ax2=pl.subplot(26,1,i)
    decomposer=hht.EMD(data[:,i]+data[:,0])
    m=decomposer.decompose()[2]
    envelope=np.abs(hilbert(m))
    ax2.plot(data[:,0],m)
    ax2.plot(data[:,0],envelope)

pl.show()


