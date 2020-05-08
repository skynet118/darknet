 ################## Object detection with OpenCv and YOLO algorithm ##################





######################################################################################
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import time


# class to show two windows
class App2:
    def __init__(self, window, video_source1, video_source2):

        self.window = window
        self.framevideo = Frame(self.window)
        # self.framevideo.pack()
        self.framevideo.grid(row=0, column=0)
        self.framevideo.configure(background="#ffffff")
        self.video_source1 = video_source1
        self.video_source2 = video_source2
        self.photo1 = ""
        self.photo2 = ""

        # open video source
        self.vid1 = MyVideoCapture(self.video_source1, self.video_source2)

        # Create a canvas that can fit the above video source size
        Label(self.framevideo, text="Video capture", bg="#ffffff").grid(row=0, column=0)
        Label(self.framevideo, text="Video Processed", bg="#ffffff").grid(row=0,column=1)

        self.canvas1 = Canvas(self.framevideo, width=416, height=416)
        self.canvas2 = Canvas(self.framevideo, width=416, height=416)
        # self.canvas1.pack(padx=5, pady=10, side="left")
        # self.canvas2.pack(padx=5, pady=60, side="left")
        self.canvas1.grid(row=1, column=0, padx=5, pady=5)
        self.canvas2.grid(row=1, column=1, padx=5, pady=5)

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 10
        self.update()

        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        ret1, frame1, ret2, frame2 = self.vid1.get_frame

        if ret1 and ret2:
                self.photo1 = ImageTk.PhotoImage(image=Image.fromarray(frame1))
                self.photo2 = ImageTk.PhotoImage(image=Image.fromarray(frame2))
                self.canvas1.create_image(0, 0, image=self.photo1, anchor=NW)
                self.canvas2.create_image(0, 0, image=self.photo2, anchor=NW)

        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source1, video_source2):
        # Open the video source
        self.vid1 = cv2.VideoCapture(video_source1)
        self.vid2 = cv2.VideoCapture(video_source2)

        if not self.vid1.isOpened():
            raise ValueError("Unable to open video source", video_source1)

    @property
    def get_frame(self):
        ret1 = ""
        ret2 = ""
        if self.vid1.isOpened() and self.vid2.isOpened():
            ret1, frame1 = self.vid1.read()
            ret2, frame2 = self.vid2.read()
            try:
                frame1 = cv2.resize(frame1, (416, 416), interpolation = cv2.INTER_AREA)
                frame2 = cv2.resize(frame2, (416, 416), interpolation = cv2.INTER_AREA)
            except: #Exception as e:
                pass
            if ret1 and ret2:
                # Return a boolean success flag and the current frame converted to BGR
                return ret1, cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB), ret2, cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            else:
                return ret1, None, ret2, None
        else:
            return ret1, None, ret2, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid1.isOpened():
            self.vid1.release()
        if self.vid2.isOpened():
            self.vid2.release()


