from platform import system
from time import sleep, time
from tkinter import *

import cv2
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
from PIL import Image, ImageTk

import RPi.GPIO as gpio
from src.Drivers.MotorDriver import *
from src.Modules.MessageBox import messagebox
from src.Modules.settings import SensorSettings, Settings


class SensorsTest:
    TestWindow = ""
    TestHistory = ""
    TestHistory_Scroll = ""
    ThreadList = []
    checkbox_vals = ""
    multiple_tests = ""
    checkbox_calls_labels = ""
    next_call_allowed = True
    
    FrontIRPin = ""
    BottomIRPin = ""

    settings_ = ""
    
    HirozontalPan = ""
    VerticalPan = ""
    
    HorizontalPanPin = ""
    VerticalPanPin = ""

    def __init__(self):
        if system().lower() == 'windows':
            messagebox("Error ", "Cannot Execute -> Needed Platform Raspbian ")
            exit()

        else:


            self.settings_ = Settings()
            self.TestWindow = Tk()
            self.TestWindow.overrideredirect(
            self.settings_.isOverRideAlloweded())  # if plf.system().lower() == 'windows' else self.window.wm_attributes("-type","splash")
            self.TestWindow.resizable(0, 0)
            self.TestWindow.config(bg = self.settings_.getBgColor())
            self.TestWindow.geometry(self.settings_.getResolution())
            self.TestWindow.geometry(f"+{abs(4)}+{abs(4)}")
            ###### GPIO SETUP#########
            self.settings_ = SensorSettings()
            
            self.FrontIRPin = self.settings_.FRONT_IR_PIN
            self.BottomIRPin = self.settings_.BOTTOM_IR_PIN

            
            gpio.setmode(gpio.BCM)
            gpio.setup(self.FrontIRPin, gpio.IN)
            gpio.setup(self.BottomIRPin, gpio.IN)
            
            
            self.HorizontalPanPin = self.settings_.HORIZONTAL_LOOK
            self.VerticalPanPin = self.settings_.VERTICAL_LOOK
            
            gpio.setup(self.settings_.VERTICAL_LOOK,gpio.OUT)
            gpio.setup(self.settings_.HORIZONTAL_LOOK,gpio.OUT)
            
            self.VerticalPan = gpio.PWM(self.settings_.VERTICAL_LOOK, 100)
            self.HorizontalPan = gpio.PWM(self.settings_.HORIZONTAL_LOOK, 100)
            
            InitilaizePins()
            

        
        
        
        

    def RedirectCallTo(self, id):
        if id == 0:
            print("front usonic test")
            self.UltraSonicSensorTest(id, "Front_UltraSonic_Sensor")
            print("Bottom usonic text")
            self.UltraSonicSensorTest(id, "Bottom_UltraSonic_Sensor")
        elif id == 1:# and self.next_call_allowed:
            self.InfraredSensorTest(id, "Bottom")
        elif id == 2 :#and self.next_call_allowed:
            self.VideoTest(id)
        elif id == 3 :#and self.next_call_allowed:
            self.MotorsTest(id)
        elif id == 4 :#and self.next_call_allowed:
            self.CameraMovementTest(id)

    def TestController(self, checkbox_vals, multiple_tests, checkbox_calls_labels):
        self.checkbox_vals = checkbox_vals.copy()
        self.checkbox_calls_labels = checkbox_calls_labels.copy()
        Header = Label(self.TestWindow, font = ("Courier bold", 12), text = "Testing",
                       width = len("  VISIOR'S On Board Sensor Test"),
                       fg = "#2ade2a",
                       bg = "black")
        Header.pack(side = "top")

        if multiple_tests == True:
            latch = False

            for i in range(len(checkbox_vals)):
                print(checkbox_vals[i].get())
                if checkbox_vals[i].get() == 1:
                    Header.configure(
                        text = "Started " + self.checkbox_calls_labels.get(i)[1].split("\n")[1].replace(")",
                                                                                                        "") + "Test")
                    Header.update()
                    if latch == False:
                        self.TestHistory = Text(self.TestWindow, height = 30, width = 40, fg = "#2ade2a", bg = "black",
                                                borderwidth = 0, highlightthickness = 0)
                        self.TestHistory_Scroll = Scrollbar(orient = "vertical", bg = "red", relief = "flat", width = 9)
                        self.TestHistory.configure(yscrollcommand = self.TestHistory_Scroll.set)
                        self.TestHistory_Scroll.pack(side = "right", fill = "y")
                        self.TestHistory.pack(side = "top", pady = 17, fill = "x")
                        self.TestHistory_Scroll.config(command = self.TestHistory.yview)
                        latch = True
                    self.RedirectCallTo(i)
            Button(self.TestWindow, font = ("Courier bold", 9), text = "\u274c", command = self.TestWindow.destroy,
                   width = 4, bg = "black",
                   fg = "red",
                   borderwidth = 0, highlightthickness = 0, activebackground = "black",
                   activeforeground = "white").place(relx = 0.91, rely = 0.0)
            messagebox("Test Result", "Tests Completed !")


        else:
            for i in range(len(checkbox_vals)):
                print(checkbox_vals[i].get())
                if checkbox_vals[i].get() == 1:
                    Button(self.TestWindow, font = ("Courier bold", 9), text = "\u274c",
                           command = self.TestWindow.destroy, width = 4, bg = "black",
                           fg = "red",
                           borderwidth = 0, highlightthickness = 0, activebackground = "black",
                           activeforeground = "white").place(relx = 0.91, rely = 0.0)
                    Label(self.TestWindow, font = ("Courier bold", 12),
                          text = "Started " + checkbox_calls_labels.get(i)[1].split("\n")[1].replace(")", "") + "Test",
                          width = len("  VISIOR'S On Board Sensor Test"),
                          fg = "#2ade2a",
                          bg = "black").pack(side = "top")
                    self.TestHistory = Text(self.TestWindow, height = 30, width = 40, fg = "#2ade2a", bg = "black",
                                            borderwidth = 0, highlightthickness = 0)
                    self.TestHistory_Scroll = Scrollbar(orient = "vertical", bg = "red", relief = "flat", width = 9)
                    self.TestHistory.configure(yscrollcommand = self.TestHistory_Scroll.set)
                    self.TestHistory_Scroll.pack(side = "right", fill = "y")
                    self.TestHistory.pack(side = "top", pady = 17, fill = "x")
                    self.TestHistory_Scroll.config(command = self.TestHistory.yview)
                    self.RedirectCallTo(i)
                    messagebox("Test Result",
                               checkbox_calls_labels.get(i)[1].split("\n")[1].replace(")", "") + " Tests Completed !")
                    break
        self.TestWindow.mainloop()

    def UltraSonicSensorTest(self, id, Sensor):
        if(Sensor=="Front_UltraSonic_Sensor"):
            ECHO_PIN = 23
            TRIGGER_PIN = 24
            min_distance = 70
        else:
            ECHO_PIN = 12
            TRIGGER_PIN = 16
            min_distance = 10

        start_time=time()
        sensor_distance_sum = 0
        final_distance = 0
        test_status_flag = False
        SensorObject = DistanceSensor(echo=ECHO_PIN,trigger=TRIGGER_PIN,max_distance=1000,pin_factory=PiGPIOFactory())
        self.TestHistory.config(fg = "red")
        self.TestHistory.delete(1.0, END)
        self.TestHistory.update()
        self.TestHistory.insert(END, "Starting " + Sensor + "Test \n")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        self.TestHistory.config(fg = "#2ade2a")
        
        tout = self.settings_.getTestTimeOut()
        
        while time() - start_time < tout // 2:
            sensor_distance_sum=sensor_distance_sum+SensorObject.distance
            self.TestHistory.insert(END, Sensor +  ">>> Test Distance %f" % (SensorObject.distance*100) + "......... Completed  \n")
            self.TestHistory.yview_moveto(1)
            self.TestWindow.update()
            sleep(1)
            
        final_distance=sensor_distance_sum/SensorObject.distance
        if(final_distance%SensorObject.distance==0):
            test_status_flag = True
            self.TestHistory.insert(END, Sensor + ">>> is not working OR is Damaged \n")
            self.TestHistory.yview_moveto(1)
            self.TestWindow.update()
        else:
            test_status_flag = False
            self.TestHistory.insert(END, Sensor + ">>> is working Fine :) \n")
            self.TestHistory.yview_moveto(1)
            self.TestWindow.update()
            
    
    def InfraredSensorTest(self, id, _Sensor):
        PinRead = 5
        gpio.setup(PinRead,gpio.IN)
        test_init_text = '''Please Keep and Remove Objects in ''' + _Sensor + ''' of IRSensor to complete the test\nStarting IR Test.......\n'''
        start_time = time()
        data_sum = 0
        test_status_flag = False
        self.TestHistory.config(fg = "red")
        self.TestHistory.delete(1.0, END)
        self.TestHistory.update()
        self.TestHistory.insert(END, test_init_text)
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        self.TestHistory.config(fg = "#2ade2a")
        sleep(0.5)
        i = 0
        self.TestHistory.insert(END, ">>> Please Bring Object Near to Sensor \n")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        sleep(5)
        tout = self.settings_.getTestTimeOut()
        while time() - start_time < tout // 2:
            data_sum += gpio.input(PinRead)
            print(data_sum)
            self.TestHistory.insert(END, _Sensor + " IRSensor Test Iteration   %d  - val : %d" % (
            i, data_sum) + "......... Completed  \n")
            self.TestHistory.yview_moveto(1)
            sleep(0.5)
            self.TestWindow.update()
            i += 1

        if data_sum < 5:
            self.next_call_allowed = True
            test_status_flag = True
        else:
            self.next_call_allowed = False
            test_status_flag = False

        self.TestHistory.insert(END, ">>> Now Please Keep Object Far from Sensor \n")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        sleep(5)
        start_time = time()
        while time() - start_time < tout // 2:
            data_sum += gpio.input(PinRead)
            print(data_sum)
            self.TestHistory.insert(END, _Sensor + " IRSensor Test Iteration   %d  - val : %d" % (
            i, data_sum) + "......... Completed  \n")
            self.TestHistory.yview_moveto(1)
            sleep(0.5)
            self.TestWindow.update()
            i += 1
        if data_sum > 0:
            self.next_call_allowed = False
            test_status_flag = True
        else:
            self.next_call_allowed = False
            test_status_flag = False

        if test_status_flag == True:
            self.TestHistory.insert(END, _Sensor + " Ir Sensor Test Completed Succesfully  ")
            self.TestHistory.yview_moveto(1)
            sleep(0.5)
            self.TestWindow.update()
        else:
            self.TestHistory.config(fg = "red")
            self.TestHistory.insert(END, _Sensor + " Ir Sensor Test Failed\nEither Sensor in Disconnected or Damaged  ")
            self.TestHistory.yview_moveto(1)
            sleep(0.5)
            self.TestWindow.update()

    def VideoTest(self, id):
        self.TestHistory.delete("1.0", END)
        self.TestHistory.update()
        img=get_Frame()
        if(cv2.show(img)):
            self.TestHistory.insert(END, "Video test Successful.........\n")
            self.TestHistory.yview_moveto(1)
            sleep(0.06)
            self.TestWindow.update()

        #for i in range(100):
         #   self.TestHistory.insert(END, "Video test %d" % (i) + ".........\n")
          #  self.TestHistory.yview_moveto(1)
           # sleep(0.06)
            #self.TestWindow.update()

    def MotorsTest(self, id):
        self.TestHistory.delete("1.0", END)
        self.TestHistory.update()
        MoveForward()
        self.TestHistory.insert(END, "Forward Motion test is Successful.........\n")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        sleep(4)
        MoveBackward()
        self.TestHistory.insert(END, "Backward Motion test is Successful.........\n")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        sleep(4)
        MoveRight()
        self.TestHistory.insert(END, "Right Motion test is Successful.........\n")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        sleep(4)
        MoveLeft()
        self.TestHistory.insert(END, "Left Motion test is Successful.........\n")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        sleep(4)
        
        ResetMotorPins()
        #for i in range(100):
         #   self.TestHistory.insert(END, "Motors test %d" % (i) + ".........\n")
          #  self.TestHistory.yview_moveto(1)
           # sleep(0.06)
            #self.TestWindow.update()
            

    def CameraMovementTest(self, id):
        self.TestHistory.delete("1.0", END)
        self.TestHistory.update()
        
        test_init_text = '''Do Not Touch or Hold the Module while test is running\nor this might damage the module\nStarting Camera Pan Test.......\n'''
        self.TestHistory.insert(END, test_init_text)
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        
        sleep(10)
        
        
        self.VerticalPan.start(0)
        self.HorizontalPan.start(0)
        
        gpio.output(self.VerticalPanPin,True)
        gpio.output(self.HorizontalPanPin , True)
        
        self.TestHistory.insert(END, "Horizontal Position Reset... ")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        self.HorizontalPan.ChangeDutyCycle(200/22+2)
        sleep(0.5)
        
        self.TestHistory.insert(END, "Vertical Position Reset... ")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        self.VerticalPan.ChangeDutyCycle(150/16+2)
        sleep(0.5)
        
        
        self.TestHistory.insert(END, "\nRunning Turning Test ...\n>>>Started Right Pan Test ... ")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        for duty in range(0,23,1):
            self.TestHistory.insert(END, f"\nTurning Right with Duty Cycle Value {duty}...")
            self.TestHistory.yview_moveto(1)
            self.TestWindow.update()
            self.HorizontalPan.ChangeDutyCycle(duty)
            self.VerticalPan.ChangeDutyCycle(duty)
            sleep(0.5)
                
        print("Switch ...")
        self.TestHistory.insert(END, "\n>>>Started Left Pan Test ... ")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        for duty in range(23,-1,-1):
            print("- duty cycle")
            self.TestHistory.insert(END, f"\nTurning Left with Duty Cycle Value {duty}...")
            self.TestHistory.yview_moveto(1)
            self.TestWindow.update()
            self.HorizontalPan.ChangeDutyCycle(duty)
            self.VerticalPan.ChangeDutyCycle(duty)
            sleep(0.5)
        
        self.TestHistory.insert(END, "\nHorizontal Position Reset... ")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        self.HorizontalPan.ChangeDutyCycle(200/22+2)
        sleep(1)
        
        self.TestHistory.insert(END, "\nVertical Position Reset... ")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        self.VerticalPan.ChangeDutyCycle(150/16+2)
        sleep(1)
        
        self.VerticalPan.stop()
        self.HorizontalPan.stop()
        
        
        
        self.TestHistory.insert(END, "\nTest Completed")
        self.TestHistory.yview_moveto(1)
        self.TestWindow.update()
        
        
        messagebox("Test Results","Test Completed !")
        

        #for i in range(100):
         #   self.TestHistory.insert(END, "Camera Movement test %d" % (i) + ".........\n")
          #  self.TestHistory.yview_moveto(1)
           # sleep(0.06)
            #self.TestWindow.update()
