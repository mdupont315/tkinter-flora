from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
import tkinter as tk
import json
import random 
import string
import os

# region Predefined Globals
TITLE = "PyFlora Posuda"
WIDTH = 800
HEIGHT = 700
BG_COLOR = "#3d6466"
ACCENT1 = "#073335"
ACCENT2 = "#177276"
TEXT = "#FFFFFF"
CONFIG_PATH = "./configs/config.json"
USERS_PATH = "./configs/users.json"
PLANT_DIR = "./plants/"
CONFIG = None
# endregion


# region User Dependant Globals
USERNAME = None
JSON_PATH = None
USER = None
PLANT_DATA = None
PLANT = None
Parent = None
# endregion



def readJson(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    return data

def writeJson(data, path, mode="w"):
    with open(path, mode) as f:
        json.dump(data, f)

def isAdmin():
    return USER["role"] == "admin"

def updateJson():
    global JSON_PATH
    JSON_PATH = PLANT_DIR+USER["plants"]
    
def refreshConfig():
    global CONFIG
    CONFIG = readJson(CONFIG_PATH)
    
def loadTheme():
    global CONFIG, BG_COLOR, ACCENT1, ACCENT2, TEXT    
    theme = CONFIG["THEME"]
    theme = CONFIG["THEMES"][theme]
    BG_COLOR = theme["BG_COLOR"]
    ACCENT1 = theme["ACCENT1"]
    ACCENT2 = theme["ACCENT2"]
    TEXT = theme["TEXT"]
    
def readUser(username):
    global USER
    users = readJson(USERS_PATH)
    USER = users[username]
    USERNAME = username
    updateJson()
    
def updateUser():
    users = readJson(USERS_PATH)
    users[USERNAME] = USER
    writeJson(users, USERS_PATH)

def isUser(username):
    users = readJson(USERS_PATH)
    return username in users
    
def verifyPass(password):
    return USER["password"] == password

def createUser(username, password, role = "user"):
    user_data = readJson(USERS_PATH)
    code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=5))
    if role == "admin" and not isAdmin():
        role = "user"
    user_data[username] = {
        "password": password,
        "role": role,
        "plants": f"{code}.json",
    }
    writeJson([], f"{PLANT_DIR}{code}.json", "x")
    writeJson(user_data, USERS_PATH)
    readUser(username)
    
def getPlant(index):
    global PLANT, PLANT_DATA
    if not PLANT_DATA:
        readPlantData()
    PLANT = PLANT_DATA[index]

def readPlantData():
    global PLANT_DATA
    PLANT_DATA = readJson(JSON_PATH)

def updatePlant(index):
    if index == len(PLANT_DATA):
        PLANT_DATA.append(PLANT)
    else:
        PLANT_DATA[index] = PLANT
    updatePlants()

def updatePlants():
    writeJson(PLANT_DATA, JSON_PATH)

def numPlants():
    return len(PLANT_DATA)

def removePlant():
    global PLANT_DATA, PLANT
    PLANT_DATA.remove(PLANT)
    updatePlants

def updatePass(current_pass, new_pass):
    print(current_pass)
    print(new_pass)
    if verifyPass(current_pass):
        USER["password"] = new_pass
        updateUser()
        messagebox.showinfo("Information","Password updated")
    else:
        messagebox.showinfo("Information","Incorrect current password")

def deleteUser(username):
    if not isAdmin():
        messagebox.showinfo("Information","You are not authorized to delete users")
        return False
    users = readJson(USERS_PATH)
    if response := messagebox.askyesno(
        "Information", "Do you want to delete the users flower file?"
    ):
        os.remove(PLANT_DIR+users[username]["plants"])
    del users[username]
    writeJson(users, USERS_PATH)
    return True
    
def getPlantFiles():
    return  [f for f in os.listdir(PLANT_DIR) if os.path.isfile(os.path.join(PLANT_DIR, f))]
    

refreshConfig()
loadTheme()

# Needs to be after loadTheme to load correct BG_COLOR
def createImage(path, size):
    image_open = Image.open(path)
    image_resized = image_open.resize(size, Image.ANTIALIAS)
    return  ImageTk.PhotoImage(image_resized)

def createImageFrame(path, size, parent, bg = BG_COLOR, name="flower_img"):
    image = createImage(path,size)
    image_widget = tk.Label(parent, image=image, background=bg, name=name)
    image_widget.image = image
    return image_widget


