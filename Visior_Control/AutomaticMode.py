# Patched .cfg connection for cam self.frame dims

import os
from tkinter import Button, Label, Tk

import cv2
from PIL import Image, ImageTk
from pynput import keyboard as py_key

#from src.Drivers.CameraPanDriver import CameraPanDriver
#from src.Drivers.CaughtDetection import CaughtDetection
#from src.Drivers.MotorDriver import *
#from src.Drivers.UltrasonicDriver import UltraSonicControl
from src.Modules.MessageBox import *
from src.Modules.settings import *
from src.Services.cloudService import *
from src.Services.Security.fileZipper import *
from src.Services.cloudService import *
import datetime

if not os.path.exists("Snapshots"):
    os.system("mkdir Snapshots")





# from CameraMotion import CameraMotion




class AutomaticMode:
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
    timeLabel = ""


    CamPanObject = ""
    CaughtObject = ""

    filesChanged = False
    recordVideo = False
    out = ""
    cloudObject = ""
    
    def __init__(self):
        try:
            #InitilaizePins()
            print("Motors init")
            #self.usonicControl = UltraSonicControl()
            settings_ = Settings()
            self.window = Tk()
            self.window.overrideredirect(
            settings_.isOverRideAlloweded())  # if plf.system().lower() == 'windows' else self.window.wm_attributes("-type","splash")
            self.window.geometry(settings_.getResolution())
            self.window.resizable(0, 0)
            self.window.title("Automatic Mode")
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
                                      text = "\u26A0 " + "Ultrasonic data Loading ...", width = 30,
                                      fg = "white",
                                      bg = "black")
            self.notification.place(relx = 0.5, rely = 0.57)

            self.ground_connect = Label(self.window, font = ("Courier bold", 12),
                                        text = "\u26A0 " + self.GroundContactTrue, width = 30,
                                        fg = "white",
                                        bg = "black")
            self.ground_connect.place(relx = 0.5, rely = 0.65)
            self.timeLabel =  Label(self.window, font = ("Courier bold", 12),
                                        text = "Time-  " + self.GroundContactTrue, width = 30,
                                        fg = "white",
                                        bg = "black")
            self.timeLabel.place(relx = 0.5, rely = 0.74)
            #self.CamPanObject = CameraPanDriver()
            #self.CaughtObject = CaughtDetection()
            
            #self.caughtMonitor()
            #self.distanceAlert()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.out = cv2.VideoWriter('Snapshots\output.mkv',fourcc, 30.0, (640,480))
            self.cloudObject = ""#cloudService()
            self.ReadPresentImages()
        except Exception as e:
            print(f"Exception in <Function> __init__ - <Class> AutomaticMode - <File> TkinterCam.py --> {e}")
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

    def closeAll(self):
        self.shutAll()
        self.window.destroy()
        
        
    def StreamScreen(self):
        try:

            self.vid = cv2.VideoCapture(0)
            
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

            self.canvas = Label(self.window, width = CameraSettings().getCamFrameDim("width"),
                                height = CameraSettings().getCamFrameDim("height"), bg = "black")
              
            self.canvas.pack()
            self.update()
            self.window.mainloop()

        except Exception as e:
            self.shutAll()
            print(f"Exception in <Function> StreamScreen - <Class> AutomaticMode - <File> TkinterCam.py --> {e}")
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
            '''if(self.cloudObject.__CloudAvaliable__):
                self.cloudObject.readyPush(SSpath)
                os.system("rm "+SSpath)
            else:'''
            print("No Cloud Avaliable ...")
            zipIt(SSpath)
        except Exception as e:
            self.shutAll()
            print(f"Exception in <Function> SaveFrame - <Class> AutomaticMode - <File> TkinterCam.py --> {e}")
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
            print(f"Exception in <Function> get_Frame - <Class> AutomaticMode - <File> TkinterCam.py --> {e}")
            pass

    def update(self):
        try:
            ret, self.frame = self.get_Frame()
            self.snapshot = self.frame
            if ret:
                self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.frame))
                self.canvas.configure(image = self.photo)
                self.canvas.image = self.photo

                self.timeLabel.config(text = "Time - "+datetime.datetime.now().strftime("%H:%M:%S%p"))
                self.timeLabel.update()
            self.window.after(10, self.update)
        except Exception as e:
            self.shutAll()
            print(f"Exception in <Function> update - <Class> AutomaticMode - <File> TkinterCam.py --> {e}")
            pass


    def shutAll(self):
        pass
        '''print("Stopped Video")
        self.out.release()
        self.vid.release()
        zipIt()'''
        
    '''def __del__(self):
        print("Stopped Video")
        self.out.release()
        self.vid.release()
        zipIt()'''

if __name__ == "__main__":
    AutomaticMode().StreamScreen()
