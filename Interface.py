import tkinter as tk
from collections import namedtuple, OrderedDict
from tkinter.filedialog import askopenfilename

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

#label for button
var = tk.StringVar()
label = tk.Label(root, textvariable = var)
var.set("Important geomagnetic data here :")
label.pack()

#call back for Button
def selectfile():
<<<<<<< HEAD
    filename = askopenfilename (initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),))
=======
    filename = askopenfilename (initialdir = "/",title = "Select file",filetypes = ("all files","*.*"))
>>>>>>> 40f7f1ed2a2085e0bdf897de64b16ab781accb38
    print(filename)

#button to import data in
button = tk.Button(root, text="Import Data", bg=grey.hex_format(), activebackground=steelblue.hex_format(), command = selectfile)
button.pack()

root.mainloop()