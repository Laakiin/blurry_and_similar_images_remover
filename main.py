import tkinter as tk
from tkinter import filedialog, ttk
from tkfilebrowser import askopendirnames
import PIL
from sewar.full_ref import uqi
from os import getcwd, popen, listdir, remove
from numpy import array
import cv2
from glob import glob
import time

ver="1.9.1"

###GLOBAL VARIABLES###

try:
    import json
    with open("settings.json") as json_file:
        data = json.load(json_file)
        similarity_threshold = data["similarity_threshold"]
        blurry_threshold = data["blurry_threshold"]
        image_filetypes = data["image_filetypes"]
        initialdir = data["initialdir"]
except:
    similarity_threshold = "0.9"
    blurry_threshold = "10"
    image_filetypes = [".jpg", ".jpeg", ".png",".JPG", ".JPEG", ".PNG"]
    initialdir = getcwd()

stop=False

class App(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        self.title("Blurry and Similar Image Remover")
        self.geometry("960x600")
        self.resizable(True, True)
        #self.iconbitmap("build_files/image-outline-filled.ico")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

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
        settings_menu.add_command(label="Initial directory", command=self.open_initialdir)
        settings_menu.add_command(label="Save settings", command=self.save_settings)
        settings_menu.add_command(label="Load settings", command=self.load_settings)
        menu_bar.add_command(label="About", command=self.about)

        self.similarity_threshold_window = None
        self.blurry_threshold_window = None
        self.image_filetypes_window = None
        self.preferences_window = None

        #bottom frame
        self.text = tk.Text(middle_frame, bg="black", fg="white")
        self.text.pack(side="left", expand=True, fill="both")

        self.scrollbar = tk.Scrollbar(middle_frame, orient="vertical")
        self.scrollbar.config(command=self.text.yview)
        self.scrollbar.pack(fill="y",side="right", after=self.text)

        self.text.config(yscrollcommand=self.scrollbar.set)

        self.btn_clear = ttk.Button(bottom_frame, text="Clear", command=self.clear)
        self.btn_clear.pack(fill="x")

        self.current_progress = tk.IntVar()

        self.progress_current = ttk.Progressbar(bottom_frame,variable=self.current_progress, orient="horizontal", length=200, mode="determinate", )
        self.progress_current.pack(fill="x")
        self.progress_current["value"] = 0

        self.progress_total = ttk.Progressbar(bottom_frame, orient="horizontal", length=200, mode="determinate",)
        self.progress_total.pack(fill="x")
        self.progress_total["value"] = 0

        #top right frame
        dirs = []
        self.listbox = tk.Listbox(top_right_frame,selectmode='multiple', bg="white", fg="black")
        self.listbox.pack(side="left", expand=True, fill="both")
        self.scrollbar = tk.Scrollbar(top_right_frame, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(fill="y",side="right", after=self.listbox)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.btn_add = ttk.Button(top_left_frame, text="Add", command=self.add)
        self.btn_add.pack(fill="x", ipady=10,side="top")
        self.btn_del = ttk.Button(top_left_frame, text="Delete", command=self.delete)
        self.btn_del.pack(fill="x", ipady=10,side="top")

        self.btn_start = ttk.Button(top_left_frame, text="Start", command=self.start)
        self.btn_start.pack(fill="x", ipady=10, side="bottom")

        self.btn_stop = ttk.Button(top_left_frame, text="Stop", command=self.stop)
        self.btn_stop.pack(fill="x", ipady=10, side="bottom")

    ##########SETTINGS MENU FUNCTIONS############
    def save_settings(self):
        settings = {}
        settings["image_filetypes"] = image_filetypes
        settings["similarity_threshold"] = similarity_threshold
        settings["blurry_threshold"] = blurry_threshold
        settings["initialdir"] = initialdir
        with open("settings.json", 'w') as outfile:
            json.dump(settings, outfile)
    def load_settings(self):
        global image_filetypes
        global similarity_threshold
        global blurry_threshold
        global initialdir
        filename = filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("json files","*.json"),("all files","*.*")))
        with open(filename) as json_file:
            settings = json.load(json_file)
            image_filetypes = settings["image_filetypes"]
            similarity_threshold = settings["similarity_threshold"]
            blurry_threshold = settings["blurry_threshold"]
            initialdir = settings["initialdir"]
    ##########SIMILARITY THRESHOLD FUNCTIONS############
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
    ##########INITIAL DIRECTORY FUNCTIONS############
    def open_initialdir(self):
        global initialdir
        dir = filedialog.askdirectory(initialdir=initialdir, title="Select directory")
        initialdir = dir
    ##########BLURRY THRESHOLD FUNCTIONS############
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
    ##########IMAGE FILETYPES FUNCTIONS############
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
    ##########ABOUT FUNCTION############
    def about(self):
        tk.messagebox.showinfo("About", f"This software was created by Anakin'Laakiin'MARQUES\nCurrently in v{ver}\nSource code available on GitHub: https://github.com/Laakiin/blurry_and_similar_images_delete")
    ##########WINDOW FUNCTIONS############
    def add(self):
        dirs = askopendirnames(title="Select a directory", initialdir=initialdir, okbuttontext="Select",
                               cancelbuttontext="Cancel", foldercreation=False)
        child_dirs = []
        for dir in dirs:
            child_dirs.append(self.listchilddirs(dir))
        # add the selected directories and their subdirectories to the listbox
        for i in range(len(child_dirs)):
            for j in range(len(child_dirs[i])):
                if child_dirs[i][j] not in self.listbox.get(0, tk.END):
                    self.listbox.insert(tk.END, child_dirs[i][j])
    def delete(self):
        if self.listbox.curselection() == ():
            return
        # get the index of the selected line
        indexes = []
        index = self.listbox.curselection()
        indexes = list(index)
        # delete the selected line
        for i in range(len(indexes)):
            self.listbox.delete(indexes[i])
    def stop(self):
        global stop
        stop = True
    def start(self):
        global stop
        stop = False
        #start a timer
        global start_time
        start_time = time.time()

        dirs = self.listbox.get(0, tk.END)

        self.progress_total["maximum"] = len(dirs)

        if dirs == ():
            tk.messagebox.showerror("No directory selected", "Please select at least one directory")
            return
        global blurry_threshold
        global similarity_threshold
        global image_filetypes
        #get the list of directories from the listbox
        self.progress_total["value"] = 0
        for i in range(len(dirs)):
            if stop:
                self.current_progress.set(0)
                self.progress_total["value"] = 0
                break
            self.update()
            imgs=self.list_img(dirs[i],image_filetypes)
            logs_file = open("logs.txt", "a")
            logs_file.write(f"------------------------------------\n")
            logs_file.write(f"Images that are going to be analysed: {imgs}\n")
            self.addText(f"Images that are going to be analysed in {dirs[i]}: {imgs}\n","other")
            logs_file.write(f"Number of images: {len(imgs)}\n")
            self.addText(f"Number of images: {len(imgs)}\n","other")
            logs_file.write(f"{popen('date /t').read()}{popen('time /t').read()}\n")
            logs_file.write("Logs begin:\n")
            self.addText(f"{popen('date /t').read()}{popen('time /t').read()}\n","other")
            blur_removed, rmv = self.remove_blurry(imgs, logs_file)
            self.current_progress.set(100)
            logs_file.write(f"Blurry images removed: \n{rmv}\n")
            self.addText(f"Blurry images removed: \n{rmv}\n","info")
            double_removed, rmv = self.remove_double(blur_removed, logs_file)
            self.current_progress.set(100)
            self.addText(f"Double images removed: \n{rmv}\n","info")
            logs_file.write(f"Double images removed: \n{rmv}\n")
            logs_file.write("Logs end\n")
            logs_file.write(f"------------------------------------\n")
            logs_file.close()
            self.progress_total["value"] += 1
            if not stop:
                self.delete_line(dirs[i])


        if not stop:
            now=time.time()
            elapsed_time=now-start_time
            #convert the elapsed time in hour, minutes and seconds
            elapsed_time = time.strftime('%Hh%Mm%Ss', time.gmtime(elapsed_time))
            tk.messagebox.showinfo("Task complete", f"The task has been completed\nTime elapsed: {elapsed_time}")
            return
        else:
            now=time.time()
            elapsed_time=now-start_time
            elapsed_time = time.strftime('%Hh%Mm%Ss', time.gmtime(elapsed_time))
            tk.messagebox.showinfo("Task stopped", f"The task has been stopped after\nTime elapsed: {elapsed_time}")
            return
        return
    def listchilddirs(self,rootdir):
        dirs = []
        dirs.append(rootdir)
        for path in glob(f'{rootdir}/*/**/', recursive=True):
            dirs.append(path)
        return dirs
    def delete_line(self,line):
        #get the index of the line
        index=self.listbox.get(0, tk.END).index(line)
        #delete the linef
        self.listbox.delete(index)
    def clear_list(self):
        self.listbox.delete(0, tk.END)
    def addText(self, txt, arg):
        self.text.configure(state="normal")
        self.text.insert(tk.END, txt)
        self.text.configure(state="disabled")
        self.text.see("end")
    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.configure(state="disabled")
    def update_current_progress(self, value):
        progress_value = self.current_progress.get()
        if progress_value < 100:
            self.current_progress.set(progress_value + value)
    ##########CORE FUNCTIONS############
    def list_img(self,path,image_filetypes):
        imgs = []
        for file in listdir(path):
            if file.endswith(tuple(image_filetypes)):
                imgs.append(f"{path}\\{file}")
            else:
                continue
        return imgs
    def remove_blurry(self,imgs,logs_file):
        global blurry_threshold
        global stop
        self.current_progress.set(0)
        self.progress_current["maximum"] = len(imgs)
        try:
            rmv = []
            for i in range(len(imgs)):
                if stop:
                    self.current_progress.set(0)
                    self.progress_total["value"] = 0
                    break
                self.update()
                img = array(PIL.Image.open(f"{imgs[i]}"))
                laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
                logs_file.write(f"Blurry value of '{imgs[i]}': {laplacian}\n")
                self.addText(f"Blurry value of '{imgs[i]}': {laplacian}\n","osef")
                self.update_current_progress(1)
                if laplacian < int(blurry_threshold):
                    logs_file.write(f"{imgs[i]} is too blurry and has been deleted\n")
                    self.addText(f"{imgs[i]} is too blurry and has been deleted\n","info")
                    rmv.append(imgs[i])
                    remove(imgs[i])
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
        global stop
        rmv=[]
        self.current_progress.set(0)
        len_img=len(imgs)
        self.progress_current["maximum"]=(len_img*(len_img-1))/2
        try:
            for i in range(len(imgs)):
                if stop:
                    self.current_progress.set(0)
                    self.progress_total["value"] = 0
                    break
                for j in range(len(imgs)):
                    if stop:
                        self.current_progress.set(0)
                        self.progress_total["value"] = 0
                        break
                    self.update()
                    if i != j:
                        self.update_current_progress(1)
                        if imgs[i] or imgs[j] not in rmv:
                            img1 = array(PIL.Image.open(f"{imgs[i]}"))
                            img2 = array(PIL.Image.open(f"{imgs[j]}"))
                        else:
                            continue
                        if img1.shape == img2.shape:
                            uqi_value = uqi(img1, img2)
                            logs_file.write(
                                f"Similarity between '{imgs[i]}' and '{imgs[j]}': {round(uqi_value * 100, 2)}%\n")
                            self.addText(f"Similarity between '{imgs[i]}' and '{imgs[j]}': {round(uqi_value * 100, 2)}%\n","osef")
                            if uqi_value > float(similarity_threshold):
                                logs_file.write(f"{imgs[i]} is similar to {imgs[j]} and has been deleted\n")
                                self.addText(f"{imgs[i]} is similar to {imgs[j]} and has been deleted\n","info")
                                rmv.append(imgs[i])
                                remove(imgs[i])
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
                #update the progress bar
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

