##tkinter test with printf in the window
import tkinter as tk
from tkinter import ttk
import tkfilebrowser

ver="0.8"

blurry_threshold = "10"
similarity_threshold = "0.82"
image_filetypes = "jpg;jpeg;png;bmp;tiff;tif"



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
        settings_menu.add_command(label="Image filetypes", command=self.open_image_filetypes)
        settings_menu.add_command(label="Similarity threshold" , command=self.open_similarity_threshold)
        settings_menu.add_command(label="Blurry threshold", command=self.open_blurry_threshold)
        menu_bar.add_command(label="About", command=self.about)

        self.similarity_threshold_window = None
        self.blurry_threshold_window = None
        self.image_filetypes_window = None

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

    def open_similarity_threshold(self):
        if self.similarity_threshold_window is not None:
            return  # The window is already open, do not open another instance

        self.similarity_threshold_window = tk.Toplevel(self)
        self.similarity_threshold_window.title("Similarity threshold")
        self.similarity_threshold_window.geometry("300x120")
        self.similarity_threshold_window.resizable(False, False)

        self.similarity_threshold_window.grid_rowconfigure(0, weight=1)
        self.similarity_threshold_window.grid_rowconfigure(1, weight=1)
        self.similarity_threshold_window.grid_columnconfigure(0, weight=1)
        self.similarity_threshold_window.grid_columnconfigure(1, weight=1)

        self.label = ttk.Label(self.similarity_threshold_window, text="Similarity threshold")
        self.label.pack(fill="x", padx=10, pady=2)

        self.slider = tk.Scale(self.similarity_threshold_window, from_=0, to=1, resolution=0.01, orient="horizontal")
        self.slider.set(float(similarity_threshold))
        self.slider.pack(fill="x", padx=10, pady=2)

        self.btn_save = ttk.Button(self.similarity_threshold_window, text="Save", command=self.save_similarity_threshold)
        self.btn_save.pack(fill="x", padx=10, pady=8)

    def save_similarity_threshold(self):
        similarity_threshold = self.slider.get()
        self.similarity_threshold_window.destroy()
        self.similarity_threshold_window = None  # Reset the reference to None after the window is closed
        self.update_similarity_threshold(similarity_threshold)

    def update_similarity_threshold(self, value):
        global similarity_threshold
        similarity_threshold = value
        print(f"Similarity threshold updated: {similarity_threshold}")

    def open_blurry_threshold(self):
        if self.blurry_threshold_window is not None:
            return

        self.blurry_threshold_window = tk.Toplevel(self)
        self.blurry_threshold_window.title("Blurry threshold")
        self.blurry_threshold_window.geometry("300x110")
        self.blurry_threshold_window.resizable(False, False)

        self.blurry_threshold_window.grid_rowconfigure(0, weight=1)
        self.blurry_threshold_window.grid_rowconfigure(1, weight=1)
        self.blurry_threshold_window.grid_columnconfigure(0, weight=1)
        self.blurry_threshold_window.grid_columnconfigure(1, weight=1)

        self.label = ttk.Label(self.blurry_threshold_window, text="Blurry threshold")
        self.label.pack(fill="x", padx=10, pady=2)

        self.slider = tk.Scale(self.blurry_threshold_window, from_=0, to=50, resolution=1, orient="horizontal")
        self.slider.set(float(blurry_threshold))
        self.slider.pack(fill="x", padx=10, pady=2)

        self.btn_save = ttk.Button(self.blurry_threshold_window, text="Save", command=self.save_blurry_threshold)
        self.btn_save.pack(fill="x", padx=10, pady=8)

    def save_blurry_threshold(self):
        blurry_threshold = self.slider.get()
        self.blurry_threshold_window.destroy()
        self.blurry_threshold_window = None
        self.update_blurry_threshold(blurry_threshold)

    def update_blurry_threshold(self, value):
        global blurry_threshold
        blurry_threshold = value
        print(f"Blurry threshold updated: {blurry_threshold}")


    def open_image_filetypes(self):
        if self.image_filetypes_window is not None:
            return

        self.image_filetypes_window = tk.Toplevel(self)
        self.image_filetypes_window.title("Image filetypes")
        self.image_filetypes_window.geometry("300x110")
        self.image_filetypes_window.resizable(False, False)

        self.image_filetypes_window.grid_rowconfigure(0, weight=1)
        self.image_filetypes_window.grid_rowconfigure(1, weight=1)
        self.image_filetypes_window.grid_columnconfigure(0, weight=1)
        self.image_filetypes_window.grid_columnconfigure(1, weight=1)

        self.label = ttk.Label(self.image_filetypes_window, text="Image filetypes")
        self.label.pack(fill="x", padx=10, pady=2)

        self.entry = ttk.Entry(self.image_filetypes_window)
        self.entry.insert(0, image_filetypes)
        self.entry.pack(fill="x", padx=10, pady=2)


        self.btn_save = ttk.Button(self.image_filetypes_window, text="Save", command=self.save_image_filetypes)
        self.btn_save.pack(fill="x", padx=10, pady=8)

    def save_image_filetypes(self):
        image_filetypes = self.entry.get()
        self.image_filetypes_window.destroy()
        self.image_filetypes_window = None
        self.update_image_filetypes(image_filetypes)

    def update_image_filetypes(self, value):
        global image_filetypes
        image_filetypes = value
        print(f"Image filetypes updated: {image_filetypes}")

    def about(self):
        tk.messagebox.showinfo("About", f"This software was created by Laakiin\nCurrent version is the {ver}\nSource code available on GitHub: https://github.com/Laakiin/blurry_and_similar_images_delete")

    #function that open a new window  displaying hello world while clicking on the button


    def blurry_threshold(self):
        return

    def image_filetypes(self):
        return

if __name__ == "__main__":
    app = App()
    app.mainloop()

