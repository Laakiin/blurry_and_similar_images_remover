#Import tkinter library
from tkinter import *
from tkinter import ttk
#Create an instance of tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
#Define a new function to open the window
def open_win():
   new= Toplevel(win)
   new.geometry("750x250")
   new.title("New Window")
   #Create a Label in New window
   Label(new, text="Hey, Howdy?", font=('Helvetica 17 bold')).pack(pady=30)
#Create a label
Label(win, text= "Click the below button to Open a New Window", font= ('Helvetica 17 bold')).pack(pady=30)
#Create a button to open a New Window
ttk.Button(win, text="Open", command=open_win).pack()
win.mainloop()