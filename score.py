import numpy as np
import csv as cs
import matplotlib.pyplot as pl 
import pyhht as hht
import pyhht.visualization as vis
import pyhht.utils as hut
import scipy.signal as si
import tkinter.messagebox as mb
import tkinter as tk
from collections import namedtuple, OrderedDict
from tkinter.filedialog import askopenfilename
from progress.bar import Bar

r = 6371000
s = ''

def loadfile(s):
    splitdata = []
    longlat = []
    splitdata2=[]
    Fourier=[]
    imfs=[]
    Names = []

    with open(s,'r') as fil:
        da=fil.readlines()


    for i in range(1,len(da)):
        splitdata2.append(da[i].split('\t'))
    splitdata2=splitdata2[0][4:len(splitdata2[0])-1]
    splitdata2=np.reshape(splitdata2,(int(len(splitdata2)/4),4))


    for i in range(0, len(splitdata2)):
        splitdata2[i][3] = float(splitdata2[i][1])*np.pi/180
        longlat.append(np.append(splitdata2[i], float(splitdata2[i][2])*np.pi/180))

    longlat=np.array(longlat)
    Names=longlat[:,0]
    with open(s,'r') as fil:
        da2=fil.readlines()

    for i in range(1,len(da)):
        splitdata.append(da2[i].split('\t\t\t\t'))

    for i in range(1,len(splitdata)):
        splitdata[i][len(splitdata[i])-1] = splitdata[i][len(splitdata[i])-1].split('\t\t')[0]

    for i in range(1, len(splitdata)):
        if not (splitdata[i][0].split('-')[0] == '\n' or splitdata[i][0].split('-')[0] == ''):
            splitdata[i][0] = (float(splitdata[i][0].split('-')[0]) - 1) * 24 + float(splitdata[i][0].split('-')[1])

    #This is the data array.
    data = np.array(splitdata[3:len(splitdata)]).astype(float)

    for b in range(1,len(data[0])):
        Four=si.stft(data[:,b], nperseg=15, noverlap=1)
        Fourier.append(np.array(Four))
    Fourier=np.array(Fourier)

    for i in range(0,len(data[0])-1):
        imfs.append(get_imf(i, data))
    
    return ([Names,data,imfs,Fourier,longlat])

# Returns the Great-Circle distance between two points of longitude and lattitude a and b, in meters
def dist(longa,lata,longb,latb):
    dlong = longb-longa
    a = (np.cos(latb)*np.sin(dlong))**2
    b = ((np.cos(lata)*np.sin(latb))-(np.sin(lata)*np.cos(latb)*np.cos(dlong)))**2
    c = np.sqrt(a+b)
    d = (np.sin(lata)*np.sin(latb)+np.cos(lata)*np.cos(latb)*np.cos(dlong))
    angle = np.arctan(c/d)
    return np.abs(r*angle/1000)

def getLoc(name, longlat):
    longi=0
    lat=0
    for i in range(0, len(longlat)):
        if (longlat[i][0]==name):
            longi = longlat[i][3]
            lat = longlat[i][4]
    return ([longi,lat])

def getDist(name1,name2, longlat):
    return dist(float(getLoc(name1, longlat)[0]), float(getLoc(name1, longlat)[1]), float(getLoc(name2, longlat)[0]), float(getLoc(name2, longlat)[1]))

def getName(index, longlat):
    return longlat[index][0]

def find_nearest(a, a0):
    "Element in nd array `a` closest to the scalar value `a0`"
    idx = np.abs(a - a0).argmin()
    return a.flat[idx],idx

def get_imf(i, data):
    decomposer=hht.EMD(data[:,i+1]+data[:,0])
    imf_highfreq=decomposer.decompose()[2]
    return imf_highfreq

def score_full(time_1,Fourier,column,imf,imfs, longlat,data):
    score=0
    t=Fourier[0,:][1]

    j=find_nearest(t,time_1)[1]
    for i in range(0,len(data[0])-1):
        if column!=i:
            c=0
            if j>=7 and j<=t[-1]-7:
                c=np.corrcoef(imfs[i][j-7:j+7],imf[j-7:j+7])[0,1]
            elif j < 7:
                c=np.corrcoef(imfs[i][0:j+7],imf[0:j+7])[0,1]
            else:
                c=np.corrcoef(imfs[i][j-7:25],imf[j-7:25])[0,1]

            score = score + np.abs((1-np.abs(c))*(Fourier[i][2]-Fourier[column][2])*getDist(getName(i, longlat),getName(column, longlat),longlat))
    sc=np.sum(score[:,j])
    #print(sc)
    return sc

