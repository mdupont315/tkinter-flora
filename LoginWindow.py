import tkinter as tk
import Globals


class LoginWindow:
    def __init__(self, parent):
        Globals.parent = parent
        Container = parent.createContainer("Login")
        # Create the image
        login_image = Globals.createImageFrame("./Assets/LoginIcon.png", (200,200), Container)
        login_image.grid(column=0, row=0)

        #Configure grid centering
        Container.grid_rowconfigure(0, weight=1)
        Container.grid_columnconfigure(0, weight=1)
        Container.grid_columnconfigure(1, weight=1)

        form = tk.Frame(Container, bg=Globals.BG_COLOR)
        form.grid(column=1, row=0)

        tk.Label(
            form,
            text="Please Login",
            bg=Globals.BG_COLOR,
            fg=Globals.TEXT,
            font=("TkMenuFont", 14),
        ).pack()

        def verifyLogin(username, password):
            Globals.readUser(username)
            valid = Globals.isUser(username) and Globals.verifyPass(password)
            if not valid:
                Globals.USER = None
                Globals.CONFIG = None
            return valid

        # Login Button widget
        def validateLogin():
            username = username_entry.get()
            password = password_entry.get()

            if verifyLogin(username, password):
                Globals.USERNAME = username
                parent.showView("Main")
            else:
                login_error_label.config(text="Incorrect username or password")

        def registerUser():
            username = username_entry.get()
            password = password_entry.get()

            if not username.strip():
                login_error_label.config(text="Username Not Set")
            elif not password.strip():
                login_error_label.config(text="Password Not Set")
            elif not Globals.isUser(username):
                login_error_label.config(text="User with that username already exists")
            else:
                Globals.createUser(username, password)
                parent.showView("Main")
            
        username_label = tk.Label(
            form, text="Username: ", bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMenuFont", 12))
        username_label.pack(pady=10)
        username_entry = tk.Entry(form, font=("TkMenuFont", 12))
        username_entry.pack(pady=5)

        password_label = tk.Label(
            form, text="Password: ", bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMEnuFont", 12))
        password_label.pack(pady=10)
        password_entry = tk.Entry(form, show="*", font=("TkMenuFont", 12))
        password_entry.pack(pady=5)

        button_frame = tk.Frame(form, bg=Globals.BG_COLOR)
        button_frame.pack(pady=20)

        login_button = tk.Button(
            button_frame,
            text="Login",
            font=("TkHeadingFont", 20),
            bg=Globals.ACCENT2,
            fg=Globals.TEXT,
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=validateLogin
        )
        login_button.grid(column=0, row=0, padx=10)

        login_button = tk.Button(
            button_frame,
            text="Register",
            font=("TkHeadingFont", 20),
            bg=Globals.ACCENT2,
            fg=Globals.TEXT,
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=registerUser
        )
        login_button.grid(column=1, row=0, padx=10)

        login_error_label = tk.Label(
            form, text="", bg=Globals.BG_COLOR, fg="red", font=("TkMenuFont", 12))
        login_error_label.pack()
