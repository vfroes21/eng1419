import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo

from serial import Serial

from pymongo import MongoClient
import database

from threading import Thread

import cv2
from PIL import Image,ImageTk
import os


# **************** global variables ************

# global resident list (need to be seen by add and edit resident classes)
global resident_list
resident_list = []

# get_rfid class must be seen by the thread
global get_rfid

# manage_residents class must be seen by the thread
global manage_residents

# **********************************************

# connecting to db
connection_str = database.get_string()
client = MongoClient(connection_str)

db = client["moradores"]
collection = db["casa1"]


# retrieving all info but id from db entries
def insert_db_entry_into_list():
    cursor = collection.find()
    global resident_list
    resident_list = []
    for document in cursor:
        new_dict = {}
        for key, value in document.items():
            if key != "_id":
                new_dict[key] = value

        resident_list.append(new_dict)

insert_db_entry_into_list()

# serial config 
serial = Serial("COM5", baudrate=9600)

def thread_serial():
            # this reads the tag id and prints it
            while True:
                txt = serial.readline().decode().strip()
                if txt.startswith("In hex:"):
                    print(txt[8:].strip())
                   
                    global manage_residents
                    if manage_residents:
                        manage_residents.tag.set(txt[8:].strip())

                    global get_rfid
                    if get_rfid:
                        get_rfid.destroy()

# star thread that keep reading rfid from serial
thread = Thread(target=thread_serial)
thread.daemon = True
thread.start()

# main class
class MainWin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Interface - ENG1419 Projeto Final")

        window_width = 825
        window_height = 600
        
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)  
        center_y = int(screen_height/2 - window_height / 2)
        
        # set the position of the window to the center of the screen   
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.label = ttk.Label(self,text="Painel de Gestão de Moradores",font=("Helvetica",14))
        self.label.pack(ipadx=10, ipady=30)

        def add_handler():
            global manage_residents
            manage_residents = ManageResidentWin(type="add",parent_class=self)
            
        # add resident button
        self.add_bt = ttk.Button(self,text="Adicionar Morador", command=add_handler)
        self.add_bt.place(x=670,y=90,width=140,height=40)
        
        # define list columns
        columns = ('f_name','l_name','tag_id','password')

        self.tree = ttk.Treeview(self, columns=columns, show='headings')

        # define column headings
        self.tree.heading('f_name', text='Nome')
        self.tree.heading('l_name', text='Sobrenome')
        self.tree.heading('tag_id', text='ID Tag')
        self.tree.heading('password',text="Senha")

        # add data to the treeview
        for resident in resident_list:
            t = tuple(resident.values())
            self.tree.insert('', tk.END, values=t)

        def show_context_menu(event):
            item = self.tree.identify_row(event.y)  # get item under cursor
            if item:
                # if item not already selected, select it
                if item not in self.tree.selection():
                 self.tree.selection_set(item)
                menu.post(event.x_root, event.y_root)  # show menu at cursor position

        def delete_item():
            selected_item = self.tree.selection()[0]
            values = self.tree.item(selected_item, 'values')   # get data from user being clicked
          
            if values:
                # find resident on db 
                busca = {"First Name":values[0]}
       
                collection.delete_one(busca)
            
                insert_db_entry_into_list()

                self.update_tree()
                self.tree.update_idletasks()     # refresh treeview
            else:
                showinfo(title="Erro",message="Tried to delete resident but no resident was received")
           

        def edit_item():
            selected_item = self.tree.selection()[0]
            values = self.tree.item(selected_item, 'values')   # get data from user being clicked
              
            if values:
                manage_win = ManageResidentWin(type="edit",parent_class=self,resident=(selected_item,values))

        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="Editar", command=edit_item)
        menu.add_command(label="Deletar", command=delete_item)

        # right mouse click event
        self.tree.bind("<Button-3>", show_context_menu)

        # Bind the TreeviewSelect event to update the selection
        self.tree.bind("<<TreeviewSelect>>", lambda event: self.tree.focus())

         # place list
        self.tree.place(height=449,x=0, y=150)

        # add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.place(height=455,x=802,y=147)
    
    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for resident in resident_list:
            t = tuple(resident.values())
            self.tree.insert('', tk.END, values=t)

        

