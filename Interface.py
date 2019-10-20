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
outputbox.place(x = 100, y = 175)


root.mainloop()