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

with open('lat_long.csv','w') as fil:
    csvwriter = cs.writer(fil)
    csvwriter.writerows(splitdata)