class ManageResidentWin(tk.Toplevel):
    def __init__(self,type,parent_class,resident=None):
        super().__init__()

        self.parent_class = parent_class
        self.resident = resident

        window_width = 500
        window_height = 650
      
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # find the center point (+ offset)
        center_x = int((screen_width/2 - window_width / 2)-75)  
        center_y = int((screen_height/2 - window_height / 2)+50)
        
        # set the position of the window to the center of the screen   
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

         # data holders
        self.f_name = tk.StringVar()
        self.l_name = tk.StringVar()
        self.tag = tk.StringVar()
        self.password = tk.StringVar()
        self.photo = tk.StringVar()

        # labels
        f_name_label = ttk.Label(self, text="Nome")
        f_name_label.place(x=10, y=10)
        l_name_label = ttk.Label(self,text="Sobrenome")
        l_name_label.place(x=10,y=100)
        tag_label = ttk.Label(self,text="Tag")
        tag_label.place(x=10,y=190)
        password_label = ttk.Label(self,text="Senha")
        password_label.place(x=10,y=480)
        photo_label = ttk.Label(self, text="Foto")
        photo_label.place(x=10, y=330)

        # entries
        f_name_entry = ttk.Entry(self, textvariable=self.f_name)
        f_name_entry.place(x=10, y=40, width=400)
        f_name_entry.focus()
        l_name_entry = ttk.Entry(self, textvariable=self.l_name)
        l_name_entry.place(x=10,y=130,width=400)
        tag_entry = ttk.Entry(self, textvariable=self.tag, state='readonly')
        tag_entry.place(x=10,y=220,width=400)
        password_entry = ttk.Entry(self,textvariable=self.password)
        password_entry.place(x=10,y=510,width=400)
        photo_entry = ttk.Entry(self, textvariable=self.photo, state='readonly')
        photo_entry.place(x=10,y=360,width=400)

        def rfid_handler():
            global get_rfid 
            get_rfid = GetRFIDwin()

        def photo_handler():
            get_photo = GetPhotoWin(self)

        self.get_rfid_bt = ttk.Button(self,text="Ler RFID", command=rfid_handler)
        self.get_rfid_bt.place(x=10,y=260,width=110,height=40)

        self.get_photo_bt = ttk.Button(self,text="Capturar",command=photo_handler)
        self.get_photo_bt.place(x=10, y=400,width=110,height=40)

        if type == "add":
            self.add_window()
        
        elif type == "edit":
            if resident:
                self.edit_window(self.resident)
            else:
                showinfo(title="Erro", message="SOMETHING WRONG, INVALID RESIDENT DATA")


    def add_handler(self):     
        # creating data and sending to db
        if self.photo.get() == "" and self.tag.get() == "":
            current_grab = self.grab_current()
           
            showinfo(title="Aviso",message="Para cadastrar um morador é necessário cadastrar um RFID ou foto")
            return

        d = {}
        d["First Name"] = f'{self.f_name.get()}'
        d["Last Name"] = f'{self.l_name.get()}'
        d["Tag ID"] = f'{self.tag.get()}'
        d["Picture File"] = f'{self.photo.get()}'
        d["Password"] = f'{self.password.get()}'

        collection.insert_one(d)

        insert_db_entry_into_list()
    
        self.destroy()  
        self.parent_class.update_tree()

    def edit_handler(self):

        # updating given entry
        if self.resident:
            # find resident on db (before edited)
            busca = {"First Name":self.resident[1][0]}
            # udpate all fields
            update_operation = {
                "$set": {
                    "First Name": self.f_name.get(),
                    "Last Name": self.l_name.get(),
                    "Tag ID": self.tag.get(),
                    "Picture File": self.photo.get(),
                    "Password": self.password.get()
                }
            }
            collection.update_one(busca, update_operation)

            insert_db_entry_into_list()

            self.destroy()
            self.parent_class.update_tree()
            self.parent_class.tree.update_idletasks()     # refresh treeview
        else:
            showinfo(title="Erro",message="Tried to update resident but no resident was received")

    def add_window(self):
        self.title("Adicionar Moradores")
        submit_bt = ttk.Button(self, text="Adicionar", command=self.add_handler)
        submit_bt.place(x=200, y=580, width=140, height=40)
    
    def edit_window(self,resident):
        # pre fill input fields
        self.f_name.set(resident[1][0])
        self.l_name.set(resident[1][1])
        self.tag.set(resident[1][2])
        self.photo.set(resident[1][3])
        self.password.set(resident[1][4])

        self.title("Editar Moradores")

        submit_bt = ttk.Button(self, text="Editar", command=self.edit_handler)
        submit_bt.place(x=200, y=430, width=140, height=40)
    

class GetRFIDwin(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title("RFID")

        window_width = 300
        window_height = 120
        
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # find the center point (+ offset)
        center_x = int((screen_width/2 - window_width / 2)-15)  
        center_y = int((screen_height/2 - window_height / 2)+20)
        
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        label = ttk.Label(self, text="Enviando comando para ler RFID...")
        label.place(x=20, y=15)

        prog_bar = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=250)
        prog_bar.place(x=20,y=50)
        prog_bar.start()

        # sending read cmd
        t = "ler\n"
        serial.write(t.encode("UTF-8"))

        label.config(text="Aguardando RFID...")


class GetPhotoWin(tk.Toplevel):
    def __init__(self,parent_class):
        super().__init__()

        self.title("Webcam")

        self.video_capture = cv2.VideoCapture(0) 
        self.current_image = None

        self.canvas = tk.Canvas(self, width=640,height=480)
        self.canvas.pack()

        self.parent_class = parent_class
        print(self.parent_class.f_name.get())

        def save_img():
            if self.current_image is not None:
                current_directory = os.path.dirname(os.path.abspath(__file__))

                if self.parent_class.f_name.get() != "" or self.parent_class.l_name.get() != "":
                    aux = 'faces/' + self.parent_class.f_name.get() + '_' + self.parent_class.l_name.get() + '.jpg'
                    s = aux.replace(' ','_')
                    path = os.path.join(s)

                    self.parent_class.photo.set(s[6:])
                else:
                    path = os.path.join(current_directory, 'faces/newuser.jpg')

                    self.parent_class.photo.set("newuser.jpg")
                

                self.current_image.save(path)

                self.destroy()


        self.download_bt = ttk.Button(self, text="Capturar", command=save_img)
        self.download_bt.pack()

        self.update_webcam()

    def update_webcam(self):
        ret,frame = self.video_capture.read()

        if ret:
            self.current_image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))       

            self.photo = ImageTk.PhotoImage(image=self.current_image)
            self.canvas.create_image(0,0,image=self.photo,anchor=tk.NW)
            self.after(15,self.update_webcam) 

   


# remove blur in windows. try catch for portability between platforms
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    app = MainWin()
    app.mainloop()