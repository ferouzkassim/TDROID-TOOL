import tkinter.ttk
import os

import fastbootpy

import detect
import fastboot
from usbcom import *
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from detect import *
from tkinter import filedialog as filer
from fastbootpy import *
root = tk.Tk()
# root the frame poatiioning and such
root.title('Tdroid_Tool')
root.configure(bg='#D8D5C8')

icon = PhotoImage(file='icon.png')
root.iconphoto(True, icon)
root.resizable(False, False)
root_wid = 900
root_hi = 600
#menu bar like
#menubar actions



screen_wdth = root.winfo_screenwidth()
scree_height = root.winfo_screenwidth()
cent_screen = int(screen_wdth / 1 - root_wid)
cent_screenh = int(scree_height / 2 - root_hi)
root.geometry(f'{root_wid}x{root_hi}+{cent_screen}+{cent_screenh}')
# end of root sizings
# labells
# lebo = Label(root,text='model',padx=30,pady=10).place(x=400,y=0)
# frames
frem = Frame(root, height=600, width=100, )
frem.columnconfigure(0, weight=1)
frem.grid(pady=0, padx=0)

frem2 = Frame(root)
frem2.grid(column=2, row=0)

frem3 = tk.Frame(root,height=600,width=100)
frem.columnconfigure(0,)
frem3.grid(column=3,row=0)


logfield = tk.Text(root, background='black', foreground='white')
logfield.grid(column=2, row=0, pady=40)
logfield.insert(END, 'logging')


def butt(txt, nem):
    nem = tk.Button(frem, text=txt, )
    nem.configure(fg='white', background='black', borderwidth=1, width=14)
    nem.grid(pady=10, padx=10, sticky=W)
    return nem


# detect=tk.Button(frem,text='Detect',)
# model list

'''drop list
model= tk.Listbox(root,height=5,listvariable=tk.StringVar(value=mdellist))
model.grid(row=0,column=10,sticky=NW,pady=25,padx=10)
'''
#function to create dialog boxest
def filedialog(name):
    namedir = filer.asksaveasfile(filetypes=[('bin file','*.bin')]
                               ,initialdir=f"{os.getcwd()}/backup")
    restore = filer.askopenfilename(filetypes=['*.bin','*.img'])
    return namedir

# fastboot pane frame

# detect.place(x=10,y=50)
# detect.configure(bg='black',foreground='white',borderwidth=2,font='ubuntu')
BackUp = butt(txt='BackUp Nv', nem='BackUp')
BackUp.grid(row=1, column=0)
BackUp.configure(command=lambda :filedialog('backupdir'))

Detect = butt(txt='Detect(ADB)', nem='Detect', )
Detect.grid(row=0, column=0, )
usbdet = tk.Button(frem3,text='Detect(usb)')
usbdet.grid(column=3,row=0)
#neded to delete text and write usb fileds filters by  pid and vid plu probbly the busnumber
usbdet.configure(command=lambda:(logfield.insert(END,list(usbdevices))))
#this lambda function frist deletes the context of the
# text field and then writes from the function to make logs look much readeable
Detect.configure(command=
                 ((lambda:logfield.delete(1.0,END)or(logfield.insert(END,f' \ndevice with \n{adbConnect()}\n found')))))


Restore = butt(txt='Restore Nv', nem='Restore')
Restore.grid(row=2, column=0)
Restore.config(command=lambda :filedialog('Restorenv'))
fix = butt(txt='fix baseband', nem='fix')
fix.configure(font='arial 10', width=14)
fix.grid(row=3, column=0)
mount = butt(txt='mount baseband', nem='mount')
mount.grid(row=4, column=0)
mount.configure(width=14)
mount.config(font='ubuntu 9')
mount.config(padx=10)

BackUpEfs = butt(txt='Backup Efs', nem='BackupEfs')
BackUpEfs.grid(row=5, column=0)
BackUpEfs.config(command=lambda :filedialog('Efs location'))

RestoreEfs = butt(txt='Restore Efs', nem='RestoreEfs')
RestoreEfs.grid(row=6, column=0)
RestoreEfs.config(command= lambda
                           :filedialog('RestoreEfs'))

Listpackages = butt(txt='List Apps', nem='apps')
Listpackages.grid(row=7, column=0)

# Listpackages.config(command=listApps)


class model_selection():
    def selection(model):
        return model

        '''if model == str('sm-a127f') or model == str('sm-a135f'):
          print('selected model is eynos')'''

    mdellist = ['sm-a125f', 'sm-a127f', 'sm-a135f', 'sm-a022f', 'sm-a225f']
    sel = tk.StringVar()

    # if fast.get()=='model':
    #   return fast.get()
    # else:
    #    logfield.insert(tkinter.END,f'scanning for {fast.get()}')
    modeloption = tkinter.ttk.Combobox(root, textvariable=sel, justify="center")
    modeloption['state'] = 'readonly'
    modeloption['values'] = mdellist


    # modeloption = ttk.OptionMenu(root, fast, *mdellist, command=selection)

    modeloption.place(x=400, y=10)
    # modeloption.configure(compound="bottom",anchor="center",direction="below",)

    '''if fast.get() != str('model'):
        logfield.insert(tkinter.END, f'scanning for {fast.get()}')
        print({fast.get()})

    else:
     return 0'''

def fastbootpane():
  try:
      '''frem.grid_forget()
      frem2.grid_forget()
      frem3.grid_forget()'''
      model_selection.modeloption.place_forget()
      itemremover = [Detect,BackUp
          ,BackUpEfs,RestoreEfs,Restore,fix,mount]
      for item in itemremover:
          item.grid_forget()
      '''fbframe1 = tk.Frame(root,bg='white')
      fbframe1.grid(column=0,row=0)
      frame1 = tkinter.Frame(root)
      frame1.grid(column=0, row=0)
      detectfb.pack()'''
      detectfb = butt('Detect Fastboot','detectfb')
      detectfb.config(command=fastbootpy.fbdevices())
      detectfb.grid(column=0,row=0)
  except:
      pass

#samsung pane frame
def samsungpane():
    Listpackages.grid_forget()
    try:
        detectfb.grid_forget()
    except:
        RestoreEfs.grid(row=6, column=0,pady=10, padx=10, sticky=W)
        model_selection.modeloption.place_forget()
        BackUpEfs.grid(row=5, column=0,pady=10, padx=10, sticky=W)
        mount.grid(row=4, column=0,pady=10, padx=10, sticky=W)
        fix.grid(row=3, column=0,pady=10, padx=10, sticky=W)
        BackUp.grid(row=1, column=0,pady=10, padx=10, sticky=W)
        Detect.grid(row=0, column=0, pady=10, padx=10, sticky=W)
        Restore.grid(row=2, column=0,pady=10, padx=10, sticky=W)
        model_selection.modeloption.place(x=400, y=10)

menubar = tk.Menu(root,activeborderwidth='20')
samenu = menubar.add_command(label='Samsung Tools',command=samsungpane)
adbmenu = menubar.add_command(label='Adb Tools')
fbootmenu = menubar.add_command(label='Fastboot tools',command=fastbootpane)
root.config(menu=menubar)


flashfield = tk.Frame(root, height=130, width=640)
fileselector = tk.Frame(root, height=130, width=100)
fileselector.grid(column=0, row=1)
fileselector.config(background='white')
flashfield.grid(column=2, row=1)

flashfield.config(bg='white')
model_selection()

root.mainloop()
