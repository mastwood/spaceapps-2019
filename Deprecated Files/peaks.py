import pandas as pd 
import csv as cs
import matplotlib.pyplot as pl 
import pyhht as hht
import pyhht.visualization as vis
import numpy as np
import scipy

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
pl.plot(data[:,0],data[:,1])
pl.show()
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
pl.plot(data[:,0],differ)
pl.show()

decomposer=hht.EMD(data[:,1]+data[:,0])
imfs = decomposer.decompose()
vis.plot_imfs(data[:,0]+data[:,1],imfs,data[:,0])


#Determine where peaks are, change parameters for a change in what is defined as a "peak". In order, minimum height limit, vertical distance to neighbouring samples, horizontal distance to neighboring samples, how prominant a "peak" is, required width of peaks.
ProtoPeaks=scipy.signal.find_peaks(data[:,1], height=0, threshold=0, distance=1, prominence=70, width=0)
Peaks=ProtoPeaks[0]
print(Peaks)
print(len(Peaks))

#Print and plot the peaks.
pl.plot(data[:,1])
pl.plot(Peaks,data[Peaks,1], 'ro', color='red')

pl.show()

