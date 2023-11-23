import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showinfo

# global resident list (need to be seen by add and edit resident classes)
resident_list = []
resident_list.append(('Victor','Froes','0001','209865'))

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
            add_window = tk.Toplevel(self)
            add_window.title("Adicionar Morador")
    
            window_width = 500
            window_height = 500
    
            # Center the Toplevel window
            center_x = int((self.winfo_screenwidth() / 2 - window_width / 2) - 75)
            center_y = int((self.winfo_screenheight() / 2 - window_height / 2) + 50)
            add_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
            # Data holders
            f_name = tk.StringVar()
            l_name = tk.StringVar()
            tag = tk.StringVar()
            password = tk.StringVar()

            # labels
            f_name_label = ttk.Label(add_window, text="Nome")
            f_name_label.place(x=10, y=10)

            l_name_label = ttk.Label(add_window,text="Sobrenome")
            l_name_label.place(x=10,y=100)

            tag_label = ttk.Label(add_window,text="Tag")
            tag_label.place(x=10,y=190)
    
            password_label = ttk.Label(add_window,text="Senha")
            password_label.place(x=10,y=280)


            # entries
            f_name_entry = ttk.Entry(add_window, textvariable=f_name)
            f_name_entry.place(x=10, y=40, width=400)
            f_name_entry.focus()

            l_name_entry = ttk.Entry(add_window, textvariable=l_name)
            l_name_entry.place(x=10,y=130,width=400)

            tag_entry = ttk.Entry(add_window, textvariable=tag)
            tag_entry.place(x=10,y=220,width=400)

            password_entry = ttk.Entry(add_window,textvariable=password)
            password_entry.place(x=10,y=310,width=400)

    
            def add_handler_in_add_window():
                resident_list.append((f'{f_name.get()}',f'{l_name.get()}',f'{tag.get()}',f'{password.get()}'))
                add_window.destroy()  # Close the Toplevel window
                update_tree()

            # Submit button for the Toplevel window
            submit_bt = ttk.Button(add_window, text="Adicionar", command=add_handler_in_add_window)
            submit_bt.place(x=200, y=430, width=140, height=40)


        '''def edit_handler():
            edit = EditResidentWin()
            edit.mainloop()
        '''
        # add resident button
        self.add_bt = ttk.Button(self,text="Adicionar Morador",command=add_handler)
        self.add_bt.place(x=670,y=90,width=140,height=40)

        '''self.edit_bt = ttk.Button(self,text="Editar Morador",command=edit_handler)
        self.edit_bt.place(x=700,y=90,width=120,height=40)'''
        
        # define list columns
        columns = ('f_name','l_name','tag_id','password')

        tree = ttk.Treeview(self, columns=columns, show='headings')

        # define column headings
        tree.heading('f_name', text='Nome')
        tree.heading('l_name', text='Sobrenome')
        tree.heading('tag_id', text='ID Tag')
        tree.heading('password',text="Senha")

        # add data to the treeview
        for resident in resident_list:
            tree.insert('', tk.END, values=resident)

        def update_tree():
             # Clear the existing items in the Treeview widget
            for item in tree.get_children():
                tree.delete(item)

            # Add data to the Treeview widget
            for resident in resident_list:
                tree.insert('', tk.END, values=resident)

         # place list
        tree.place(height=449,x=0, y=150)

        # add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.place(height=455,x=802,y=147)

        
        
class AddResidentWin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Adicionar Morador")

        window_width = 600
        window_height = 600
        
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

        f_name_label = ttk.Label(self,text="Nome")
        f_name_label.place(x=10,y=10)

        f_name_entry = ttk.Entry(self, textvariable=self.f_name)
        f_name_entry.place(x=10,y=40,width=400)
        f_name_entry.focus()

        def add_handler():
            #resident_list.append
            print(self.f_name.get())

        # submit button
        self.submit_bt = ttk.Button(self,text="Adicionar",command=add_handler)
        self.submit_bt.place(x=50,y=500,width=140,height=40)

        


class EditResidentWin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Editar Moradores")

        window_width = 825
        window_height = 600
        
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # find the center point (+ offset)
        center_x = int((screen_width/2 - window_width / 2)-75)  
        center_y = int((screen_height/2 - window_height / 2)+50)
        
        # set the position of the window to the center of the screen   
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        # define list columns
        columns = ('f_name','l_name','tag_id','password')

        tree = ttk.Treeview(self, columns=columns, show='headings')

        # define headings
        tree.heading('f_name', text='Nome')
        tree.heading('l_name', text='Sobrenome')
        tree.heading('tag_id', text='ID Tag')
        tree.heading('password',text="Senha")

        # place list
        tree.grid(row=0, column=0, sticky='nsew')

        # add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')



# remove blur in windows. try catch for portability between platforms
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
finally:
    app = MainWin()
    app.mainloop()