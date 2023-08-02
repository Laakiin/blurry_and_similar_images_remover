##tkinter test with printf in the window
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkfilebrowser

class App(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        self.title("Hello, Tkinter")
        self.geometry("600x500")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        #create frames for layout with two columns and two rows but on the second row, the column span is 2
        top_frame = tk.Frame(self, background="yellow")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        bottom_frame = tk.Frame(self, background="green")
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        #add a menu bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        #add a settings menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Image filetypes")
        settings_menu.add_command(label="Similarity threshold")
        settings_menu.add_command(label="Blurry threshold")





#bottom frame

        #add a text widget to the bottom frame and add a scrollbar to it, so we can scroll the text inside it, under this text widget, add a clear button to clear the text widget
        self.text = tk.Text(bottom_frame, bg="white", fg="black")
        self.text.pack(side="top")
        self.scrollbar = tk.Scrollbar(bottom_frame, orient="vertical")
        self.scrollbar.config(command=self.text.yview)
        self.scrollbar.pack(side="right", fill="y", after=self.text)
        self.text.config(yscrollcommand=self.scrollbar.set)
        self.btn_clear = ttk.Button(bottom_frame, text="Clear", command=self.clear)
        self.btn_clear.pack(fill="x", expand=True, side="right")




#top right frame
        dirs = []
        #display of a list of lines
        self.listbox = tk.Listbox(top_frame, bg="white", fg="black", selectmode="multiple")
        self.listbox.pack(side="right",expand=True)
        #add a scrollbar to the listbox
        self.scrollbar = tk.Scrollbar(top_frame, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side="right", fill="y", after=self.listbox)
        self.listbox.config(yscrollcommand=self.scrollbar.set)


        #add a button next to the listbox used to delete the selected line
        self.btn_del = ttk.Button(top_frame, text="Delete", command=self.delete)
        self.btn_del.pack(fill="x")
        self.btn_add = ttk.Button(top_frame, text="Add", command=self.add)
        self.btn_add.pack(fill="x")

    def add(self):
        dirs = tkfilebrowser.askopendirnames()
        for filename in dirs:
            self.listbox.insert(tk.END, filename)
            print(f"{filename} added")

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
        for i in indexes:
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

if __name__ == "__main__":
    app = App()
    app.mainloop()

