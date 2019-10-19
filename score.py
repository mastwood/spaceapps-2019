import numpy as np
r = 6371000

# Returns the Great-Circle distance between two points of longitude and lattitude a and b 
def dist(longa,lata,longb,latb):
    print(longa,lata,longb,latb)
    dlong = longb-longa
    dlat = latb-lata
    a = (np.cos(latb)*np.sin(dlong))**2
    b = (np.cos(lata)*np.sin(latb)-np.sin(lata)*np.cos(latb)*np.cos(dlong))**2
    c = np.sqrt(a+b)
    d = (np.sin(lata)*np.sin(latb)+np.cos(lata)*np.cos(latb)*np.cos(dlong))
    angle = np.arccos(c/d)
    print(np.degrees(angle))
    return (r*angle)

print(dist(np.radians(60),np.radians(-70),np.radians(70),np.radians(-70)))

