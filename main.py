import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkfilebrowser
import PIL
from sewar.full_ref import uqi
from PIL import Image
import os
import numpy as np
import cv2

ver="1.5"

blurry_threshold = "10"
similarity_threshold = "0.9"
image_filetypes = [".jpg", ".png", ".jpeg", ".JPG", ".JPEG", ".PNG"]

initialdir = os.getcwd()


class App(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        self.title("Blurry/Double Image Remover")
        self.geometry("960x600")
        self.resizable(True, True)

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
        settings_menu.add_command(label="Preferences", command=self.open_preferences)
        menu_bar.add_command(label="About", command=self.about)

        self.similarity_threshold_window = None
        self.blurry_threshold_window = None
        self.image_filetypes_window = None
        self.preferences_window = None

        #bottom frame

        #add a text widget to the bottom frame with a scrollbar
        self.text = tk.Text(middle_frame, bg="white", fg="black")
        self.text.pack(side="left", expand=True, fill="both")
        self.scrollbar = tk.Scrollbar(middle_frame, orient="vertical")
        self.scrollbar.config(command=self.text.yview)
        self.scrollbar.pack(fill="y",side="right", after=self.text)
        self.text.config(yscrollcommand=self.scrollbar.set)
        #now add a clear button to the bottom frame under the text widget and scrollbar to clear the text widget
        self.btn_clear = ttk.Button(bottom_frame, text="Clear", command=self.clear)
        self.btn_clear.pack(fill="x")

        self.progress_total = ttk.Progressbar(bottom_frame, orient="horizontal", length=200, mode="determinate",)
        self.progress_total.pack(fill="x")
        self.progress_total["value"] = 0
        self.progress_total["maximum"] = 100


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

        self.btn_start = ttk.Button(top_left_frame, text="Start", command=self.start)
        self.btn_start.pack(fill="x", ipady=10, side="bottom")



    def start(self):
        dirs = self.listbox.get(0, tk.END)
        nb_elem=len(dirs)
        step=100/nb_elem
        if dirs == ():
            #add a message box to inform the user that no directory has been selected
            tk.messagebox.showerror("No directory selected", "Please select at least one directory")
            print("No directory selected")
            return
        global blurry_threshold
        global similarity_threshold
        global image_filetypes
        #get the list of directories from the listbox
        for i in range(len(dirs)):
            self.update()
            imgs=self.list_img(dirs[i],image_filetypes)
            logs_file = open("logs.txt", "a")
            logs_file.write(f"------------------------------------\n")
            logs_file.write(f"Images that are going to be analysed: {imgs}\n")
            self.addText(f"Images that are going to be analysed in {dirs[i]}: {imgs}\n")
            logs_file.write(f"Number of images: {len(imgs)}\n")
            self.addText(f"Number of images: {len(imgs)}\n")
            logs_file.write(f"{os.popen('date /t').read()}{os.popen('time /t').read()}\n")
            logs_file.write("Logs begin:\n")
            self.addText(f"{os.popen('date /t').read()}{os.popen('time /t').read()}\n")
            blur_removed, rmv = self.remove_blurry(imgs, logs_file)
            logs_file.write(f"Blurry images removed: \n{rmv}\n")
            self.addText(f"Blurry images removed: \n{rmv}\n")
            double_removed, rmv = self.remove_double(blur_removed, logs_file)
            self.addText(f"Double images removed: \n{rmv}\n")
            logs_file.write(f"Double images removed: \n{rmv}\n")
            logs_file.write("Logs end\n")
            logs_file.write(f"------------------------------------\n")
            logs_file.close()
            self.delete_line(dirs[i])
            self.progress_total["value"] += step

        tk.messagebox.showinfo("Task complete", "The task has been completed")
        print("Program finished")
        return

    #function that deletes a line in the listbox searching by the content of the line and not the selected line
    def delete_line(self,line):
        #get the index of the line
        index=self.listbox.get(0, tk.END).index(line)
        #delete the linef
        self.listbox.delete(index)
    def add(self):
        dirs = tkfilebrowser.askopendirnames(title="Select a directory", initialdir=initialdir , okbuttontext="Select", cancelbuttontext="Cancel", foldercreation=False)
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

    #function that clears the listbox
    def clear_list(self):
        self.listbox.delete(0, tk.END)
        print("Listbox cleared")

    def print_btn(self,btns , i):
        self.addText(f"{btns[i]} pressed\n")
        print(f"{btns[i]} pressed")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.configure(state="disabled")
        print("Cleared")

    def addText(self, txt):
        self.text.configure(state="normal")
        self.text.insert(tk.END, txt)
        self.text.configure(state="disabled")

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

        #add menu bar to the window with a info button
        self.menu_bar = tk.Menu(self.similarity_threshold_window)
        self.similarity_threshold_window.config(menu=self.menu_bar)
        self.menu_bar.add_command(label="Info", command=self.info_similarity_threshold)

        self.label = ttk.Label(self.similarity_threshold_window, text="Similarity threshold")
        self.label.pack(fill="x", padx=10, pady=2)

        self.slider = tk.Scale(self.similarity_threshold_window, from_=0, to=1, resolution=0.01, orient="horizontal")
        self.slider.set(float(similarity_threshold))
        self.slider.pack(fill="x", padx=10, pady=2)

        self.btn_save = ttk.Button(self.similarity_threshold_window, text="Save", command=self.save_similarity_threshold)
        self.btn_save.pack(fill="x", padx=10, pady=8)

    def info_similarity_threshold(self):
        tk.messagebox.showinfo("Info", "The similarity threshold is a value between 0 and 1 that represents the similarity between two images. The higher the value, the more similar the images must be to be considered duplicates.")
    def save_similarity_threshold(self):
        similarity_threshold = self.slider.get()
        self.similarity_threshold_window.destroy()
        self.similarity_threshold_window = None  # Reset the reference to None after the window is closed
        self.update_similarity_threshold(similarity_threshold)

    def update_similarity_threshold(self, value):
        global similarity_threshold
        similarity_threshold = value
        print(f"Similarity threshold updated: {similarity_threshold}")

    def open_preferences(self):
        if self.preferences_window is not None:
            return  # The window is already open, do not open another instance

        self.preferences_window = tk.Toplevel(self)
        self.preferences_window.title("Preferences")
        self.preferences_window.geometry("300x120")
        self.preferences_window.resizable(False, False)

        self.preferences_window.grid_rowconfigure(0, weight=1)
        self.preferences_window.grid_rowconfigure(1, weight=1)
        self.preferences_window.grid_columnconfigure(0, weight=1)
        self.preferences_window.grid_columnconfigure(1, weight=1)

        self.upper_frame = ttk.Frame(self.preferences_window)
        self.upper_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.middle_frame = ttk.Frame(self.preferences_window)
        self.middle_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.lower_frame = ttk.Frame(self.preferences_window)
        self.lower_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        #add menu bar to the window with a info button
        self.menu_bar = tk.Menu(self.preferences_window)
        self.preferences_window.config(menu=self.menu_bar)
        self.menu_bar.add_command(label="Info", command=self.info_preferences)

        self.label = ttk.Label(self.upper_frame, text="Preferences")
        self.label.pack(fill="x", padx=10, pady=2)

        self.dir_input = ttk.Entry(self.middle_frame)
        self.dir_input.pack(ipadx=50,padx=2,pady=2, side="left")

        self.btn_dir = ttk.Button(self.middle_frame, text="Select dir", command=self.select_dir)
        self.btn_dir.pack(after=self.dir_input, side="right", padx=2, pady=2)

        self.btn_save = ttk.Button(self.lower_frame, text="Save", command=self.save_preferences)
        self.btn_save.pack(fill="x", padx=10, pady=8)

    def select_dir(self):
        dir = filedialog.askdirectory(initialdir=initialdir, title="Select directory")
        self.dir_input.delete(0, tk.END)
        self.dir_input.insert(0, dir)
    def info_preferences(self):
        tk.messagebox.showinfo("Info", "Here you can select the initial directory where the you will be while adding directories.")
    def save_preferences(self):
        preferences = self.dir_input.get()
        self.preferences_window.destroy()
        self.preferences_window = None  # Reset the reference to None after the window is closed
        self.update_preferences(preferences)

    def update_preferences(self, value):
        global initialdir
        initialdir = value
        print(f"Initial directory updated: {initialdir}")
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

        #add menu bar to the window with a info button
        self.menu_bar = tk.Menu(self.blurry_threshold_window)
        self.blurry_threshold_window.config(menu=self.menu_bar)
        self.menu_bar.add_command(label="Info", command=self.info_blurry_threshold)

        self.label = ttk.Label(self.blurry_threshold_window, text="Blurry threshold")
        self.label.pack(fill="x", padx=10, pady=2)

        self.slider = tk.Scale(self.blurry_threshold_window, from_=0, to=50, resolution=1, orient="horizontal")
        self.slider.set(float(blurry_threshold))
        self.slider.pack(fill="x", padx=10, pady=2)

        self.btn_save = ttk.Button(self.blurry_threshold_window, text="Save", command=self.save_blurry_threshold)
        self.btn_save.pack(fill="x", padx=10, pady=8)

    def info_blurry_threshold(self):
        tk.messagebox.showinfo("Info", f"The blurry threshold is a value between 0 and 50 that represents the maximum amount of blur an image can have to be considered 'too' blurry.\n(The lower, the blurrier)")

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

        #add menu bar to the window with a info button
        self.menu_bar = tk.Menu(self.image_filetypes_window)
        self.image_filetypes_window.config(menu=self.menu_bar)
        self.menu_bar.add_command(label="Info", command=self.info_image_filetypes)

        self.label = ttk.Label(self.image_filetypes_window, text="Image filetypes")
        self.label.pack(fill="x", padx=10, pady=2)

        self.entry = ttk.Entry(self.image_filetypes_window)
        self.entry.insert(0, image_filetypes)
        self.entry.pack(fill="x", padx=10, pady=2)


        self.btn_save = ttk.Button(self.image_filetypes_window, text="Save", command=self.save_image_filetypes)
        self.btn_save.pack(fill="x", padx=10, pady=8)

    def info_image_filetypes(self):
        tk.messagebox.showinfo("Info", "The image filetypes are the filetypes that will be considered as images. The filetypes must be separated by a space. For example: .jpg .png .jpeg")
    def save_image_filetypes(self):
        image_filetypes = self.entry.get()
        self.image_filetypes_window.destroy()
        self.image_filetypes_window = None
        self.update_image_filetypes(image_filetypes)

    def update_image_filetypes(self, value):
        global image_filetypes
        #split the string into a list
        image_filetypes = value.split(" ")
        print(f"Image filetypes updated: {image_filetypes}")

    def about(self):
        tk.messagebox.showinfo("About", f"This software was created by Laakiin\nCurrently in v{ver}\nSource code available on GitHub: https://github.com/Laakiin/blurry_and_similar_images_delete")

    def list_img(self,path,image_filetypes):
        imgs = []
        for file in os.listdir(path):
            if file.endswith(tuple(image_filetypes)):
                imgs.append(f"{path}\\{file}")
            else:
                continue
        return imgs

    def remove_blurry(self,imgs,logs_file):
        global blurry_threshold
        try:
            rmv = []
            for i in range(len(imgs)):
                img = np.array(Image.open(f"{imgs[i]}"))
                laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
                logs_file.write(f"Blurry value of '{imgs[i]}': {laplacian}\n")
                print(f"Blurry value of '{imgs[i]}': {laplacian}")
                self.addText(f"Blurry value of '{imgs[i]}': {laplacian}\n")
                if laplacian < int(blurry_threshold):
                    logs_file.write(f"{imgs[i]} is too blurry and has been deleted\n")
                    print(f"{imgs[i]} is too blurry and has been deleted")
                    self.addText(f"{imgs[i]} is too blurry and has been deleted\n")
                    rmv.append(imgs[i])
                    os.remove(imgs[i])
                    imgs.remove(imgs[i])
                else:
                    continue
            return imgs, rmv
        except IndexError:
            return imgs, rmv
        except PIL.UnidentifiedImageError:
            logs_file.write("PIL.UnidentifiedImageError\n")
            imgs.remove(imgs[i])
            self.remove_blurry(imgs, logs_file)
            return imgs, rmv
        except PermissionError:
            logs_file.write("PermissionError\n")
            self.remove_blurry(imgs, logs_file)
            return imgs, rmv

    def remove_double(self,imgs,logs_file):
        global similarity_threshold
        rmv=[]
        try:
            for i in range(len(imgs)):
                for j in range(len(imgs)):
                    if i != j:
                        img1 = np.array(Image.open(f"{imgs[i]}"))
                        img2 = np.array(Image.open(f"{imgs[j]}"))
                        if img1.shape == img2.shape:
                            uqi_value = uqi(img1, img2)
                            logs_file.write(
                                f"Similarity between '{imgs[i]}' and '{imgs[j]}': {round(uqi_value * 100, 2)}%\n")
                            print(f"Similarity between '{imgs[i]}' and '{imgs[j]}': {round(uqi_value * 100, 2)}%")
                            self.addText(f"Similarity between '{imgs[i]}' and '{imgs[j]}': {round(uqi_value * 100, 2)}%\n")
                            if uqi_value > float(similarity_threshold):
                                logs_file.write(f"{imgs[i]} is similar to {imgs[j]} and has been deleted\n")
                                print(f"{imgs[i]} is similar to {imgs[j]} and has been deleted")
                                self.addText(f"{imgs[i]} is similar to {imgs[j]} and has been deleted\n")
                                rmv.append(imgs[i])
                                os.remove(imgs[i])
                                imgs.remove(imgs[i])
                                break
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                #remove the image from the list
                imgs.remove(imgs[i])
            return imgs, rmv
        except IndexError:
            return imgs, rmv
        except PIL.UnidentifiedImageError:
            logs_file.write("PIL.UnidentifiedImageError\n")
            imgs.remove(imgs[i])
            self.remove_double(imgs,logs_file)
            return imgs, rmv
        except PermissionError:
            logs_file.write("PermissionError\n")
            self.remove_double(imgs,logs_file)
            return imgs, rmv

if __name__ == "__main__":
    app = App()
    app.mainloop()

