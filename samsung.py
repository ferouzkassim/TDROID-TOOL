import tkinter as tk
from tkinter import W,ttk
from tkinter import filedialog as filer
import os.path
class butonField:
    def __init__(self,name,root,xcol,ycol):
        self.name = name
        self.root = root
        self.xcol = xcol
        self.ycol = ycol
    def  butt(self,name,root,xcol,ycol):
        button = tk.Button(root,text=name)
        button.grid(column=xcol,row=ycol)

    def buttn(self,name,root):
        nem = tk.Button(root, text=name, )
        nem.configure(fg='white', background='black', borderwidth=1, width=14)
        nem.grid(pady=4, padx=4, sticky=W)
        nem.config(command=lambda: filer.askopenfilenames(defaultextension=(('bin file','*.bin'),
                                                                     ('tar file','*.tar'),
                                                                     ('img file','*.img'),('pit file','*.pit')),
                                                                       ))

    def fileloader(self):
        pass