def onMain(Names,data,imfs,Fourier,longlat):
    k=[]
    bar= Bar("Processing", max=len(data))
    for j in range(0,len(data)):
        p=[]
        
        for i in range(0,len(data[j])-1):
            p.append(score_full(j,Fourier,i,imfs[i],imfs,longlat,data))
        k.append(p/np.max(p))
        bar.next()
    pl.imshow(np.array(k).T,aspect=len(data)/len(data[0]))

    with open('.\Data\Score_data.txt','w') as fileOpen:
        fileOpen.write(str(list(Names)).replace('[','').replace(']',''))
        fileOpen.write('\n')
        for c in range(1,len(data)):
            fileOpen.write(str(list(np.array(k)[c,:])).replace('[','').replace(']',''))
            fileOpen.write('\n')
    bar.finish()

    pl.colorbar()
    pl.show()
    for i in range(1,len(data[0])):
        ax = pl.subplot(len(data[0]),1,i)
        ax.plot(data[:,0],data[:,i])
    pl.show()


#window
root = tk.Tk()
root.geometry("800x800")

#importing colours for window
Colour = namedtuple('RGB','red, green, blue')
colours = {} #dict of colours
class RGB(Colour):
    def hex_format(self):
        '''Returns colour in hex format'''
        return '#{:02X}{:02X}{:02X}'.format(self.red,self.green,self.blue)
steelblue = RGB(79,148,205)
grey = RGB(205,201,201)

#creating a background
root.configure(background = 'light blue')

#label for button
var = tk.StringVar()
label = tk.Label(root, textvariable = var, bg = 'light blue' )
var.set("Input geomagnetic data here :")
label.place(x = 310, y = 1)

#call back for Button
def selectfile():
    filename = askopenfilename (initialdir = "/", title = "Select file", filetypes = (("text files","*.txt"),))
    #filearray = np.loadtxt(fname = filename)
    s = loadfile(filename)
    mb.showinfo("Thank You", "Data uploaded successfully")
    onMain(s[0],s[1],s[2],s[3],s[4])
    
    

#button to import data in
button = tk.Button(root, text="Import Data",  bg=grey.hex_format(), activebackground=steelblue.hex_format(), command = selectfile)
button.place(x = 350, y = 37)

#creating a spot for output data
outputbox = tk.LabelFrame( root, bg = 'white', text="This is the resulting data", height = 600, width = 600,  )
outputbox.place(x = 100, y = 110)

#instructions for the menu
m = tk.StringVar()
instruct = tk.Label(root, textvariable = m, bg = 'light blue' )
m.set("Please choose a location from the menu at the top")
instruct.place(x = 250, y = 80)

#create a menu to choose which plot from

#This will be the command that displays the graphs
def donothing():
    picture = tk.PhotoImage(file = "sunshine.gif")
    image = tk.Canvas.create_image(500, 500, image=picture)
    image.place(x= 125, y= 135)

menubar = tk.Menu(root, bg = 'grey')
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="BACK", command=donothing)
filemenu.add_command(label="FCHP", command=donothing)
filemenu.add_command(label="FCHU", command=donothing)
filemenu.add_command(label="FSIM", command=donothing)
filemenu.add_command(label="FSMI", command=donothing)
filemenu.add_command(label="GILL", command=donothing)
filemenu.add_command(label="LGRR", command=donothing)
filemenu.add_command(label="MCMU", command=donothing)
filemenu.add_command(label="MSTK", command=donothing)
filemenu.add_command(label="NORM", command=donothing)
filemenu.add_command(label="POLS", command=donothing)
filemenu.add_command(label="RABB", command=donothing)
filemenu.add_command(label="THRF", command=donothing)
filemenu.add_command(label="VULC", command=donothing)
filemenu.add_command(label="WEYB", command=donothing)
filemenu.add_command(label="WGRY", command=donothing)
filemenu.add_command(label="BLC", command=donothing)
filemenu.add_command(label="BRD", command=donothing)
filemenu.add_command(label="CBB", command=donothing)
filemenu.add_command(label="FCC", command=donothing)
filemenu.add_command(label="IQA", command=donothing)
filemenu.add_command(label="MEA", command=donothing)
filemenu.add_command(label="OTT", command=donothing)
filemenu.add_command(label="RES", command=donothing)
filemenu.add_command(label="STJ", command=donothing)
filemenu.add_command(label="VIC", command=donothing)
menubar.add_cascade(label="Location", menu=filemenu)

root.configure(menu = menubar)
root.mainloop()



