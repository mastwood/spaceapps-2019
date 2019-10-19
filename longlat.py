import numpy as np
import pandas as pd 
import csv as cs

da = ''

with open('./Data/dataset1.txt','r') as fil:
    da=fil.readlines()

splitdata=[]
for i in range(1,len(da)):
    splitdata.append(da[i].split('\t'))
splitdata=splitdata[0][4:len(splitdata[0])-1]
splitdata=np.reshape(splitdata,(int(len(splitdata)/4),4))

data = []
for i in range(0, len(splitdata)):
    splitdata[i][3] = float(splitdata[i][1])*np.pi/180
    data.append(np.append(splitdata[i], float(splitdata[i][2])*np.pi/180))
print(data)

with open('lat_long.csv','w') as fil:
     csvwriter = cs.writer(fil)
     csvwriter.writerows(data)

