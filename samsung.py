import tkinter as tk
from tkinter import W,ttk
from tkinter import filedialog as filer
import os.path
class butonField:
    def __init__(self,name,root,xcol,ycol,altroot):
        self.name = name
        self.root = root
        self.altroot = altroot
        self.xcol = xcol
        self.ycol = ycol
    def  butt(self,name,root,xcol,ycol):
          button = tk.Button(root,text=name)
          button.grid(column=xcol,row=ycol)

    def buttn(self,name,root,altroot,row):
        selected_file = None
        firmwarefile = None
        nem = tk.Button(root, text=name, )
        nem.configure(fg='white', background='black', borderwidth=1, width=14)
        nem.grid(pady=4, padx=4, sticky=W)
        x=0
        entry = tk.Entry(altroot, width=110)
        entry.grid(row =row,column=0,pady=10)




        def assign_file(file_var):
            nonlocal selected_file
            selected_file = filer.askopenfile(title='Select firmware', filetypes=(
                ('bin file', '*.bin'),
                ('tar file', '*.tar'),
                ('img file', '*.img'),
                ('pit file', '*.pit'),
                ('.tar file', '*tar'),
                ('.md5 file', '*.md5')))
        nem.config(command=lambda:[ assign_file(selected_file)])
        firmwarefile = tk.StringVar(value=selected_file)
        entry.config(relief='ridge', bd=2, textvariable=firmwarefile)
        return selected_file

    def fileloader(self):
        pass


