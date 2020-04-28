


######### Deprecated Soon will be removed  ################

import datetime
import os
import shutil
from time import sleep
from tkinter import *
from zipfile import ZipFile
from git import Repo
from MessageBox import messagebox
from platform import  system



class Updates():
    root = ""
    text = ""
    vsb = ""
    CONSOLE_BACKUP_FILE = "ConsoleBackup.zip"
    DELETE_COMMAND = ""

    def __init__(self):
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.resizable(0, 0)
        self.root.config(bg = "black")
        self.root.geometry('640x480')
        self.root.geometry(f"+{abs(4)}+{abs(4)}")

        Label(self.root, font = ("Courier bold", 20), text = "VISIOR Updation", width = "1080", fg = "#2ade2a",
              bg = "black").pack(side = "top")
        Button(self.root, font = ("Courier bold", 10), text = "\u274c", command = self.root.destroy, width = 4,
               bg = "black", fg = "red", borderwidth = 0, highlightthickness = 0, activebackground = "black",
               activeforeground = "white").place(relx = 0.91, rely = 0.0)

        self.text = Text(self.root, height = 26, width = 100, fg = "#2ade2a", bg = "black", borderwidth = 0,
                         font = ("Courier bold", 13),
                         highlightthickness = 0)
        self.vsb = Scrollbar(orient = "vertical")
        self.text.configure(yscrollcommand = self.vsb.set)
        self.vsb.pack(side = "right", fill = 'y')
        self.text.pack(side = "left")
        self.setDelCommand()



    def setDelCommand(self,root_dir = "VisiorNewUpdates"):
        os_info  =  system().lower()
        self.text.insert(END, f"->Platform Detected  :  {os_info} \n\n")
        self.text.yview_moveto(1)
        self.root.update()
        if "windows" in os_info:
            self.DELETE_COMMAND = 'rmdir /S /Q "{}"'.format(root_dir)
        else:
            self.DELETE_COMMAND = "rm -r {}".format(root_dir)

        return self.DELETE_COMMAND



    def CreateUpdate(self):
        files_dict = { }
        files_list = os.listdir("./")

        count = 0
        for file in files_list:
            if ".py" in file:
                files_dict[count] = file
                count += 1

        updates_files = input(f"Files With Update are ? \n{files_dict}\n-> ").split(" ")
        updates_files = [int(f) for f in updates_files]
        mode = int(input("1.Overwrite\t2.Append"))
        changelogs = open('UpdatedFiles.txt', "w+" if mode == 1 else "a")

        if mode == 2:
            changelogs.write("\n")

        for file in updates_files:
            update_string = files_dict[int(file)] + "=" + str(datetime.datetime.now())
            changelogs.write(update_string + "\n")
        print("Done Writing Updates...")
        changelogs.close()

    def replaceNewFiles(self, updates_to_be_installed, root_dir, install_button):

        try:
            install_button.destroy()
            self.root.update()
            self.text.insert(END, "\n\nCreated a Backup of old files \u2714 \n")
            self.text.yview_moveto(1)
            self.root.update()
            sleep(0.3)
            print(updates_to_be_installed)

            for i in updates_to_be_installed:
                if os.path.exists(i):
                    self.CONSOLE_BACKUP_FILE.write(i)
                    self.text.insert(END, f"Installing new {i} \n")
                    self.text.yview_moveto(1)
                    self.root.update()
                    shutil.copy(root_dir + "/" + i, os.getcwd())
                    sleep(0.3)
                    self.text.insert(END, f"Installed new {i} \u2714  \n")
                    self.text.yview_moveto(1)
                    self.root.update()
                    print(f"Installed new -> {i}")
                    print("Exixts")
                else:
                    self.text.insert(END, f"Installing new {i} \n")
                    self.text.yview_moveto(1)
                    self.root.update()
                    shutil.copy(root_dir + "/" + i, os.getcwd())
                    sleep(0.3)
                    self.text.insert(END, f"Installed new {i} \u2714  \n")
                    self.text.yview_moveto(1)
                    self.root.update()
                    print(f"Installed new -> {i}")

            shutil.copy(root_dir + "/UpdatedFiles.txt", os.getcwd())
            shutil.copy(root_dir + "/changelogs.vr", os.getcwd())
            sleep(0.5)
            messagebox("Updates Completed", "Updates Successfully Installed")
            os.system(self.DELETE_COMMAND)#'rmdir /S /Q "{}"'.format(root_dir))


        except Exception as e:
            messagebox("Updates Failed", f"The Error is due to {e}")
            os.system(self.DELETE_COMMAND)#'rmdir /S /Q "{}"'.format(root_dir))

    def CheckUpdate(self):
        try:
            new_update_file = "VisiorNewUpdates"
            if os.path.exists(new_update_file):
                os.system(self.DELETE_COMMAND)#'rmdir /S /Q "{}"'.format(new_update_file))
                self.text.insert(END, "Existing Update file removed\nGetting New Files ...\n")
                self.text.yview_moveto(1)
                self.root.update()
                Repo.clone_from("http://github.com/lllSniperlyfelll/Visior", branch = "VisiorConsole",
                                to_path = new_update_file)
                self.text.insert(END,
                                 "Checked update files \u2714 \n")
                self.text.yview_moveto(1)
                self.vsb.update()

                local_UpdateFile = open("UpdatedFiles.txt", "r")
                remote_UpdateFile = open(new_update_file + "/UpdatedFiles.txt", "r")
                changelogs = open(new_update_file + "/changelogs.vr", "r")
                changelogs_text = changelogs.read()
                changelogs.close()

            else:
                self.text.insert(END, "Checking if Update is avaliable \n")
                self.text.yview_moveto(1)
                self.root.update()
                Repo.clone_from("http://github.com/lllSniperlyfelll/Visior", branch = "VisiorConsole",
                                to_path = new_update_file)
                self.text.insert(END,
                                 "Checked update files \u2714 \n")
                self.text.yview_moveto(1)
                self.vsb.update()

                local_UpdateFile = open("UpdatedFiles.txt", "r")
                remote_UpdateFile = open(new_update_file + "/UpdatedFiles.txt", "r")
                changelogs = open(new_update_file + "/changelogs.vr", "r")
                changelogs_text = changelogs.read()
                changelogs.close()

            local_file_list = local_UpdateFile.read().split("\n")
            local_file_dict = { }

            for local_file in local_file_list:
                temp = local_file.split("=")
                if len(temp) >= 2:
                    local_file_dict[temp[0]] = temp[1]

            remote_file_list = remote_UpdateFile.read().split("\n")
            remote_file_dict = { }
            for remote_file in remote_file_list:
                temp = remote_file.split("=")
                if len(temp) >= 2:
                    remote_file_dict[temp[0]] = temp[1]

            local_UpdateFile.close()
            remote_UpdateFile.close()

            updates_to_be_installed = []
            for key, val in remote_file_dict.items():
                if local_file_dict.get(key) == None:
                    updates_to_be_installed.append(key)
                else:
                    if not val == local_file_dict.get(key):
                        updates_to_be_installed.append(key)

            if len(updates_to_be_installed) >= 1:
                if self.CONSOLE_BACKUP_FILE in os.listdir():
                    os.system(self.setDelCommand(self.CONSOLE_BACKUP_FILE))#'rmdir /S /Q "{}"'.format(self.CONSOLE_BACKUP_FILE))

                self.CONSOLE_BACKUP_FILE = ZipFile("ConsoleBackup.zip", "w")
                self.text.insert(END, "Updates Avaliable  \n\n")
                self.text.yview_moveto(1)

                self.text.insert(END, changelogs_text)

                self.root.update()

                btn = Button(self.root, font = ("Courier bold", 11), text = "Install Updates", width = 10, fg = "black",
                             bg = "#2ade2a", borderwidth = 0, highlightthickness = 0, activebackground = "black",
                             activeforeground = "white",
                             command = lambda: self.replaceNewFiles(updates_to_be_installed, new_update_file, btn))
                btn.place(relx = 0.8, rely = 0.93)


            else:
                sleep(0.3)
                messagebox("Updates Completed", "Latest Updates Already Installed ... :)")
                os.system(self.DELETE_COMMAND)

            self.root.mainloop()



        except Exception as e:
            print(f"error fetching dir {e}")
            e = str(e)
            if "git" in e:
                str_l = e.split("fatal")
                messagebox("Updates Failed", "fatal :" + str_l[1])
            else:
                messagebox("Updates Failed", e)


if __name__ == "__main__":
    if os.path.exists("VisiorNewUpdates"):
        os.system('rmdir /S /Q "{}"'.format("VisiorNewUpdates"))
    Updates().CreateUpdate()
