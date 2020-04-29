from  tkinter import *
from src.Modules.settings import Settings
from src.Modules.MessageBox import messagebox
from src.Modules.Testing.SensorTest import SensorsTest


# import Console as CC


class SystemTest():
    SysWindow = ""
    win_width = ""
    win_height = ""
    max_boxes = 5
    recCount = 0
    checkbox_vals = [0, 0, 0, 0, 0]
    checkbox_calls_labels = { 0: ["fsonic", "This Will Carry out Tests on \nUltrasonic Sensor"],
                              1: ["bsonic", "This Will Carry out Tests on \nBottom Infrared Sensor"],
                              2: ["motors", "This Will Carry out Tests on \nThe Driving Motors"],
                              3: ["camerapan", "This Will Carry out Tests on \nThe Camera Moment \nModule"] }

    def __init__(self):
        if True:
            settings_ = Settings()
            self.SysWindow = Tk()
            self.SysWindow.overrideredirect(
                settings_.isOverRideAlloweded())  # if plf.system().lower() == 'windows' else self.window.wm_attributes("-type","splash")
            self.SysWindow.resizable(0, 0)
            self.SysWindow.config(bg = settings_.getBgColor())
            self.SysWindow.geometry(settings_.getResolution())
            self.win_width = 600
            self.win_height = 400
            self.SysWindow.geometry(f"+{abs(0)}+{abs(0)}")

            Button(self.SysWindow, font = ("Courier bold", 10), text = "\u274c", command = self.SysWindow.destroy,
                   width = 4,
                   bg = "black",
                   fg = "red",
                   borderwidth = 0, highlightthickness = 0, activebackground = "black",
                   activeforeground = "white").place(relx = 0.91, rely = 0.0)

            # Button(self.SysWindow, font = ("Courier bold", 13), text = "\u25c0 Back", command = self.Back,
            #      width = 7,
            #     bg = "black",
            #    fg = "#2ade2a",
            #   borderwidth = 0, highlightthickness = 0, activebackground = "black",
            #  activeforeground = "white").place(relx = 0.0, rely =0.93)

            for IntVars_ in range(0, self.max_boxes):
                self.checkbox_vals[IntVars_] = IntVar()
            print(f"Check Box init -> {self.checkbox_vals}")
            self.MainMenu()
            print("System Test Menu Init")

    def MainMenu(self):
        try:
            print("Creating ManinMenu System Test")
            Label(self.SysWindow, font = ("Courier bold", 15), text = "VISIOR'S On Board Sensor Test",
                  width = len("VISIOR'S On Board Sensor Test"),
                  fg = "#2ade2a",
                  bg = "black").pack(side = "top")
            Label(self.SysWindow, font = ("Courier bold", 9),
                  text = "Select the Component to be tested\nClick 'Start Tests' button to begin \n ''you can also run multpile tests''",
                  width = self.win_width,
                  fg = "#00e6b8",
                  bg = "black").pack(side = "top")

            Button(self.SysWindow, font = ("Cambria bold", 13), text = "Start Tests >>", width = len("Start Tests >>"),
                   highlightthickness = 0, bg = "black",
                   fg = "#00e6b8", borderwidth = 3, command = self.getCheckBoxState, activebackground = "black",
                   activeforeground = "white", relief = "ridge").pack(side = "bottom", pady = 5)

            self.CreateCheckBar()
            print("Creating ManinMenu System Test DOne !!!")
            self.SysWindow.mainloop()
        except Exception as e:
            print(f"Exception in <Function> MainMenu - <Class> SystemTest - <File> SystemTest.py --> {e}")
            pass

    def CreateCheckBar(self):
        y_pos_start = 0.25

        for checkboxes in range(0, self.max_boxes):
            if checkboxes <= 2:
                x_pos_start = 0.15
            else:
                x_pos_start = 0.6
            if checkboxes == 3:
                y_pos_start = 0.25

            check_box_text = self.checkbox_calls_labels.get(checkboxes)[1].split("\n")[1].replace(")", "")
            Checkbutton(self.SysWindow, text = check_box_text, variable = self.checkbox_vals[checkboxes], fg = "red",
                        font = ("Courier bold", 10),
                        bg = "black", borderwidth = 0, highlightthickness = 0, activebackground = "black",
                        activeforeground = "white").place(relx = x_pos_start, rely = y_pos_start)
            Label(self.SysWindow, font = ("Courier bold", 9), justify = "left",
                  text = self.checkbox_calls_labels.get(checkboxes)[1], width = len("This Will Run Test son   "),
                  fg = "#00e6b8",
                  bg = "black").place(relx = x_pos_start, rely = y_pos_start + 0.06)
            y_pos_start += 0.23

    def getCheckBoxState(self):
        print(len(self.checkbox_vals))

        sum_check = 0
        for i in range(len(self.checkbox_vals)):
            sum_check += self.checkbox_vals[i].get()

        if sum_check == 0:
            messagebox("Cannot Run Tests", "No Option Selected For Test \n'Select Atleast one option'")
        else:
            self.SysWindow.destroy()
            SensorsTest().TestController(self.checkbox_vals, not sum_check == 1, self.checkbox_calls_labels)
            messagebox("Tests Completed", "Tests Completed Successfully ")
            SystemTest().MainMenu()

            # self.SysWindow.after(3000, self.SysWindow.destroy)


if __name__ == "__main__":
    St = SystemTest()
    St.MainMenu()
