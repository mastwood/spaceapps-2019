import numpy as np
import pandas as pd 
import csv as cs

da = ''
with open('./Data/dataset1.txt','r') as fil:
    da=fil.readlines()

splitdata=[]
for i in range(1,len(da)):
    splitdata.append(da[i].split('\t\t\t\t'))
for i in range(1,len(splitdata)):
    splitdata[i][len(splitdata[i])-1]=splitdata[i][len(splitdata[i])-1].split('\t\t')[0]

with open('cleanedData.csv','w') as fil:
    csvwriter = cs.writer(fil)
    csvwriter.writerows(splitdata)