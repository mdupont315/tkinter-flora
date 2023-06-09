import tkinter as tk
from tkinter import ttk
import json
from PIL import ImageTk
from PIL import Image
from tkcalendar import Calendar
import datetime
from tkinter import filedialog as fd
from tkinter import messagebox
import os
import shutil
import Globals

class EditWindow():

    IMG_PATH = ""

    def __init__(self, parent, index, new_plant = False):
        
        def newPhoto():
            filetypes = (
                ('Image files', '*.png, *.jpg'),
                ('All files', '*.*')
            )
            src_file = fd.askopenfilename(title="Choose flower image", filetypes=filetypes)
            filename = os.path.basename(src_file)
            # specify the destination directory path
            dst_dir = './Images/'
            full_dst = os.path.abspath(dst_dir + filename).replace("\\", "/")
            if (src_file != full_dst):
                # copy the file to the destination directory
                shutil.copy(src_file, dst_dir)

            # get the filename of the copied file
            
            self.IMG_PATH = filename

            Globals.createImage(self.IMG_PATH, (200,200))

            plant_image.config(image=image)
            plant_image.image = image


        def mainWin(special):
            if new_plant:
                special = 1
            parent.refreshPlant(index, special)
            parent.showView("Main")

        def deletePlant():
            response = messagebox.askyesno("Delete Plant", "Are you sure you want to delete this?")
            if response:
                Globals.removePlant()
                mainWin(2)



        def updateView():
            name_edit.grid()
            name_static.grid_remove()
            pos_edit.grid()
            pos_static.grid_remove()
            soil_edit.grid()
            soil_static.grid_remove()
            bloom_edit.grid()
            bloom_static.grid_remove()
            frequency_edit.grid()
            frequency_static.grid_remove()
            details_edit.grid()
            details_static.grid_remove()
            picture_edit.grid()
            Update_Button.grid_remove()
            Save_Button.grid()
            Delete_Button.grid()

        def staticView():
            if updateJson() == -1:
                return
            if not new_plant:
                name_static.config(text=Globals.PLANT["name"])
                pos_static.config(text=Globals.PLANT["position"])
                soil_static.config(text=Globals.PLANT["soil"])
                bloom_static.config(text=Globals.PLANT["blooming_time"])
                details_static.config(text=Globals.PLANT["details"])
                frequency_str = Globals.PLANT["frequency"].split(" ")
                frequency_str = formatFrequency(frequency_str[0],frequency_str[1])
                frequency_static.config(text=frequency_str)
            name_static.grid()
            name_edit.grid_remove()
            pos_static.grid()
            pos_edit.grid_remove()
            soil_static.grid()
            soil_edit.grid_remove()
            bloom_static.grid()
            bloom_edit.grid_remove()
            details_static.grid()
            details_edit.grid_remove()
            picture_edit.grid_remove()
            frequency_static.grid()
            frequency_edit.grid_remove()
            Update_Button.grid()
            Save_Button.grid_remove()
            Delete_Button.grid_remove()


        def formatFrequency(freq_int, freq_per):
                if (len(freq_int) == 0):
                    freq_int = "1"
                if (freq_int == "1"):
                    freq_per = freq_per[:-1]
                return f"{freq_int} {freq_per}".strip()

        def updateJson():
            name = name_edit.get('1.0', tk.END).strip()
            pos = pos_edit.get('1.0', tk.END).strip()
            soil = soil_edit.get('1.0', tk.END).strip()
            bloom = bloom_edit.get('1.0', tk.END).strip()
            details = details_edit.get('1.0', tk.END).strip()
            path = self.IMG_PATH.strip()
            freq = f"{frequency_int.get()} {frequency_combo.get()}".strip()
            last_water = datetime.datetime.strptime(cal.get_date(), '%m/%d/%y').strftime('%Y-%m-%d').strip()

            elements = [name, pos, soil, bloom, details, path, freq, last_water]
            if any(element is None or element == "" for element in elements):
                messagebox.showerror("Error", "Please fill in all boxes and select an image")
                return -1
            Globals.PLANT["name"] = name
            Globals.PLANT["position"] = pos
            Globals.PLANT["soil"] =  soil
            Globals.PLANT["blooming_time"] = bloom
            Globals.PLANT["details"] = details
            Globals.PLANT["image_path"] = path
            Globals.PLANT["frequency"] = freq
            Globals.PLANT["last_watered"] = last_water

            
            Globals.updatePlant(index)

        parent.frames["Edit"] = tk.Frame(parent, bg=Globals.BG_COLOR)

        def newPlant():
            updateView()

        # create frame widget
        Container = parent.createContainer("Edit")

        Header = tk.Frame(Container, width=Globals.WIDTH, height=100, bg=Globals.ACCENT1)

        tk.Label(
                Header,
                text=Globals.TITLE,
                bg=Globals.ACCENT2,
                fg=Globals.TEXT,
                font=("TkMenuFont", 25),
            ).grid(row=0, column=0, sticky="w", padx=20, pady=10)

        name_static = tk.Label(
                Header,
                text="Plant Name",
                bg=Globals.ACCENT2,
                fg=Globals.TEXT,
                font=("TkMenuFont", 20),
                width=15
            )
        name_static.grid(row=0, column=1, sticky="e", padx=30, pady=15)
        
        name_edit = tk.Text(
                Header,
                bg=Globals.ACCENT2,
                fg=Globals.TEXT,
                font=("TkMenuFont", 20),
                width=15,
                height=1
            )
        
        name_edit.grid(row=0, column=1, sticky="e", padx=30, pady=15)
        name_edit.grid_remove()
        


        # Configure the first column to expand and fill any extra space
        Header.columnconfigure(0, weight=1)
        Header.pack(fill="x")

        scrollbar = tk.Scrollbar(Container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # create the canvas widget
        canvas = tk.Canvas(Container, width=Globals.WIDTH, height=Globals.HEIGHT-100, yscrollcommand=scrollbar.set, highlightthickness=0, bg=Globals.BG_COLOR)
        canvas.pack(side="left", fill="both", expand=True, padx=30)

        # create the frame inside the canvas widget
        Plant_Info = tk.Frame(canvas, bg=Globals.BG_COLOR, highlightthickness=0)
        Plant_Info.pack(fill="both", expand=True)


        tk.Label(
                Plant_Info,
                text="Planting Location",
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            ).grid(row=0, column=0, sticky="w", padx=30, pady=15)

        pos_static = tk.Label(
                Plant_Info,
                text= "Plant Postion",
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            )
        pos_static.grid(row=0, column=1, padx=10, sticky="w")

        pos_edit = tk.Text(
            Plant_Info,
            bg=Globals.BG_COLOR,
            fg=Globals.TEXT,
            height=2,
            width=20,
            font=("TkMenuFont", 15),
        )
        
        pos_edit.grid(row=0, column=1, sticky="w", pady=15)
        pos_edit.grid_remove()

        tk.Label(
                Plant_Info,
                text="Soil Type",
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            ).grid(row=1, column=0, sticky="w", padx=30, pady=15)

        
        soil_static = tk.Label(
                Plant_Info,
                text="Soil Type",
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            )
        soil_static.grid(row=1, column=1, sticky="w", padx=10, pady=15)

        soil_edit = tk.Text(
                Plant_Info,
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                height=2,
                width=20,
                font=("TkMenuFont", 15),
            )
        
        soil_edit.grid(row=1, column=1, sticky="w", pady=15)
        soil_edit.grid_remove()

        tk.Label(
                Plant_Info,
                text="Blooming Time",
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            ).grid(row=2, column=0, sticky="w", padx=30, pady=15)

        bloom_static = tk.Label(
                Plant_Info,
                text= "Blooming Time",
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            )
        bloom_static.grid(row=2, column=1, sticky="w", padx=10, pady=15)

        bloom_edit = tk.Text(
                Plant_Info,
                height=2,
                width=20,
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            )
        
        bloom_edit.grid(row=2, column=1, sticky="w", pady=15)
        bloom_edit.grid_remove()

        tk.Label(
                Plant_Info,
                text="Watering Frequency",
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            ).grid(row=3, column=0, sticky="w", padx=30, pady=15)


        frequency_str = "1 Day"

        frequency_static = tk.Label(
                Plant_Info,
                text=frequency_str,
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            )

        frequency_static.grid(row=3, column=1, sticky="w", padx=10, pady=15)

        frequency_edit = tk.Frame(Plant_Info, bg=Globals.BG_COLOR)


        def validate_input(new_value):
            if new_value == "":
                return True
            try:
                value = int(new_value)
                if value < 0 or value >= 100:
                    return False
            except ValueError:
                return False
            return True

        # create an Entry widget that only accepts numbers
        frequency_int = tk.Entry(
            frequency_edit,
            validate="key",
            bg=Globals.BG_COLOR,
            fg=Globals.TEXT,
            width=5,
            font=("TkMenuFont", 15),
        )
        frequency_int.insert(0, frequency_str.split(" ")[0])
        frequency_int['validatecommand'] = (frequency_int.register(validate_input), '%P')
        frequency_int.grid(row=0, column=0)

        # create a list of options for the combo box
        options = ['Days', 'Weeks']
        frequency_combo = ttk.Combobox(
            frequency_edit,
            values=options,
            background=Globals.BG_COLOR,
            foreground=Globals.TEXT,
            width=6,
            state='readonly'
            )
        frequency_combo.current(0 if frequency_str.split(" ")[1] in ["Days","Day"] else 1)
        frequency_combo.grid(row=0, column=1)

        frequency_edit.grid(row=3, column=1, sticky="w", pady=15)
        frequency_edit.grid_remove()

        tk.Label(
                Plant_Info,
                text="Details",
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            ).grid(row=4, column=0, sticky="w", padx=30, pady=15)

        details_static = tk.Label(
                Plant_Info,
                text="Details",
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
                wraplength=650
            )
        details_static.grid(row=5, column=0, columnspan=3, sticky="w", padx=40, pady=15)

        details_edit = tk.Text(
                Plant_Info,
                height=3,
                width=50,
                wrap=tk.WORD,
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            )
        details_edit.grid(row=4, column=0, columnspan=3, sticky="w", padx=(150, 15), pady=15)
        details_edit.grid_remove()


        plant_image = Globals.createImageFrame("./Assets/Question.png",(150, 150), Plant_Info, Globals.ACCENT1)
        plant_image.grid(row=0, column=2, rowspan=3, sticky="w", padx=(0,15))

        picture_edit = tk.Button(
                Plant_Info,
                text="Select Photo",
                bg=Globals.ACCENT2,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
                command=newPhoto
            )
        picture_edit.grid(row=3, column=2, sticky="w", pady=15)
        picture_edit.grid_remove()

        tk.Label(
                Plant_Info,
                text="Watering Calendar",
                bg=Globals.BG_COLOR,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
            ).grid(row=6, column=0, sticky="w", padx=30, pady=15)

        def waterPlant():
            today = datetime.date.today()
            cal.selection_set(today)
            Globals.PLANT["last_watered"] = today.strftime('%Y-%m-%d')
            Globals.updatePlant(index)


        tk.Button(
                Plant_Info,
                text="Water",
                bg=Globals.ACCENT2,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
                command=waterPlant
            ).grid(row=7, column=0, sticky="w", padx=30, pady=15)


        date = datetime.date.today()
        cal = Calendar(Plant_Info, selectmode='day', year=date.year, month=date.month, day=date.day)
        cal.grid(row=6, column=1, rowspan=2, sticky = "w", pady=15)

        Update_Button = tk.Button(
                Plant_Info,
                text="Update",
                bg=Globals.ACCENT2,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
                command=updateView
            )
        Update_Button.grid(row=6, column=2, sticky="w", padx=15, pady=15)

        Save_Button = tk.Button(
                Plant_Info,
                text="Save",
                bg=Globals.ACCENT2,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
                command=staticView
            )
        Save_Button.grid(row=6, column=2, sticky="w", padx=15, pady=15)
        Save_Button.grid_remove()

        tk.Button(
                Plant_Info,
                text="Back",
                bg=Globals.ACCENT2,
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
                command=lambda: Globals.parent.showView("Main")
            ).grid(row=7, column=2, sticky="w", padx=15, pady=15)
        
        Delete_Button = tk.Button(
                Plant_Info,
                text="Delete Plant",
                bg="red",
                fg=Globals.TEXT,
                font=("TkMenuFont", 15),
                command=deletePlant
            )
        Delete_Button.grid(row=8, column=1, sticky="w", padx=15, pady=15)
        Delete_Button.grid_remove()


        scrollbar.config(command=canvas.yview)
        canvas.create_window((0,0), window=Plant_Info, anchor="nw")
        Plant_Info.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))



        if new_plant:
            Globals.PLANT = {}
            index = Globals.numPlants()
            newPlant()
        else:
            Globals.getPlant(index)
            self.IMG_PATH = Globals.PLANT["image_path"]
            name_static.config(text=Globals.PLANT["name"])
            name_edit.insert(tk.END, Globals.PLANT["name"])
            pos_static.config(text=Globals.PLANT["position"])
            pos_edit.insert(tk.END, Globals.PLANT["position"])
            soil_static.config(text=Globals.PLANT["soil"])
            soil_edit.insert(tk.END, Globals.PLANT["soil"])
            bloom_static.config(text=Globals.PLANT["blooming_time"])
            bloom_edit.insert(tk.END, Globals.PLANT["blooming_time"])
            frequency_str = Globals.PLANT["frequency"].split(" ")
            frequency_str = formatFrequency(frequency_str[0], frequency_str[1])
            frequency_static.config(text=frequency_str)
            details_static.config(text=Globals.PLANT["details"])
            details_edit.insert(tk.END, Globals.PLANT["details"])
            image = Globals.createImage("./Images/"+Globals.PLANT["image_path"], (150,150))
            plant_image.config(image=image)
            plant_image.image = image
            date = datetime.datetime.strptime(Globals.PLANT["last_watered"], '%Y-%m-%d')
            cal.selection_set(date.date())



    