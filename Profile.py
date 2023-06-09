import tkinter as tk
from tkinter import messagebox
import Globals

class Profile:
    def __init__(self, parent):
        
        def mainWin():
            parent.showView("Main")

        def manageUser():
            parent.showView("Manage")

        # Login Button widget
        def update_user():
            if new_pass.get() == confirm_pass.get():
                Globals.updatePass(current_pass.get(), new_pass.get())
            else:
                messagebox.showinfo("Information","Provided passwords don't match")
            
        Container = parent.createContainer("Profile")

        username_label = tk.Label(Container, text=Globals.USERNAME, bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMenuFont", 25))
        username_label.pack(pady=(50,10))

        tk.Label(Container, text="Current Password: ", bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMEnuFont", 12)).pack(pady=10)
        current_pass = tk.Entry(Container, show="*", font=("TkMenuFont", 12))
        current_pass.pack(pady=5)

        tk.Label(Container, text="New Password: ", bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMEnuFont", 12)).pack(pady=10)
        new_pass = tk.Entry(Container, show="*", font=("TkMenuFont", 12))
        new_pass.pack(pady=5)

        tk.Label(Container, text="Verify Password: ", bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMEnuFont", 12)).pack(pady=10)
        confirm_pass = tk.Entry(Container, show="*", font=("TkMenuFont", 12))
        confirm_pass.pack(pady=5)


        button_frame = tk.Frame(
            Container, 
            bg=Globals.BG_COLOR
        )
        button_frame.pack(expand=True, pady=5)

        tk.Button(
            button_frame,
            text="Update",
            font=("TkHeadingFont", 20),
            bg=Globals.ACCENT2,
            fg=Globals.TEXT,
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=update_user
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="Back",
            font=("TkHeadingFont", 20),
            bg=Globals.ACCENT2,
            fg=Globals.TEXT,
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=mainWin
        ).grid(row=0, column=1, padx=10)

        if (Globals.isAdmin()):
            tk.Button(
                button_frame,
                text="Manage Users",
                font=("TkHeadingFont", 20),
                bg=Globals.ACCENT2,
                fg=Globals.TEXT,
                cursor="hand2",
                activebackground="#badee2",
                activeforeground="black",
                command=manageUser
            ).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        
