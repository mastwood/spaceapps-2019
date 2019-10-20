from tkinter import *

root = Tk()
frame=Frame(root)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
frame.grid(row=0, column=0, sticky=N+S+E+W)
grid=Frame(frame)
grid.grid(sticky=N+S+E+W, column=0, row=7, columnspan=2)
Grid.rowconfigure(frame, 7, weight=1)
Grid.columnconfigure(frame, 0, weight=1)
z=1

def imageopen(int):
    novi = Toplevel()
    canvas = Canvas(novi, width = 450, height = 350)
    canvas.pack(expand = YES, fill = BOTH)
    gif1 = PhotoImage(file = z)
                                #image not visual
    canvas.create_image(0, 0, image = gif1, anchor = NW)
    #assigned the gif1 to the canvas object
    canvas.gif1 = gif1
    
root.geometry("400x400")
#example values
for x in range(7):
    for y in range(4):
        
        btn = Button(frame, text=("Image",z),fg='blue',command=lambda:imageopen(z".gif"))
        btn.grid(column=y, row=x, sticky=N+S+E+W)
        z=z+1
for x in range(4):
  Grid.columnconfigure(frame, x, weight=1)

for y in range(7):
  Grid.rowconfigure(frame, y, weight=1)

root.mainloop()