import numpy as np
import pandas as pd 

da = ''
with open('./Data/dataset1.txt','r') as fil:
    da=fil.readlines()

splitdata=[]
for i in range(1,len(da)):
    splitdata.append(da[i].split('\t\t\t\t'))
print(splitdata)