import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo

root = tk.Tk()

root.title("Interface - ENG1419 Projeto Final")

window_width = 800
window_height = 600

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

center_text = ttk.Label(
    root,
    text="Painel de Gestão de Moradores",
    font=("Helvetica",14)
)
center_text.pack(ipadx=10, ipady=100)

def visualize_handler():
    showinfo(title="Info", message="Visualizar clicado")

def add_handler():
    showinfo(title="Info", message="Adicionar clicado")

def edit_handler():
    showinfo(title="Info", message="Editar clicado")

# Buttons
visualize = ttk.Button(
    root,
    text="Visualizar Moradores",
    command=visualize_handler
)

visualize.place(x=315,y=250,width=160,height=60)

add = ttk.Button(
    root,
    text="Adicionar Morador",
    command=add_handler
)

add.place(x=315,y=330,width=160,height=60)

edit = ttk.Button(
    root,
    text="Editar Morador",
    command=edit_handler
)

edit.place(x=315,y=410,width=160,height=60)

# remove blur in windows. try catch for portability between platforms
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()