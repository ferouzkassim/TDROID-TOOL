import tkinter as tk
from tkinter import *
import tkinter as ttk
root = tk.Tk()
#root the frame poatiioning and such
root.title('Tdroid_Tool')
root.configure(bg='#D8D5C8')
icon = PhotoImage(file='icon.png')
root.iconphoto(True, icon)
root.resizable(False,False)
root_wid = 900
root_hi = 600
screen_wdth = root.winfo_screenwidth()
scree_height = root.winfo_screenwidth()
cent_screen = int(screen_wdth/1-root_wid)
cent_screenh = int(scree_height/2-root_hi)
root.geometry(f'{root_wid}x{root_hi}+{cent_screen}+{cent_screenh}')
#end of root sizings
#labells
lebo = Label(root,text='model',padx=30,pady=10).place(x=400,y=0)
#frames
frem = Frame(root, height=600, width=100, )
frem.columnconfigure(0,weight=1)
frem.grid(pady=25,padx=1)
frem2= Frame(root)
frem2.grid(column=1,row=1)

#button
def butt(txt, nem ):
    nem = tk.Button(frem, text=txt, )
    nem.configure(bg='black', foreground='white', borderwidth=2,width=14)
    nem.grid(pady=10,padx=10,sticky=W)
    return nem

#detect=tk.Button(frem,text='Detect',)
#model list
mdellist=['sm-a125f','sm-a127f','sm-a135f','sm-a022f','sm-a225f']
for umdel in mdellist:
    umdel.upper()

#drop list
model=tk.Listbox(root,height=2,listvariable=tk.StringVar(value=(for umdel in mdellist:
umdel.upper())))
model.grid(row=0,column=10,sticky=NW,pady=25,padx=10)



#detect.place(x=10,y=50)
#detect.configure(bg='black',foreground='white',borderwidth=2,font='ubuntu')
BackUp=butt(txt='BackUp Nv',nem='BackUp')
BackUp.grid(row=1,column=0)
Detect=butt(txt='Detect',nem='Detect',)
Detect.grid(row=0,column=0,)
Restore=butt(txt='Restore Nv',nem='Restore')
Restore.grid(row=2,column=0)
fix=butt(txt='fix baseband',nem='fix')
fix.configure(font='arial 10')
fix.grid(row=3,column=0)
mount=butt(txt='mount baseband',nem='mount')
mount.grid(row=4,column=0)
mount.config(font='ubuntu 9')
mount.config(padx=10)
BackUpEfs=butt(txt='Backup Efs',nem='BackupEfs')
BackUpEfs.grid(row=5,column=0)


#textare

root.mainloop()
