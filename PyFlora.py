import tkinter as tk
from MainWindow import MainWindow
from EditWindow import EditWindow
from LoginWindow import LoginWindow
from Manage import Manage
from Profile import Profile
import Globals
from tkinter import messagebox

class PyFlora(tk.Tk):
    main = None
    profile = None
    manage = None
    login = None
    
    def __init__(self):
        super().__init__()
        ## Create window and center it
        self.title(Globals.TITLE)
        x = self.winfo_screenwidth() // 2
        y = int(self.winfo_screenheight() * 0.1)
        self.geometry(f'{Globals.WIDTH}x{Globals.HEIGHT}+{str(x)}+{y}')
        self.configure(bg="white")
        self.resizable(False,False)
        # Define the frames for each view
        self.frames = {
            "Login": tk.Frame(self),
            "Main": tk.Frame(self),
            "Edit": tk.Frame(self),
            "Profile": tk.Frame(self),
            "Manage": tk.Frame(self)
        }
        
        # Show login window
        self.showView("Login")

    def generateFrames(self, frameName):
        if frameName == "Login" and not self.login:
            self.login = LoginWindow(self)
        if frameName == "Main" and not self.main:
            self.main = MainWindow(self)
        if frameName == "Profile" and not self.profile:
            self.profile = Profile(self)
        if frameName == "Manage" and not self.manage:
            if Globals.isAdmin():
                self.manage = Manage(self)
            else:
                messagebox.showinfo("Information","Not authorized to access this resource!")
                return False
        return True

    def showView(self, view_name):
        if (self.generateFrames(view_name)):
            for view in self.frames.values():
                view.pack_forget()
            if view_name == "Main":
                self.main.refreshPlant(Globals.numPlants(),2)
            self.frames[view_name].pack(expand=True, fill="both")

    def showEdit(self, index):
        EditWindow(self, index)
        self.showView("Edit")

    def newPlant(self):
        EditWindow(self, 0, True)
        self.showView("Edit")

    def refreshPlant(self, index, special = 0):
        self.main.refreshPlant(index,special)

    def createContainer(self, frame):
        Container = tk.Frame(self.frames[frame], width=Globals.WIDTH, height=Globals.HEIGHT, bg=Globals.BG_COLOR)
        Container.pack(expand=True, fill="both")
        return Container

if __name__ == "__main__":
    app = PyFlora()
    app.mainloop()
