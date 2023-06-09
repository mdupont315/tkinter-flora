import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import Globals

class Manage:
    def __init__(self, parent):
        
        
        #if not Globals.isAdmin():
        #    messagebox.showinfo("Information","You are not allowed here")
        #    return
        
        


        def refreshTable():
            for child in Table.winfo_children():
                    child.destroy()
            createTable()

        def updatePlant(event, username, details):
            selected_item = event.widget.get()
            new_plant = selected_item.split(" (")[0]
            details[username]["plants"] = new_plant
            Globals.writeJson(details, Globals.USERS_PATH)
            if (username) == Globals.USERNAME:
                Globals.readUser(username)
                Globals.readPlantData()
            



        def createTable():

            def deleteUser(username):
                response = messagebox.askyesno("Delete User", f"Are you sure you want to delete {username}?")
                if not response:
                    return
                if (Globals.deleteUser(username)):
                    refreshTable()
                

            user_data = Globals.readJson(Globals.USERS_PATH)
            Table.pack()

            tk.Label(Table, text="Name", bg=Globals.ACCENT1, fg=Globals.TEXT, font=("TkMenuFont", 20)).grid(row=0, column=0)
            tk.Label(Table, text="Role", bg=Globals.ACCENT1, fg=Globals.TEXT, font=("TkMenuFont", 20)).grid(row=0, column=1)
            tk.Label(Table, text="Plant File", bg=Globals.ACCENT1, fg=Globals.TEXT, font=("TkMenuFont", 20)).grid(row=0, column=2)
            tk.Label(Table, text="Actions", bg=Globals.ACCENT1, fg=Globals.TEXT, font=("TkMenuFont", 20)).grid(row=0, column=3, columnspan=2)

            # Display user data in the grid
            i = 0
            for username, details in user_data.items():
                tk.Label(Table, text=username, bg=Globals.ACCENT1, fg=Globals.TEXT, font=("TkMenuFont", 15)).grid(row=i+1, column=0)

                plant_files = Globals.getPlantFiles()
                plant_combo = ttk.Combobox(Table, values=plant_files, background=Globals.BG_COLOR, foreground=Globals.TEXT, font=("TkMenuFont", 15), width=18)
                plant_combo.current(plant_files.index(details["plants"]))
                plant_combo.grid(row=i+1, column=1)
                plant_combo.bind("<<ComboboxSelected>>", lambda event, username=username, details=user_data: updatePlant(event, username, details))

                if username is not Globals.USERNAME:
                    role_combobox = ttk.Combobox(Table, values=["user","admin"], background=Globals.BG_COLOR, foreground=Globals.TEXT, font=("TkMenuFont", 15), width=6)
                    role_combobox.current(0)
                    if details['role'] == 'admin':
                        role_combobox.current(1)
                    role_combobox.grid(row=i+1, column=2)
                    
                else:
                    tk.Label(Table, text=details['role'], bg=Globals.ACCENT1, fg=Globals.TEXT, font=("TkMenuFont", 15)).grid(row=i+1, column=2)
                tk.Button(Table, text="Reset Password", bg=Globals.ACCENT2, fg=Globals.TEXT, font=("TkMenuFont", 15), command=lambda username = username: createPopup("Reset Password", 1, username)).grid(row=i+1, column=3, padx=10, pady=10)
                
                
                delete_user = tk.Button(Table,  text="Delete User", bg="Red", fg=Globals.TEXT, font=("TkMenuFont", 15), command=lambda: deleteUser(username))
                if (username == Globals.USERNAME):
                    delete_user.configure(state="disabled")
                delete_user.grid(row=i+1, column=4, padx=10, pady=10)
                i += 1

        def back():
            parent.showView("Profile")
        
            
        def createPopup(title, mode=0, user=None):

            def verify(user = None):
                password = password_entry.get()

                if mode == 0:
                    user = username_entry.get()
                    if not user:
                        messagebox.showinfo(title, "Passwords do not match!")
                        return
                
                    
                if not password:
                    messagebox.showinfo(title, "Passwords do not match!")
                    return
                if password_entry.get() != password_verify.get():
                    messagebox.showinfo(title, "Passwords do not match!")
                    return

                user_data = Globals.readJson(Globals.USERS_PATH) 
                if mode == 0:
                    
                    if user in user_data:
                        messagebox.showinfo("New User", "User already exists!")
                        return
                    
                    tmp_USERNAME = Globals.USERNAME
                    Globals.createUser(user, password)
                    Globals.readUser(tmp_USERNAME)
                    refreshTable()
                else:
                    user_data[user]["password"] = password
                    Globals.writeJson(user_data, Globals.USERS_PATH)
                    messagebox.showinfo(title, f"{user}'s password has been updated")
                popup.destroy()
                
            popup = tk.Toplevel()

            popup.title(title)
            x = parent.winfo_screenwidth() // 2
            y = int(parent.winfo_screenheight() * 0.1)
            popup.geometry(f"400x500+{x}+{y}")
            popup.config(bg=Globals.BG_COLOR)
            
            label = tk.Label(popup, text=title, font=("TkMenuFont", 20), bg=Globals.BG_COLOR, fg=Globals.TEXT)
            label.pack()

            if (mode == 0):
                tk.Label(popup, text="Username: ", bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMenuFont", 12)).pack(pady=10)
                username_entry = tk.Entry(popup, font=("TkMenuFont", 12))
                username_entry.pack(pady=5)

            tk.Label(popup, text="Password: ", bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMEnuFont", 12)).pack(pady=10)
            password_entry = tk.Entry(popup, show="*", font=("TkMenuFont", 12))
            password_entry.pack(pady=5)

            tk.Label(popup, text="Confirm Password: ", bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMEnuFont", 12)).pack(pady=10)
            password_verify = tk.Entry(popup, show="*", font=("TkMenuFont", 12))
            password_verify.pack(pady=5)

            if (mode == 0):
                role_frame = tk.Frame(popup, bg=Globals.BG_COLOR)
                role_frame.pack(pady=10)
                tk.Label(role_frame, text="Role: ", bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMEnuFont", 12)).grid(column=0, row=0, padx=10, pady=10)
                role_combobox = ttk.Combobox(role_frame, values=["user","admin"], background=Globals.BG_COLOR, foreground=Globals.TEXT, font=("TkMenuFont", 15), width=6)
                role_combobox.current(0)
                role_combobox.grid(column=1, row=0, padx=10, pady=10)
            
            button_frame= tk.Frame(popup, bg=Globals.BG_COLOR)
            button_frame.pack(pady=15)
            tk.Button(button_frame, text="Save", font=("TkMenuFont", 15), command=lambda: verify(user)).grid(column=0, row=0, padx=10, pady=10)
            tk.Button(button_frame, text="Close", font=("TkMenuFont", 15), command=popup.destroy).grid(column=1, row=0, padx=10, pady=10)
            
            popup.grab_set()
            
            
        Container = parent.createContainer("Manage")
        # Create grid labels
        tk.Label(Container, text="User Manager", bg=Globals.BG_COLOR, fg=Globals.TEXT, font=("TkMenuFont", 25)).pack(fill="x", pady=25)

        Table = tk.Frame(Container, bg=Globals.ACCENT1, padx=25, pady=25)
        createTable()

        Buttons = tk.Frame(Container, bg=Globals.BG_COLOR)
        Buttons.pack(pady=15)
        # Create buttons
        tk.Button(Buttons, text="Add User", bg=Globals.ACCENT2, fg=Globals.TEXT, font=("TkMenuFont", 15), command=lambda: createPopup("New User")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(Buttons, text="Back", bg=Globals.ACCENT2, fg=Globals.TEXT, font=("TkMenuFont", 15), command=back).grid(row=1, column=1, padx=10, pady=10)




