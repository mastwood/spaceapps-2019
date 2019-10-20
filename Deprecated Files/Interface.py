import tkinter as tk
from collections import namedtuple, OrderedDict
from tkinter.filedialog import askopenfilename
import numpy as np 
import tkinter.messagebox as mb


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
    filearray = np.loadtxt(fname = filename)
    print(filearray)
    mb.showinfo("Thank You", "Data uploaded successfully")
    

#button to import data in
button = tk.Button(root, text="Import Data",  bg=grey.hex_format(), activebackground=steelblue.hex_format(), command = selectfile)
button.place(x = 350, y = 37)

#creating a spot for output data
outputbox = tk.LabelFrame( root, bg = 'white', text="This is the resulting data", height = 600, width = 600,  )
outputbox.place(x = 100, y = 110)

#istructions for the menu
m = tk.StringVar()
instruct = tk.Label(root, textvariable = m, bg = 'light blue' )
m.set("Please choose a location from the menu at the top")
instruct.place(x = 250, y = 80)

#create a menu to choose which plot from

#This will be thhe command that displays the graphs
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