class App:

    def __init__(self, root):
        
        self.root = root
        self.framebuttons = Frame(root)
        # self.framebuttons.pack()
        self.framebuttons.configure(bg='#ffffff')
        self.framebuttons.grid(row=1, column= 0)

        self.leftsideframe = Frame(self.framebuttons)
        self.leftsideframe.configure(bg='#ffffff')
        self.leftsideframe.grid(row=0, column=0, padx=20, pady=20)

        self.rightsideframe = Frame(self.framebuttons)
        self.rightsideframe.configure(bg='#ffffff')
        self.rightsideframe.grid(row=0, column=1, padx=20, pady=20, sticky=W)

        Label(self.leftsideframe, text="Select Mode", bg="#ffffff").grid(row=0, column=0, columnspan=1, sticky=W)
        choises = ['Detection Real time', 'Image Processing', 'Video Processing']
        
        mode_selected = StringVar(self.leftsideframe)


        def selection(eventObject):
            
            if eventObject.widget.get() == "Detection Real time":
                mode_selected.set("demo")
            elif eventObject.widget.get() == "Image Processing":
                mode_selected.set("test")
            elif eventObject.widget.get() == "Video Processing":
                mode_selected.set("test")

    
        combomenu = ttk.Combobox(self.leftsideframe, values=choises, textvariable= choises[0] ,  state='readonly')
        combomenu.current(0)
        combomenu.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky=W) 
        combomenu.bind("<<ComboboxSelected>>", selection)
        
     
        # Radio button

        Label(self.leftsideframe ,text="Choose the threshold: \n", bg="#ffffff").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        valueRadioButton = IntVar()
        valueRadioButton.set(0)
        thresholds = [("0.3"),("0.5"), ("0.75")]

        def showChoise():
            print(valueRadioButton.get())
        
        for val, threshold in enumerate(thresholds):
            Radiobutton(self.leftsideframe, text=threshold, padx= 20, variable=valueRadioButton, command=showChoise, value=val, background="#ffffff", highlightbackground="#ffffff").grid(padx=2, pady=2,sticky=W)



        def directory_file(entryButton, labelEntry):
            if labelEntry['text'] == "Open File":
                file_selected = filedialog.askopenfilename(filetypes=(("python files","*.mp4"),("All files","*.*")))
                entryButton.insert(END, file_selected)
            elif labelEntry['text'] == "Weights":
                file_selected = filedialog.askopenfilename(filetypes=(("weights files","*.weights"),("All files","*.*")))
                entryButton.insert(END, file_selected)
            elif labelEntry['text'] == "Configuration":
                file_selected = filedialog.askopenfilename(filetypes=(("configuration files","*.cfg"),("All files","*.*")))

            print(file_selected)


    # first label, entry and button to brose
        labelEntry = Label(self.rightsideframe, text="Open File", bg="#ffffff")
        labelEntry.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        entryFile = Entry(self.rightsideframe, font=12, width=40)
        entryFile.grid(row=0, column=4, columnspan=3, padx=5, pady=5)
        browseButton = Button(self.rightsideframe, text="Browse", padx=25, pady=5, command=lambda: directory_file(entryFile, labelEntry), fg="#000000", bg="#ffffff")
        browseButton.grid(row=0, column=7,columnspan=2, padx=5, pady=5, sticky=W)

    # 2
        labelEntry2 = Label(self.rightsideframe, text="Weights",bg="#ffffff")
        labelEntry2.grid(row=1, column=2, columnspan=2, padx=5, pady=5)
        entryFile2 = Entry(self.rightsideframe, font=12, width=40)
        entryFile2.grid(row=1, column=4, columnspan=3, padx=5, pady=5)
        browseButton2 = Button(self.rightsideframe, text="Browse", padx=25, pady=5, command=lambda: directory_file(entryFile2, labelEntry2), fg="#000000", bg="#ffffff")
        browseButton2.grid(row=1, column=7, columnspan=2, padx=5, pady=5, sticky=W)
    # 3
        labelEntry3 = Label(self.rightsideframe, text="Configuration", bg="#ffffff")
        labelEntry3.grid(row=2, column=2, columnspan=2, padx=5, pady=5)
        entryFile3 = Entry(self.rightsideframe, font=12, width=40)
        entryFile3.grid(row=2, column=4, columnspan=3, padx=5, pady=5)
        browseButton3 = Button(self.rightsideframe, text="Browse", padx=25, pady=5, command=lambda: directory_file(entryFile3, labelEntry3), fg="#000000", bg="#ffffff")
        browseButton3.grid(row=2, column=7, columnspan=2, padx=5, pady=5, sticky=W)


        def run_algorithm(mode_selected):
            print("./darknet " + mode_selected.get() + " second parameter" + " third parameter ")

        startButton = Button(self.rightsideframe, text="Start", command=lambda:run_algorithm(mode_selected), padx=35, pady=6, fg="#ffffff", bg="#0066ff")
        startButton.grid(row=3, column=6, columnspan=2, padx=10, pady=10)

        exitButton = Button(self.rightsideframe, text="Exit", command= self.root.destroy ,padx=35, pady=6, fg="#ffffff", bg="#cc0000")
        exitButton.grid(row=3, column=8, columnspan=2, padx=10, pady=10)


    # functions that execute the YOLO's algorithm 
      



 
def main():
    
    root = Tk()
    root.geometry("+1200+600")
    root.title("Object detection")
    root.configure(background="#ffffff")
    
    App(root)
    App2(root, 'example1.mp4', 'example2.mp4')
    root.mainloop()


if __name__ == '__main__':

	main()
