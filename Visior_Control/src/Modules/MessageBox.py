from tkinter import Button, Entry, Label, Tk

from src.Modules.settings import *
from src.Services.Security.fileZipper import *


def messagebox(title, info,font_size = 12):
    settings_ = Settings()

    info_box = Tk()
    info_box.focus_set()
    info_box.geometry(f"+{100}+{100}")

    info_box.geometry("470x270")
    info_box.configure(bg = settings_.getBgColor(), highlightbackground = "white", highlightthickness = 2)
    info_box.resizable(0, 0)
    Button(info_box, font = ("Courier bold", 10), text = "\u274c", command = info_box.destroy, width = 3,
           fg = "red",
           bg = "black",
           borderwidth = 0, highlightthickness = 0, activebackground = "black", activeforeground = "white").place(
        relx = 0.91, rely = 0.01)
    info_box.overrideredirect(settings_.isOverRideAlloweded())

    Label(info_box, text = "\u26A0 " + title, fg = "#2ade2a", bg = "black", font = ("times bold", 14)).pack(
        side = "top", pady = 20)
    Label(info_box, text = info, fg = "#2ade2a", bg = "black", font = ("times bold", font_size), wraplength = 450).pack(
        side = "top",
        pady = 50)

    info_box.mainloop()



def inputBox():
    settings_ = Settings()

    input_box = Tk()
    input_box.focus_set()
    input_box.geometry(f"+{100}+{100}")

    input_box.geometry("470x270")
    input_box.configure(bg = settings_.getBgColor(), highlightbackground = "white", highlightthickness = 2)
    input_box.resizable(0, 0)
    Button(input_box, font = ("Courier bold", 10), text = "\u274c", command = input_box.destroy, width = 3,
           fg = "red",
           bg = "black",
           borderwidth = 0, highlightthickness = 0, activebackground = "black", activeforeground = "white").place(
        relx = 0.91, rely = 0.01)
    input_box.overrideredirect(settings_.isOverRideAlloweded())

    Label(input_box, text = "\u26A0 Unlock files" , fg = "#2ade2a", bg = "black", font = ("times bold", 14)).pack(
        side = "top", pady = 20)
    Label(input_box, text = "Enter unlock key", fg = "#2ade2a", bg = "black", font = ("times bold", 12), wraplength = 450).pack(
        side = "top",
        pady = 20)
    passwordInput = Entry(input_box, show = "$", width=70)
    passwordInput.pack(
        side = "top",
        pady = 20)

    Button(input_box, font = ("Cambria bold", 11), text = "Unlock", width = 10, fg = "#00e6b8", bg = "black",
        borderwidth = 3, highlightthickness = 0, command = lambda: callValidator(passwordInput.get()) , activebackground = "black",
        activeforeground = "white", relief = "ridge").pack(side = "bottom",pady = 10)

    input_box.mainloop()


def callValidator(inputData):
    print(inputData)
    if keyValidator().validateKey(inputData):
        messagebox("Done", "Files unlocked")
    else:
        messagebox("Error","Error in unlocking")
