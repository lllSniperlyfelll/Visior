# Patched .cfg connection for cam self.frame dims

import os
from tkinter import Button, Label, Tk

import cv2
from PIL import Image, ImageTk
from pynput import keyboard as py_key

from src.Drivers.CameraPanDriver import CameraPanDriver
from src.Drivers.CaughtDetection import CaughtDetection
from src.Drivers.MotorDriver import *
from src.Drivers.UltrasonicDriver import UltraSonicControl
from src.Modules.MessageBox import *
from src.Modules.settings import *
from src.Services.cloudService import *
from src.Services.Security.fileZipper import *

if not os.path.exists("Snapshots"):
    os.system("mkdir Snapshots")





# from CameraMotion import CameraMotion


#########################################   check for screen shots alerady existing before saving new one ############################# 


class RcModeController:
    window = ""
    vid = ""
    width = 0
    height = 0
    canvas = ""
    delay = 15
    photo = ""
    snapshot = ""
    image_count = 0
    CamUp = ""
    CamDown = ""
    CamLeft = ""
    CamRight = ""
    MoveForward = ""
    MoveBackward = ""
    TurnLeft = ""
    TurnRight = ""
    CamMotion = ""
    ground_connect = ""
    usonicControl = ""

    AreaClearStr = "\u2714 " + "Front Area Clear"
    ObstacleStr = "\u26A0 " + "Object Detected In Front Of Me"

    GroundContactTrue = "\u2714 " + " Ground Contact True"
    GroundContactNegative = "\u26A0 " + "Ground Contact Negative"
    CamPanObject = ""
    CaughtObject = ""

    filesChanged = False
    recordVideo = False
    out = ""
    
    def __init__(self):
        try:
            InitilaizePins()
            print("Motors init")
            self.usonicControl = UltraSonicControl()
            settings_ = Settings()
            self.window = Tk()
            self.window.overrideredirect(
            settings_.isOverRideAlloweded())  # if plf.system().lower() == 'windows' else self.window.wm_attributes("-type","splash")
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

            # self.CamMotion = CameraMotion()
            # self.CamMotion.ResetCameraPosition()
            self.notification = Label(self.window, font = ("Courier bold", 12),
                                      text = "\u26A0 " + "Loading ...", width = 30,
                                      fg = "white",
                                      bg = "black")
            self.notification.place(relx = 0.5, rely = 0.57)

            self.ground_connect = Label(self.window, font = ("Courier bold", 12),
                                        text = "\u26A0 " + "Loading ...", width = 30,
                                        fg = "white",
                                        bg = "black")
            self.ground_connect.place(relx = 0.5, rely = 0.63)

            self.CamPanObject = CameraPanDriver()
            self.CaughtObject = CaughtDetection()
            
            #if(not os.path.exists("./SnapShots")):
                #print("Making SS dir")
                #os.mkdir("./SnapShots")
            self.caughtMonitor()
            self.distanceAlert()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter('Snapshots\output.mkv',fourcc, 30.0, (640,480))
            self.ReadPresentImages()
        except Exception as e:
            print(f"Exception in <Function> __init__ - <Class> RcModeController - <File> TkinterCam.py --> {e}")
            self.shutAll()
            pass
    
    
    def distanceAlert(self):
        try:
            warningSign, usonicData = self.usonicControl.checkArea()
            if(warningSign):
                self.ground_connect.config(fg = "#2ade2a", text = str(usonicData) + " cm")
            else:
                self.ground_connect.config(fg = "red", text = str(usonicData) + " cm")
            self.ground_connect.update()
            #print("Distance check")
            self.window.after(100, self.distanceAlert)
        except:
            self.shutAll()
            print("Distance alert exception")
            
    def caughtMonitor(self):
        try:
            detection_status = self.CaughtObject.onGround()
            if detection_status == True:
                self.notification.config(fg = "#2ade2a", text = self.GroundContactTrue)
                self.notification.update()
            else:
                self.notification.config(fg = "red", text = self.GroundContactNegative)
                self.notification.update()
            #print("Caught check")    
            self.window.after(100, self.caughtMonitor)
        except:
            self.shutAll()
            print("Caught check exception")
        
    def ReadPresentImages(self):
        self.image_count =len(os.listdir("./Snapshots/"))

    def on_press(self, key):
        b_g = "black"
        f_g = "red"
        # border_w = 3

        if str(format(key)) == "'w'":
            self.CamPanObject.PanUp()
        elif str(format(key)) == "'s'":
            self.CamPanObject.PanDown()
        elif str(format(key)) == "'a'":
            self.CamPanObject.PanLeft()
        elif str(format(key)) == "'d'":
            self.CamPanObject.PanRight()
        elif str(format(key)) == "Key.up":
            MoveForward()
        elif str(format(key)) == "Key.down":
            MoveBackward()
        elif str(format(key)) == "Key.left":
            MoveLeft()
        elif str(format(key)) == "Key.right":
            MoveRight()
        else:
            ResetMotorPins()

    def on_release(self, key):
        pass

    def closeAll(self):
        self.shutAll()
        self.window.destroy()
        
        
    def StreamScreen(self):
        try:

            self.vid = cv2.VideoCapture(0)
            print("Opencv init ..")
            print("Key Listener started .. ")

            Label(self.window, font = ("Courier bold", 20), text = "VISIOR'S On Board Camera Stream", width = "1080",
                  fg = "#2ade2a",
                  bg = "black").pack(side = "top")
            Button(self.window, font = ("Courier bold", 10), text = "\u274c", command = self.closeAll, width = 4,
                   bg = "black",
                   fg = "red",
                   borderwidth = 0, highlightthickness = 0, activebackground = "black",
                   activeforeground = "white").place(relx = 0.91, rely = 0.0)
            Button(self.window, font = ("Courier bold", 11), text = "\u25A3 " + "Snapshot", command = self.SaveFrame,
                   width = 10,
                   bg = "#00e6b8",
                   fg = "black",
                   borderwidth = 3, highlightthickness = 0, activebackground = "black",
                   activeforeground = "white", relief = "ridge").place(relx = 0.013, rely = 0.57)
            Button(self.window, font = ("Courier bold", 11), text = "\u25CF " + "Record", command = self.controlVideoRecording,
                   width = 10,
                   bg = "black",
                   fg = "#00e6b8",
                   borderwidth = 3, highlightthickness = 0, activebackground = "black",
                   activeforeground = "white", relief = "ridge").place(relx = 0.013 * 2 + 0.15, rely = 0.57)

            self.CreateCameraButtons()
            self.CreateMovementButton()

            self.canvas = Label(self.window, width = CameraSettings().getCamFrameDim("width"),
                                height = CameraSettings().getCamFrameDim("height"), bg = "black")
              
            #self.canvas = Label(self.window, width = 60,height = 10, bg = "black")
            self.canvas.pack()


            self.update()
            listerner = py_key.Listener(
                on_press = self.on_press,
                on_release = self.on_release
            )
            listerner.start()
            
            
            self.window.mainloop()

        except Exception as e:
            self.shutAll()
            print(f"Exception in <Function> StreamScreen - <Class> RcModeController - <File> TkinterCam.py --> {e}")
            pass

    def controlVideoRecording(self):
        self.recordVideo = not self.recordVideo
        print("Vedio recording -> ", self.recordVideo)

    def SaveFrame(self):
        try:
            print("saved ")
            self.image_count += 1
            SSpath = "./Snapshots/s"+str(self.image_count)+ str(hashlib.sha256(str(self.image_count).encode()).hexdigest()) + ".jpg"
            cv2.imwrite(SSpath, cv2.cvtColor(self.snapshot, cv2.COLOR_BGR2RGB))
            #self.filesChanged = True
            if(self.cloudObject.__CloudAvaliable__):
                self.cloudObject.readyPush(SSpath)
                os.system("rm "+SSpath)
            else:
                print("No Cloud Avaliable ...")
                zipIt(SSpath)
        except Exception as e:
            self.shutAll()
            print(f"Exception in <Function> SaveFrame - <Class> RcModeController - <File> TkinterCam.py --> {e}")
            pass

    def get_Frame(self):
        try:
            if self.vid.isOpened():
                ret, self.frame = self.vid.read()
                shape = self.frame.shape
                #print("Frame shape ->",shape)
                #fx=1.4 , fy=0.9
                #280,130
                if self.recordVideo:
                    self.out.write(self.frame)
                    print(self.out)
                    print("Recording")
                return ret, cv2.cvtColor(cv2.resize(self.frame, (shape[0], shape[1]//2),fx = 5, fy = 0.9), cv2.COLOR_BGR2RGB)        
        except Exception as e:
            self.shutAll()
            print(f"Exception in <Function> get_Frame - <Class> RcModeController - <File> TkinterCam.py --> {e}")
            pass

    def update(self):
        try:
            ret, self.frame = self.get_Frame()
            self.snapshot = self.frame
            if ret:
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.frame))
                self.canvas.configure(image = self.photo)
                self.canvas.image = self.photo
            self.window.after(10, self.update)
        except Exception as e:
            self.shutAll()
            print(f"Exception in <Function> update - <Class> RcModeController - <File> TkinterCam.py --> {e}")
            pass

    def CreateCameraButtons(self):

        self.CamUp = Button(self.window, font = ("Courier bold", 15), text = "Ⓦ", width = 4,
                            fg = "#2ade2a",
                            bg = "black",
                            borderwidth = 0, highlightthickness = 0, activebackground = "black",
                            activeforeground = "white")
        self.CamUp.place(relx = 0.25, rely = 0.72)
        self.CamRight = Button(self.window, font = ("Courier bold", 15), text = "Ⓓ", width = 4,
                               fg = "#2ade2a",
                               bg = "black",
                               borderwidth = 0, highlightthickness = 0, activebackground = "black",
                               activeforeground = "white")
        self.CamRight.place(relx = 0.343, rely = 0.79)
        self.CamDown = Button(self.window, font = ("Courier bold", 15), text = "Ⓢ", width = 4,
                              fg = "#2ade2a",
                              bg = "black",
                              borderwidth = 0, highlightthickness = 0, activebackground = "black",
                              activeforeground = "white")
        self.CamDown.place(relx = 0.25, rely = 0.82)
        self.CamLeft = Button(self.window, font = ("Courier bold", 15), text = "Ⓐ", width = 4,
                              fg = "#2ade2a",
                              bg = "black",
                              borderwidth = 0, highlightthickness = 0, activebackground = "black",
                              activeforeground = "white")
        self.CamLeft.place(relx = 0.16, rely = 0.79)
        Label(self.window, font = ("Arial bold", 7), justify = "left",
              text = "W : Look Up\n\nS : Look Down\n\nA : Look Left\n\nD : Look Right",
              width = len(" Camera Control "),
              fg = "#00e6b8",
              bg = "black").place(relx = 0.0, rely = 0.73)

        Label(self.window, font = ("Courier bold", 12), text = "Camera Control", width = len(" Camera Control "),
              fg = "white",
              bg = "black").place(relx = 0.132 + 0.04, rely = 0.89)

    def CreateMovementButton(self):

        self.MoveForward = Button(self.window, font = ("Courier bold", 16), text = "\u2191", width = 4,
                                  bg = "black",
                                  fg = "red",
                                  borderwidth = 0, highlightthickness = 0, activebackground = "black",
                                  activeforeground = "white")
        self.MoveForward.place(relx = 0.7, rely = 0.72)
        self.MoveBackward = Button(self.window, font = ("Courier bold", 16), text = "\u2193", width = 4,
                                   bg = "black",
                                   fg = "red",
                                   borderwidth = 0, highlightthickness = 0, activebackground = "black",
                                   activeforeground = "white")
        self.MoveBackward.place(relx = 0.7, rely = 0.8)
        self.TurnLeft = Button(self.window, font = ("Courier bold", 16), text = "\u2190", width = 4,
                               bg = "black",
                               fg = "red",
                               borderwidth = 0, highlightthickness = 0, activebackground = "black",
                               activeforeground = "white")
        self.TurnLeft.place(relx = 0.62, rely = 0.8)
        self.TurnRight = Button(self.window, font = ("Courier bold", 16), text = "\u2192", width = 4,
                                bg = "black",
                                fg = "red",
                                borderwidth = 0, highlightthickness = 0, activebackground = "black",
                                activeforeground = "white")
        self.TurnRight.place(relx = 0.78, rely = 0.8)
        Label(self.window, font = ("Arial bold", 7), justify = "left",
              text = "Up Key : Forward\n\nDown Key : Back\n\nLeft Key : Left\n\nRight Key : Right",
              width = len(" Camera Control "),
              fg = "#00e6b8",
              bg = "black").place(relx = 0.86, rely = 0.73)

        Label(self.window, font = ("Courier bold", 12), text = "Motion Control", width = len(" Camera Control "),
              fg = "white",
              bg = "black").place(relx = 0.63, rely = 0.89)
    

    def shutAll(self):
        print("Stopped Video")
        self.out.release()
        self.vid.release()
        zipIt()
        
    def __del__(self):
        print("Stopped Video")
        self.out.release()
        self.vid.release()
        zipIt()

if __name__ == "__main__":
    RcModeController().StreamScreen()
