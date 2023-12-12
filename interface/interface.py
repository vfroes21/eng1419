import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo

from serial import Serial

from pymongo import MongoClient
import database

# global resident list (need to be seen by add and edit resident classes)
resident_list = []

# serial config
'''serial = Serial("COM5", baudrate=9600)
t = "ler\n"
'''

# connecting to db
connection_str = database.get_string()
client = MongoClient(connection_str)

db = client["moradores"]
collection = db["casa1"]

cursor = collection.find()

#doc = {"First Name":"Jan", "Last Name": "Krueger", "Tag ID": "0002", "Password":"202265"}
#collection.insert_one(doc)

# retrieving all info but id from the db entry
for document in cursor:
    new_dict = {}
    for key, value in document.items():
        if key != "_id":
            new_dict[key] = value
           
    resident_list.append(new_dict)
   

# this reads the tag id and prints it
'''while True:
    serial.write(t.encode("UTF-8"))
    txt = serial.readline().decode().strip()
    if txt.startswith("In hex:"):
        print(txt[8:].strip())'''

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
            manage_residents = ManageResidentWin(type="add",parent_class=self)
            

        # add resident button
        self.add_bt = ttk.Button(self,text="Adicionar Morador", comman=add_handler)
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
            if selected_item:
                self.tree.delete(selected_item)

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
            self.tree.insert('', tk.END, values=resident)

        

class ManageResidentWin(tk.Toplevel):
    def __init__(self,type,parent_class,resident=None):
        super().__init__()

        self.parent_class = parent_class

        window_width = 500
        window_height = 500
        
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
        
        # labels
        f_name_label = ttk.Label(self, text="Nome")
        f_name_label.place(x=10, y=10)
        l_name_label = ttk.Label(self,text="Sobrenome")
        l_name_label.place(x=10,y=100)
        tag_label = ttk.Label(self,text="Tag")
        tag_label.place(x=10,y=190)

        password_label = ttk.Label(self,text="Senha")
        password_label.place(x=10,y=280)

        # entries
        f_name_entry = ttk.Entry(self, textvariable=self.f_name)
        f_name_entry.place(x=10, y=40, width=400)
        f_name_entry.focus()
        l_name_entry = ttk.Entry(self, textvariable=self.l_name)
        l_name_entry.place(x=10,y=130,width=400)
        tag_entry = ttk.Entry(self, textvariable=self.tag)
        tag_entry.place(x=10,y=220,width=400)
        password_entry = ttk.Entry(self,textvariable=self.password)
        password_entry.place(x=10,y=310,width=400)

        if type == "add":
            self.add_window()
        
        elif type == "edit":
            if resident:
                self.resident = resident
                self.edit_window(self.resident)
            else:
                showinfo(title="Erro", message="SOMETHING WRONG, INVALID RESIDENT DATA")


    def add_handler(self):
        resident_list.append((f'{self.f_name.get()}',f'{self.l_name.get()}',f'{self.tag.get()}',f'{self.password.get()}'))
        self.destroy()  # Close the Toplevel window
        self.parent_class.update_tree()

    def edit_handler(self):
        self.parent_class.tree.set(self.resident[0], 'f_name', value=self.f_name.get())
        self.parent_class.tree.set(self.resident[0], 'l_name', value=self.l_name.get())
        self.parent_class.tree.set(self.resident[0], 'tag_id', value=self.tag.get())
        self.parent_class.tree.set(self.resident[0], 'password', value=self.password.get())

        self.destroy()
        self.parent_class.tree.update_idletasks()     # refresh treeview

    def add_window(self):
        self.title("Adicionar Moradores")
        submit_bt = ttk.Button(self, text="Adicionar", command=self.add_handler)
        submit_bt.place(x=200, y=430, width=140, height=40)
    
    def edit_window(self,resident):
        self.f_name.set(resident[1][0])
        self.l_name.set(resident[1][1])
        self.tag.set(resident[1][2])
        self.password.set(resident[1][3])

        self.title("Editar Moradores")

        submit_bt = ttk.Button(self, text="Editar", command=self.edit_handler)
        submit_bt.place(x=200, y=430, width=140, height=40)
    


# remove blur in windows. try catch for portability between platforms
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    app = MainWin()
    app.mainloop()