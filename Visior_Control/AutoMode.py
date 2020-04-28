# Patched .cfg connection for cam frame dims

import os
from tkinter import Button, Label, Tk

import cv2
from PIL import Image, ImageTk

# from IrTestStub import GroundConnect, IrTestStub
from src.Modules.settings import CameraSettings, Settings


# from CameraMotion import CameraMotion

class AutoModeController:
    window = ""
    vid = ""
    width = 0
    height = 0
    canvas = ""
    delay = 15
    photo = ""
    snapshot = ""
    image_count = 0


    def __init__(self):
        try:
            settings_ = Settings()
            self.window = Tk()
            self.window.overrideredirect(
                settings_.isOverRideAlloweded())
            self.window.geometry(settings_.getResolution())
            self.window.resizable(0, 0)
            self.window.config(bg = settings_.getBgColor())
            w_height, w_width = 640, 490

            width = self.window.winfo_screenwidth()
            height = self.window.winfo_screenheight()
            print(f"width x height -> {width}x{height}")
            self.window.geometry(f"+{abs(0)}+{abs(0)}")
            self.width = 620  # self.window.winfo_screenwidth()
            self.height = 620  # self.window.winfo_screenheight()
            print(f"width x height -> {360}x{360}")
            self.window.focus()

            self.notification = Label(self.window, font = ("Courier bold", 12),
                                      text = "Time: " + "2:40 PM", width = 30,
                                      fg = "white",
                                      bg = "black")
            self.notification.place(relx = 0.5, rely = 0.57)

            self.ground_connect = Label(self.window, font = ("Courier bold", 12),
                                        text = "Now At:  " + "19.2183 N 72.9781 E ", width = 30,
                                        fg = "#00e6b8",
                                        bg = "black")
            self.ground_connect.place(relx = 0.2, rely = 0.63)
            self.ground_connect = Label(self.window, font = ("Courier bold", 12),
                                        text = "Destination:  " + "29.2343 N 43.9731 E ", width = 30,
                                        fg = "red",
                                        bg = "black")
            self.ground_connect.place(relx = 0.2, rely = 0.69)



        except Exception as e:
            print(f"Exception in <Function> __init__ - <Class> RcModeController - <File> TkinterCam.py --> {e}")
            pass


    def ReadPresentImages(self):
        imglist = os.listdir("./Snapshots/")[-1]
        first_split = imglist.split("_")
        second_split = first_split[1].split(".")
        self.image_count = int(second_split[0])
        print(f"image_counter -> {self.image_count}")

    def StreamScreen(self):
        try:
            self.vid = cv2.VideoCapture(0)
            print("Opencv init ..")
            Label(self.window, font = ("Courier bold", 20), text = "VISIOR'S On Board Camera Recording", width = "1080",
                  fg = "#2ade2a",
                  bg = "black").pack(side = "top")
            Button(self.window, font = ("Courier bold", 10), text = "\u274c", command = self.window.destroy, width = 4,
                   bg = "black",
                   fg = "red",
                   borderwidth = 0, highlightthickness = 0, activebackground = "black",
                   activeforeground = "white").place(relx = 0.91, rely = 0.0)
            Button(self.window, font = ("Courier bold", 11), text = "\u25A3 " + "Snapshot", command = self.SaveFrame,
                   width = 10,
                   bg = "#00e6b8",
                   fg = "black",
                   borderwidth = 3, highlightthickness = 0, activebackground = "black",
                   activeforeground = "white", relief = "ridge").place(relx = 0.005, rely = 0.57)


            self.canvas = Label(self.window, width = CameraSettings().getCamFrameDim("width"),
                                height = CameraSettings().getCamFrameDim("height"), bg = "blue")
            self.canvas.pack()

            self.update()
            self.window.mainloop()

        except Exception as e:
            print(f"Exception in <Function> StreamScreen - <Class> AutoModeController - <File> AutoMode.py --> {e}")
            pass


    def SaveFrame(self):
        try:
            self.image_count += 1
            SSpath = "./SnapShots/snapshot_" + str(self.image_count) + ".jpg"
            cv2.imwrite(SSpath, cv2.cvtColor(self.snapshot, cv2.COLOR_BGR2RGB))
            SavedLoc = Label(self.window, font = ("Courier bold underline", 12),
                             text = f"Snapshot Saved in -> {SSpath}",
                             width = "1080",
                             fg = "white", bg = "black")
            SavedLoc.pack(side = "bottom")
            self.window.after(1000, SavedLoc.forget)
        except Exception as e:
            print(f"Exception in <Function> SaveFrame - <Class> RcModeController - <File> TkinterCam.py --> {e}")
            pass

    def get_Frame(self):
        try:
            if self.vid.isOpened():
                ret, frame = self.vid.read()
                return ret, cv2.cvtColor(cv2.resize(frame, None, fx = 0.9, fy = 1.4), cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"Exception in <Function> get_Frame - <Class> AutoModeController - <File> AutoMode.py --> {e}")
            pass

    def update(self):
        try:
            ret, frame = self.get_Frame()
            self.snapshot = frame
            if ret:
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
                self.canvas.configure(image = self.photo)
                self.canvas.image = self.photo
            self.window.after(1000, self.update)
        except Exception as e:
            print(f"Exception in <Function> update - <Class> AutoModeController - <File> AutoMode.py --> {e}")
            pass


if __name__ == "__main__":
   AutoModeController().StreamScreen()
