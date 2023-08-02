##tkinter test with printf in the window
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkfilebrowser

ver="0.1"

class App(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        self.title("Hello, Tkinter")
        self.geometry("660x600")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        #create frames for layout with two columns and two rows but on the second row, the column span is 2
        top_frame = tk.Frame(self)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        top_right_frame = tk.Frame(top_frame)
        top_right_frame.pack(side="right", fill="both", expand=True)

        top_left_frame = tk.Frame(top_frame)
        top_left_frame.pack(side="left", fill="both", expand=True)


        middle_frame = tk.Frame(self)
        middle_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        bottom_frame = tk.Frame(self)
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        #add a menu bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        #add a settings menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Image filetypes")
        settings_menu.add_command(label="Similarity threshold")
        settings_menu.add_command(label="Blurry threshold")
        menu_bar.add_command(label="About", command=self.about)





#bottom frame

        #add a text widget to the bottom frame with a scrollbar
        self.text = tk.Text(middle_frame, bg="white", fg="black")
        self.text.pack(side="left", expand=True)
        self.scrollbar = tk.Scrollbar(middle_frame, orient="vertical")
        self.scrollbar.config(command=self.text.yview)
        self.scrollbar.pack(fill="y",side="right", after=self.text)
        self.text.config(yscrollcommand=self.scrollbar.set)
        #now add a clear button to the bottom frame under the text widget and scrollbar to clear the text widget
        self.btn_clear = ttk.Button(bottom_frame, text="Clear", command=self.clear)
        self.btn_clear.pack(fill="x")






#top right frame
        dirs = []
        #display of a list of lines in a listbox widget with a scrollbar in the top right frame
        self.listbox = tk.Listbox(top_right_frame, bg="white", fg="black")
        self.listbox.pack(side="left", expand=True, fill="both")
        self.scrollbar = tk.Scrollbar(top_right_frame, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(fill="y",side="right", after=self.listbox)
        self.listbox.config(yscrollcommand=self.scrollbar.set)




        #add a button next to the listbox used to delete the selected line
        self.btn_add = ttk.Button(top_left_frame, text="Add", command=self.add)
        self.btn_add.pack(fill="x", ipady=10,side="top")
        self.btn_del = ttk.Button(top_left_frame, text="Delete", command=self.delete)
        self.btn_del.pack(fill="x", ipady=10,side="top")


    def add(self):
        dirs = tkfilebrowser.askopendirnames()
        #add dirs in the listbox, but verify that the line doesn't exist already
        for dir in dirs:
            if dir not in self.listbox.get(0, tk.END):
                self.listbox.insert(tk.END, dir)
                print(f"{dir} added")
            else:
                print(f"{dir} already in the list")

    def delete(self):
        if self.listbox.curselection() == ():
            print("No line selected")
            return
        #get the index of the selected line

        indexes=[]
        index=self.listbox.curselection()
        indexes=list(index)
        print(indexes)
        #delete the selected line
        for i in range(len(indexes)):
            self.listbox.delete(indexes[i])
            print(f"Line {indexes[i]} deleted")



    def print_btn(self,btns , i):
        self.addText(f"{btns[i]} pressed\n")
        print(f"{btns[i]} pressed")

    def clear(self):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", tk.END)
        self.txt.configure(state="disabled")
        print("Cleared")

    def addText(self, text):
        self.txt.configure(state="normal")
        self.txt.insert(tk.END, text)
        self.txt.configure(state="disabled")

    def about(self):
        tk.messagebox.showinfo("About", f"This software was created by Laakiin\nCurrent version is the {ver}\nSource code available on GitHub: https://github.com/Laakiin/blurry_and_similar_images_delete")


if __name__ == "__main__":
    app = App()
    app.mainloop()

