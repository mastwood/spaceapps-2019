import numpy as np
import csv as cs
import matplotlib.pyplot as pl 
import pyhht as hht
import pyhht.visualization as vis
import pyhht.utils as hut
import scipy.signal as si
from progress.bar import Bar

r = 6371000
s = '.\Data\dataset1.txt'

def loadfile(path):
    s = path

with open(s,'r') as fil:
    da=fil.readlines()

splitdata2=[]
for i in range(1,len(da)):
    splitdata2.append(da[i].split('\t'))
splitdata2=splitdata2[0][4:len(splitdata2[0])-1]
splitdata2=np.reshape(splitdata2,(int(len(splitdata2)/4),4))

longlat = []
for i in range(0, len(splitdata2)):
    splitdata2[i][3] = float(splitdata2[i][1])*np.pi/270
    longlat.append(np.append(splitdata2[i], float(splitdata2[i][2])*np.pi/270))
longlat=np.array(longlat)
Names=longlat[0:-1,0]
print(Names)
with open('./Data/dataset1.txt','r') as fil:
    da2=fil.readlines()

splitdata=[]
for i in range(1,len(da)):
    splitdata.append(da2[i].split('\t\t\t\t'))

for i in range(1,len(splitdata)):
    splitdata[i][len(splitdata[i])-1] = splitdata[i][len(splitdata[i])-1].split('\t\t')[0]

for i in range(1, len(splitdata)):
    if not (splitdata[i][0].split('-')[0] == '\n' or splitdata[i][0].split('-')[0] == ''):
        splitdata[i][0] = (float(splitdata[i][0].split('-')[0]) - 1) * 24 + float(splitdata[i][0].split('-')[1])

#This is the data array.
data=np.array(splitdata[3:len(splitdata)]).astype(float)

# Returns the Great-Circle distance between two points of longitude and lattitude a and b, in meters
def dist(longa,lata,longb,latb):
    dlong = longb-longa
    a = (np.cos(latb)*np.sin(dlong))**2
    b = ((np.cos(lata)*np.sin(latb))-(np.sin(lata)*np.cos(latb)*np.cos(dlong)))**2
    c = np.sqrt(a+b)
    d = (np.sin(lata)*np.sin(latb)+np.cos(lata)*np.cos(latb)*np.cos(dlong))
    angle = np.arctan(c/d)
    return np.abs(r*angle/1000)

def getLoc(name):
    longi=0
    lat=0
    for i in range(0, len(longlat)):
        if (longlat[i][0]==name):
            longi = longlat[i][3]
            lat = longlat[i][4]
    return ([longi,lat])

def getDist(name1,name2):
    return dist(float(getLoc(name1)[0]), float(getLoc(name1)[1]), float(getLoc(name2)[0]), float(getLoc(name2)[1]))

def getName(index):
    return longlat[index][0]

Fourier=[]
for b in range(1,27):
    Four=si.stft(data[:,b], nperseg=15, noverlap=1)
    Fourier.append(np.array(Four))
Fourier=np.array(Fourier)
def find_nearest(a, a0):
    "Element in nd array `a` closest to the scalar value `a0`"
    idx = np.abs(a - a0).argmin()
    return a.flat[idx],idx

def get_imf(i):
    decomposer=hht.EMD(data[:,i+1]+data[:,0])
    imf_highfreq=decomposer.decompose()[2]
    return imf_highfreq

imfs=[]
for i in range(0,26):
    imfs.append(get_imf(i))

def score_full(time_1,Fourier,column,imf,imfs):
    score=0
    t=Fourier[0,:][1]

    j=find_nearest(t,time_1)[1]
    for i in range(0,26):
        if column!=i:
            c=0
            if j>=7 and j<=t[-1]-7:
                c=np.corrcoef(imfs[i][j-7:j+7],imf[j-7:j+7])[0,1]
            elif j < 7:
                c=np.corrcoef(imfs[i][0:j+7],imf[0:j+7])[0,1]
            else:
                c=np.corrcoef(imfs[i][j-7:25],imf[j-7:25])[0,1]

            score = score + np.abs((1-np.abs(c))*(Fourier[i][2]-Fourier[column][2])/getDist(getName(i),getName(column)))
    sc=np.sum(score[:,j])
    #print(sc)
    return sc
k=[]

bar= Bar("Processing", max=744)
for j in range(0,744):
    p=[]
    for i in range(0,26):
        p.append(score_full(j,Fourier,i,imfs[i],imfs))
    k.append(p/np.max(p))
    bar.next()
with open('./Data/Score_data.txt','w') as fileOpen:
    fileOpen.write(Names)
    for c in range(1,26):
        fileOpen.write((k.T)[:,c])
bar.finish()
pl.imshow(np.array(k).T,aspect=744/26)
pl.colorbar()
pl.show()
for i in range(1,27):
    ax = pl.subplot(27,1,i)
    ax.plot(data[:,0],data[:,i])
pl.show()

