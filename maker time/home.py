import tkinter as tk
from tkinter import *
import requests as rq
from tkinter import messagebox

api_key ='64fc6a9674dbf61d7a83e855b4f93084'
url = 'https://superheroapi.com/api/'
last_query = ""

def search():

    name = heroEntry.get()
    api = f"{url}{api_key}/search/{name}"
    try:
        response = rq.get(api)
        data = response.json()

        print(data)

    except Exception as e:
       print(e)

def search_image():
    global last_query, img
    query = Entry.get().strip()

    if not query:
        messagebox.showwarning("Увага б поле введення")
        return

root = tk.Tk()
root.title("superheroapi")
root.geometry("500x700")
root.configure(bg='#000080')


lbl = Label(root, text="SUPERHERO")
lbl.pack(fill=X, ipady=20)
lbl.configure(fg='#b8860b', font='Minecraft-Regular', bg='#000080')



hero = Button(root, text="HERO", command=search)
hero.pack(fill=X)
hero.configure(font='Minecraft-Regular', bg='#ff0000')


heroEntry = Entry(root)
heroEntry.pack(fill=X)
heroEntry.configure(bg='#808080')




root.mainloop()

