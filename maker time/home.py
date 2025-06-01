import tkinter as tk
from tkinter import*
import requests as rq

root = Tk()
root.title("superheroapi")
root.geometry("500x700")
root.configure(bg='#FF0000')


root.configure(fg='#000000')


root.title(root, text="SUPERHERO API")
lbl = Label(root, text="SUPERHERO")
lbl.grid(colum=0, row=0)



root.mainloop()

