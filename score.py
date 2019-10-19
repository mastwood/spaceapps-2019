import numpy as np
r = 6371000

with open('.\lat_long.csv','r') as fil:
    da=fil.readlines()

with open('.\cleanedData.csv','r') as fil:
    data=fil.readlines()

lat_long = []
for i in range(0,len(da)):
    lat_long.append(da[i].split(','))

for i in range(0, len(lat_long)):
    for j in range(0,len(lat_long[i])):
        lat_long[i][j] = lat_long[i][j].strip()

# Returns the Great-Circle distance between two points of longitude and lattitude a and b, in meters
def dist(longa,lata,longb,latb):
    dlong = longb-longa
    a = (np.cos(latb)*np.sin(dlong))**2
    b = ((np.cos(lata)*np.sin(latb))-(np.sin(lata)*np.cos(latb)*np.cos(dlong)))**2
    c = np.sqrt(a+b)
    d = (np.sin(lata)*np.sin(latb)+np.cos(lata)*np.cos(latb)*np.cos(dlong))
    angle = np.arctan(c/d)
    return (r*angle/1000)

def getLoc(name):
    for i in range(0, len(lat_long)):
        if (lat_long[i][0]==name):
            long = lat_long[i][3]
            lat = lat_long[i][4]
    return ([long,lat])

def getDist(name1,name2):
    return dist(float(getLoc(name1)[0]), float(getLoc(name1)[1]), float(getLoc(name2)[0]), float(getLoc(name2)[1]))


print(getDist('BACK','GILL'))
print(data)


