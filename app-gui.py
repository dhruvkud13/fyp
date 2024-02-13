from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
from create_dataset import augment_captured_images
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
import cv2
from time import time
from PIL import Image
from tkinter import filedialog
import os
#from PIL import ImageTk, Image
from gender_prediction import emotion,ageAndgender
names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Police Department")
        self.resizable(False, False)
        self.geometry("650x350")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            render = PhotoImage(file='homepagepic.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="        Police Department System        ", font=self.controller.title_font,fg="#263942")
            label.grid(row=0, sticky="ew")
            button1 = tk.Button(self, text="   Rgeister a Criminal  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="   Check Suspect  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
            button1.grid(row=1, column=0, ipady=3, ipadx=7)
            button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button3.grid(row=3, column=0, ipady=3, ipadx=32)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name of criminal:", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg="#ffffff", bg="#263942")
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
        self.buttonclear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)
    # def start_training(self):
    #     global names
    #     if self.user_name.get() == "None":
    #         messagebox.showerror("Error", "Name cannot be 'None'")
    #         return
    #     elif self.user_name.get() in names:
    #         messagebox.showerror("Error", "User already exists!")
    #         return
    #     elif len(self.user_name.get()) == 0:
    #         messagebox.showerror("Error", "Name cannot be empty!")
    #         return
    #     name = self.user_name.get()
    #     names.add(name)
    #     self.controller.active_name = name
    #     self.controller.frames["PageTwo"].refresh_names()
    #     self.controller.show_frame("PageThree")
    def start_training(self):
        global names

        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return

        name = self.user_name.get()

        # Check if the name is already registered
        with open("registered_criminals.txt", "r") as f:
            registered_names = f.read().strip().split()
            if name in registered_names:
                messagebox.showerror("Error", "Criminal already registered!")
                return

        # Add the name to the set and update the registered_criminals.txt file
        names.add(name)
        with open("registered_criminals.txt", "a") as f:
            f.write(name + "\n")

        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")
            
    def clear(self):
        self.user_name.delete(0, 'end')


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Check Suspect", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.buttonclear = tk.Button(self, text="Clear", command=self.clear, fg="#ffffff", bg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.next_foo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)
        self.buttonclear.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)
        
    def next_foo(self):
        if self.user_name.get() == 'None':
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.user_name.get()
        self.controller.show_frame("PageFour")  
    # def next_foo(self):
    #     self.controller.active_name = ''  # Set active_name to an empty string
    #     self.controller.show_frame("PageFour")  
        
    def clear(self):
        self.user_name.delete(0, 'end')
        
    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))
            
class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.uploadbutton = tk.Button(self, text="Upload Image", fg="#ffffff", bg="#263942", command=self.image_upload)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.augmentbutton = tk.Button(self, text="Augment the Image", fg="#ffffff", bg="#263942",command=self.augment)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)
        self.uploadbutton.grid(row=2, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.augmentbutton.grid(row=2, column=1, ipadx=5, ipady=4, padx=10, pady=20)

        self.path_label = tk.Label(self, text="", font='Helvetica 10', fg="gray")
        self.path_label.grid(row=3, column=0, sticky="ew", pady=10)
        self.uploaded_image_path = ""

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "Not enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        self.controller.show_frame("PageFour")

    def augment(self):
        messagebox.showinfo("INSTRUCTIONS", "We will now augment the captured images.")
        x= augment_captured_images(self.controller.active_name, self.uploaded_image_path)
        self.controller.num_of_images = x
        messagebox.showinfo("SUCCESS", "Image augmentation completed.")

    def image_upload(self):
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                with open(file_path, 'r'):
                    pass  # Test if the file can be opened for reading
            except Exception as e:
                self.path_label.config(text=f"Error: {e}")
                return

            # self.controller.active_name = self.controller.frames["PageOne"].user_name.get()
            self.uploaded_image_path = file_path
            self.path_label.config(text=f"Selected Image: {file_path}")
# class PageFour(tk.Frame):

    # def __init__(self, parent, controller):
    #     tk.Frame.__init__(self, parent)
    #     self.controller = controller

    #     label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
    #     label.grid(row=0,column=0, sticky="ew")
    #     button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
    #     #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
    #     #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
    #     button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
    #     button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
    #     #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
    #     #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
    #     button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    # def openwebcam(self):
    #     main_app(self.controller.active_name)

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")

        self.path_label = tk.Label(self, text="", font='Helvetica 10', fg="gray")
        self.path_label.grid(row=1, column=0, sticky="ew", pady=10)

        button_camera = tk.Button(self, text="Face Recognition using Camera", command=self.openwebcam, fg="#ffffff", bg="#263942")
        button_camera.grid(row=2, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

        button_upload = tk.Button(self, text="Face Recognition using Image Upload", command=self.open_image_recognition, fg="#ffffff", bg="#263942")
        button_upload.grid(row=3, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

        button_video = tk.Button(self, text="Face Recognition using Video Upload", command=self.open_video_recognition, fg="#ffffff", bg="#263942")
        button_video.grid(row=4, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

        button_home = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button_home.grid(row=5, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    # def open_camera_recognition(self):
    #     self.controller.active_name = self.controller.frames["PageOne"].user_name.get()
    #     self.controller.show_frame("PageFour")
    #     main_app(self.controller.active_name)
    def openwebcam(self):
        main_app(self.controller.active_name)

    def open_image_recognition(self):
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            try:
                with open(file_path, 'r'):
                    pass  # Test if the file can be opened for reading
            except Exception as e:
                self.path_label.config(text=f"Error: {e}")
                return

            # self.controller.active_name = self.controller.frames["PageOne"].user_name.get()
            self.path_label.config(text=f"Selected Image: {file_path}")
            self.controller.show_frame("PageFour")
            main_app(self.controller.active_name, image_path=file_path)
        else:
            self.path_label.config(text="No image selected.")

    def open_video_recognition(self):
        video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4;*.avi")])
        if video_path:
            try:
                with open(video_path, 'r'):
                    pass  # Test if the file can be opened for reading
            except Exception as e:
                self.path_label.config(text=f"Error: {e}")
                return

            # self.controller.active_name = self.controller.frames["PageOne"].user_name.get()
            self.path_label.config(text=f"Selected Video: {video_path}")
            self.controller.show_frame("PageFour")
            main_app(self.controller.active_name, video_path=video_path)
        else:
            self.path_label.config(text="No video selected.")
    '''
    def gender_age_pred(self):
       ageAndgender()
    def emot(self):
        emotion()
'''


app = MainUI()
app.iconphoto(True, tk.PhotoImage(file='icon.ico'))
app.mainloop()
