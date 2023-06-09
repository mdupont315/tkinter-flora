import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from PIL import Image
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from tkinter import messagebox
import Globals


class MainWindow():
    inner_frame = None
    parent = None
    plant = None
    NewPlantBox = None
    canvas = None
    scrollbar = None
    API_KEY = "22d7e6fe89684cd0a99124511232805"

    def generatePlantBox(self, image_path, flower_name, index):
        PlantBox = tk.Frame(self.inner_frame, width=300,
                            height=200, bg=Globals.ACCENT1)
        PlantBox.grid(row=index % 2, column=index//2, pady=20, padx=40)

        image = Globals.createImageFrame(image_path, (150, 150), PlantBox)
        image.grid(row=0, column=0, rowspan=3)
        image.bind("<Button-1>", lambda event: self.updatePlant(event, index))

        tk.Label(
            PlantBox,
            text=flower_name,
            bg=Globals.ACCENT1,
            fg=Globals.TEXT,
            name="flower_name",
            font=("TkMenuFont", 15),
        ).grid(row=0, column=1, sticky="nw", padx=10, pady=10, columnspan=2)

        PlantStatus = tk.Frame(PlantBox, bg=Globals.ACCENT1,
                               height=200, name="status_frame")
        PlantStatus.grid(row=1, column=1, sticky="s", padx=10, pady=20)
        PlantBox.rowconfigure(1, weight=1)

        tk.Label(
            PlantStatus,
            text="Status",
            bg=Globals.ACCENT1,
            fg=Globals.TEXT,
            font=("TkMenuFont", 10),
        ).grid(row=0, column=0, sticky="sw")

        status_code, status_img = self.checkPlantStatus(index)

        status = tk.Label(
            PlantStatus,
            text=status_code,
            bg=Globals.ACCENT1,
            fg=Globals.TEXT,
            name="status_code",
            font=("TkMenuFont", 10),
        ).grid(row=1, column=0, sticky="sw")

        icon = tk.Label(
            PlantBox,
            image=status_img,
            bg=Globals.ACCENT1,
            fg=Globals.TEXT,
            name="status_img",
        )
        icon.image = status_img
        icon.grid(row=1, column=2, sticky="es", rowspan=2, padx=10, pady=10)

        PlantBox.columnconfigure(1, weight=1)
        PlantBox.columnconfigure(1, weight=1)
        PlantBox.bind(
            "<Button-1>", lambda event: self.updatePlant(event, index))

    def showWateringChart(self, root):
        chart_window = tk.Toplevel(root)
        chart_window.title("Watering Chart")
        plants = [plant["name"] for plant in Globals.PLANT_DATA]
        days_since_watered = [(datetime.now() - datetime.strptime(plant.get("last_watered", "1900-01-01"), "%Y-%m-%d")).days for plant in Globals.PLANT_DATA]

        # Table
        table = ttk.Treeview(chart_window, columns=(
            "Plant", "Last Watered"), show="headings")
        table.heading("Plant", text="Plant")
        table.heading("Last Watered", text="Last Watered")
        table.column("Plant", width=150)
        table.column("Last Watered", width=150)

        for plant in Globals.PLANT_DATA:
            table.insert("", tk.END, values=(plant["name"], plant.get("last_watered", "N/A")))

        table.pack(pady=20)

        # Plot
        fig, ax = plt.subplots()
        y_pos = range(len(plants))
        ax.plot(y_pos, days_since_watered)
        ax.set_xticks(y_pos)
        ax.set_xticklabels(plants, rotation=45)
        ax.set_title("Days Since Last Watered")
        ax.set_ylabel("Days Past")
        ax.set_xlabel("Plants")
        fig.subplots_adjust(left=0.2, bottom=0.5, right=0.9, top=0.9)
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def checkPlantStatus(self, index):
        # get last watered date

        Globals.getPlant(index)
        last_watered = Globals.PLANT["last_watered"]
        frequency = Globals.PLANT["frequency"]

        watered_date = datetime.strptime(last_watered, '%Y-%m-%d')
        future_date = watered_date
        if 'day' in frequency:
            days = int(frequency.split()[0])
            future_date = watered_date + timedelta(days=days)
        elif 'week' in frequency:
            weeks = int(frequency.split()[0])
            future_date = watered_date + timedelta(weeks=weeks)

        status_code = "good"
        status_path = ""
        days_passed = (datetime.now() - future_date).days
        if days_passed <= 0:
            status_code = 'good'
            status_path = "./Assets/Thumbs_Up.png"
        elif days_passed <= 7:
            status_code = 'okay'
            status_path = "./Assets/Question.png"
        else:
            status_code = 'bad'
            status_path = "./Assets/Bad.png"
        # Check frequency

        # return status and image
        return status_code, Globals.createImage(status_path, (50, 50))

    def updateScrollbar(self):
        self.canvas.update()
        if self.canvas.xview()[1] == 1.0:
            self.scrollbar.pack_forget()
        else:
            self.scrollbar.pack(fill="x", side="bottom")

    def refreshPlant(self, index, Special=0):

        if Special == 2:
            for widget in self.inner_frame.winfo_children():
                widget.destroy()
            self.generatePlantBoxes()
            self.generateNewPlantBox()
            return

        numPlants = Globals.numPlants()
        if index >= numPlants:
            return

        Globals.updatePlant(index)

        if (Special == 1):
            self.NewPlantBox.grid_remove()
            self.generatePlantBox(
                "./"+Globals.PLANT["image_path"], Globals.PLANT["name"], index)
            i = numPlants
            self.NewPlantBox.grid(row=i % 2, column=i//2, pady=20, padx=40)
            return

        row = index // 2
        col = index % 2
        self.parent = self.inner_frame.grid_slaves(row=row, column=col)[0]
        for name, child in self.parent.children.items():
            if name == "flower_img":
                fImg = child
            elif name == "flower_name":
                fName = child
            elif name == "status_img":
                sImg = child
            elif name == "status_frame":
                for sName, sChild in child.children.items():
                    if sName == "status_code":
                        sCode = sChild

        flower_img =Globals.createImage("./Images/"+Globals.PLANT["image_path"], (150,150))
        fImg.config(image=flower_img)
        fImg.image = flower_img
        fName.config(text=Globals.PLANT["name"])
        code, img = self.checkPlantStatus(index)
        sCode.config(text=code)
        sImg.config(image=img)
        sImg.image = img
        self.updateScrollbar()

    def generateNewPlantBox(self):

        index = Globals.numPlants()

        self.NewPlantBox = tk.Frame(
            self.inner_frame, width=275, height=175, bg=Globals.ACCENT1)
        self.NewPlantBox.grid(row=index % 2, column=index//2, pady=20, padx=40)
        self.NewPlantBox.grid_propagate(False)

        image = Globals.createImageFrame(
            "./Assets/Plus.png", (75, 75), self.NewPlantBox, Globals.ACCENT1)
        image.grid(row=0, column=0, sticky="nsew")
        image.bind("<Button-1>", lambda event: self.newPlant(event))

        tk.Label(
            self.NewPlantBox,
            text="New Plant",
            bg=Globals.ACCENT1,
            fg=Globals.TEXT,
            font=("TkMenuFont", 15),
        ).grid(row=1, column=0, sticky="nsew", padx=10, pady=10, columnspan=3, rowspan=3)

        self.NewPlantBox.rowconfigure(0, weight=1)
        self.NewPlantBox.rowconfigure(1, weight=1)
        self.NewPlantBox.columnconfigure(0, weight=1)
        self.NewPlantBox.bind("<Button-1>", lambda event: self.newPlant(event))

    def generatePlantBoxes(self):
        if Globals.PLANT_DATA is None:
            Globals.readPlantData()
        for index, plant in enumerate(Globals.PLANT_DATA):
            path = f"./Images/{plant['image_path']}"
            if path == "./Images/":
                path = "./Assets/Question.png"
            self.generatePlantBox(path, plant['name'], index)

    def updatePlant(self, event, plant_index):
        print(self.parent)
        self.parent.showEdit(plant_index)

    def newPlant(self, event):
        self.parent.newPlant()

    def __init__(self, parent):
        self.parent = parent

        def showProfile():
            self.parent.showView("Profile")

        def updateWeather():
            # API FOR https://www.weatherapi.com/my/
            city = combo_box.get()
            if city == "Select a City":
                messagebox.showinfo("Notice", "Cannot update weather without picking city")
                return
            
            if self.API_KEY == "ENTER API KEY HERE":
                messagebox.showinfo("Notice", "Cannot retreive weather without API key")
                return
            
            query = f"http://api.weatherapi.com/v1/current.json?key={self.API_KEY}&q={city}&aqi=no"
            response = requests.post(query)

            data = json.loads(response.text)

            metric = metric_box.get()

            temptype = "temp_f"
            temp_denom = "° F"
            speed = "wind_mph"
            speed_denom = "MPH"
            if metric == "C/KPH":
                temptype = "temp_c"
                temp_denom = "° C"
                speed = "wind_kph"
                speed_denom = "KPH"

            temperature = data["current"][temptype]
            wind_speed = data["current"][speed]
            temp.config(text=str(temperature)+temp_denom)
            wind.config(text=str(wind_speed)+speed_denom)

        # create frame widget
        Container = self.parent.createContainer("Main")

        Header = tk.Frame(Container, width=Globals.WIDTH,
                          height=100, bg=Globals.ACCENT1)

        tk.Label(
            Header,
            text=Globals.TITLE,
            bg=Globals.ACCENT1,
            fg=Globals.TEXT,
            font=("TkMenuFont", 25),
        ).grid(row=0, column=0, sticky="w", padx=20, pady=10)

        tk.Button(
            Header,
            text="Profile",
            bg=Globals.ACCENT2,
            fg=Globals.TEXT,
            font=("TkMenuFont", 20),
            width=15,
            command=showProfile
        ).grid(row=0, column=1, sticky="e", padx=30, pady=15)

        # Configure the first column to expand and fill any extra space
        Header.columnconfigure(0, weight=1)
        Header.pack(fill="x")

        # region Information Bar
        InfoBar = tk.Frame(Container, width=Globals.WIDTH,
                           height=100, bg=Globals.BG_COLOR)
        InfoBar.pack(fill="x")

        tk.Button(
            InfoBar,
            text="Water Chart",
            bg=Globals.ACCENT2,
            fg=Globals.TEXT,
            font=("TkMenuFont", 15),
            width=15,
            command=lambda: self.showWateringChart(self.parent)
        ).grid(row=0, column=0, sticky="nw", padx=30, pady=15)

        WeatherInfo = tk.Frame(
            InfoBar, width=Globals.WIDTH/2, height=100, bg=Globals.BG_COLOR)
        WeatherInfo.grid(row=0, column=1, sticky="ne", padx=30, pady=15)

        tk.Label(
            WeatherInfo,
            text="Metric",
            bg=Globals.BG_COLOR,
            fg=Globals.TEXT,
            font=("TkMenuFont", 10),
        ).grid(row=0, column=0, sticky="w", pady=10)

        Metrics = ["F/MPH", "C/KPH"]
        metric_box = ttk.Combobox(
            WeatherInfo, values=Metrics, height=2, width=15, state="readonly")
        metric_box.set("F/MPH")
        metric_box.grid(row=0, column=1, pady=10, padx=10, sticky="nw")

        tk.Label(
            WeatherInfo,
            text="City",
            bg=Globals.BG_COLOR,
            fg=Globals.TEXT,
            font=("TkMenuFont", 10),
        ).grid(row=0, column=2, sticky="w", pady=10)

        Cities = ['Zagreb', 'Split', 'Rijeka', 'Osijek', 'Zadar', 'Pula', 'Sesvete', 'Slavonski Brod', 'Karlovac', 'Varazdin',
                  'Sibenik', 'Sisak', 'Vukovar', 'Dubrovnik', 'Cakovec', 'Bjelovar', 'Samobor', 'Vinkovci', 'Virovitica', 'Pozega']
        combo_box = ttk.Combobox(
            WeatherInfo, values=Cities, height=2, width=15, state="readonly")
        combo_box.set("Select a City")
        combo_box.grid(row=0, column=3, pady=10, padx=10, sticky="nw")

        tk.Label(
            WeatherInfo,
            text="Weather",
            bg=Globals.BG_COLOR,
            fg=Globals.TEXT,
            font=("TkMenuFont", 10),
        ).grid(row=1, column=0, sticky="w", pady=10)

        temp = tk.Label(
            WeatherInfo,
            text="0° F",
            bg=Globals.BG_COLOR,
            fg=Globals.TEXT,
            font=("TkMenuFont", 10),
        )
        temp.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        tk.Label(
            WeatherInfo,
            text="Wind Speed",
            bg=Globals.BG_COLOR,
            fg=Globals.TEXT,
            font=("TkMenuFont", 10),
        ).grid(row=1, column=2, sticky="w", pady=10)

        wind = tk.Label(
            WeatherInfo,
            text="0 MPH",
            bg=Globals.BG_COLOR,
            fg=Globals.TEXT,
            font=("TkMenuFont", 10),
        )
        wind.grid(row=1, column=3, sticky="w", padx=10, pady=10)

        tk.Button(
            WeatherInfo,
            text="Update Weather",
            bg=Globals.ACCENT2,
            fg=Globals.TEXT,
            font=("TkMenuFont", 10),
            width=15,
            command=updateWeather
        ).grid(row=2, column=1, columnspan=2, sticky="n", pady=20)

        # endregion

        # region self.plant View

        PlantView = tk.Frame(Container, width=Globals.WIDTH, height=300,)
        PlantView.pack(fill="x", padx=20)

        self.scrollbar = tk.Scrollbar(PlantView, orient="horizontal")
        self.scrollbar.pack(fill="x", side="bottom")

        # create the canvas widget
        self.canvas = tk.Canvas(PlantView, width=380, height=475, xscrollcommand=self.scrollbar.set,
                                highlightbackground=Globals.BG_COLOR, bg=Globals.BG_COLOR)
        self.canvas.pack(side="left", fill="both", expand=True)

        # create the frame inside the canvas widget
        self.inner_frame = tk.Frame(self.canvas, bg=Globals.BG_COLOR)
        self.inner_frame.pack(fill="both", expand=True)

        self.generatePlantBoxes()

        self.generateNewPlantBox()

        self.scrollbar.config(command=self.canvas.xview)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))

        # endregion

        PlantView.after(0, self.updateScrollbar)
        InfoBar.columnconfigure(0, weight=1)
