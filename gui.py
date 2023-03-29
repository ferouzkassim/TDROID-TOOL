import logging
import tkinter.ttk
import os

import loggs
from usbcom import usbdevices
import detect
import fastboot
import samsung
import threading
import loggs
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from detect import *
from detect import detect as dt
from tkinter import filedialog as filer
from fastbootpy import *
root = tk.Tk()
# root the frame poatiioning and such
root.title('Tdroid_Tool')
root.configure(bg='#D8D5C8')

icon = PhotoImage(file='icon.png')
root.iconphoto(True, icon)
root.resizable(False,True)
root_wid = 900
root_hi = 700
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

global logfield


logfield = tk.Text(root,background='black',
                   foreground='white',font='ubuntu')

logfield.grid(column=2, row=0, pady=20)


scroll = tk.Scrollbar(logfield, orient=tk.VERTICAL, command=logfield.yview)
scroll.place(relx=1.0, rely=0, relheight=1.0, anchor=tk.NE)

logfield.config(yscrollcommand=scroll.set,cursor='arrow')
logfield.insert(tk.END, 'logging')
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
def filedialog(name):
    backup = filer.asksaveasfilename(defaultextension='.td',initialdir=('/backup'),
                                 filetypes=[(('bin file','*.bin'),
                                              ('td file','*.tdf')
                                             )])


    return backup
def fileres(name):
    part_restore_file = filer.askopenfilename(defaultextension='.tar',initialdir=('/backup'),
                                 filetypes=[('bin file', '*.bin'),
        ('td file', '*.tdf'),
        ('tar files', '*.tar'),
                                            ('img files','*.img')])
    return part_restore_file
#function to create dialog boxest

# fastboot pane frame
# detect.place(x=10,y=50)
# detect.configure(bg='black',foreground='white',borderwidth=2,font='ubuntu')
def bakup_nv():
    logfield.delete(1.0, END)
    result = [backuping.PartBackup(BackUP, filedialog('efs'), 'efs'),
              backuping.puller(BackUP,backuping.PartBackup(BackUP, filedialog('efs'), 'efs')[1],filedialog('efs')),
              backuping.zipper(BackUP,filedialog('efs'))]

    if result is not None:
        logfield.insert(END, result[0])
        logfield.insert(END, backuping.puller(BackUP, result[1], result[2]))


BackUp = butt(txt='BackUp Nv', nem='BackUp')
BackUp.grid(row=1, column=0)
BackUp.configure(command=lambda:bakup_nv())

##login to the lgfiled from line 105 to 119

Detect = butt(txt='Detect(ADB)', nem='Detect', )
Detect.grid(row=0, column=0, )
Detect.configure(command=lambda: asyncio.run(loggs.adinfo(logfield)))

usbdet = tk.Button(frem3,text='Detect(usb)')
usbdet.grid(column=3,row=0)
#neded to delete text and write usb fileds filters by  pid and vid plu probbly the busnumber
usbdet.configure(command=lambda:(logfield.delete(1.0,END),
                                 (logfield.insert(END,f'{detectusb}'))))
#this lambda function frist deletes the context of the
# text field and then writes from the function to make logs look much readeable


Restore = butt(txt='Restore Nv', nem='Restore')
Restore.grid(row=2, column=0)
def restore_backup():
    logfield.delete(1.0, END)
    result = backuping.part_restore(BackUP, fileres('efs'), 'efs')

    if result is not None:
        logfield.insert(END, result[0])
        logfield.insert(END,backuping.pusher(BackUP, result[1], result[2]))

Restore.configure(command=lambda :[logfield.delete(1.0,END),
                        restore_backup()])
fix = butt(txt='Fix Baseband', nem='fix')
fix.configure(font='arial 10', width=14)
fix.config(command=lambda :[logfield.delete(1.0,END),
                            logfield.insert(1.0,Partmnt.part_mount(BackUP,'efs'))])
fix.grid(row=3, column=0)
mount = butt(txt='Mount Baseband', nem='mount')
mount.grid(row=4, column=0)
mount.configure(width=14,command=lambda :[logfield.insert(END,f'\n{detector.shellconnector}')])
mount.config(font='ubuntu 9')
mount.config(padx=10)

BackUpEfs = butt(txt='Backup Efs', nem='BackupEfs')
BackUpEfs.grid(row=5, column=0)
BackUpEfs.config(command=lambda:[logfield.delete(1.0,END),logfield.insert(END,backuping.PartBackup(
    BackUP,filedialog('efs'),["efs","sec_efs","cpefs"]
))])

RestoreEfs = butt(txt='Restore Efs', nem='RestoreEfs')
RestoreEfs.grid(row=6, column=0)
RestoreEfs.config(command= lambda
                           :[restoring.part_restore(BackUP,fileres('efs'),'efs')])

Listpackages = butt(txt='List Apps', nem='apps')
#Listpackages.master()
Listpackages.grid(row=7, column=0)
apps = detect

Listpackages.config(command=lambda:[logfield.
                    delete(1.0,END),

                     logfield.insert(END, f'{apps.applister(apps)}')
                     ,detector.searcher(logfield)])
# Listpackages.config(command=listApps)
sn_repair  = butt('Repair SN',nem='apps')
sn_repair.grid(row=7,column=0)
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
    '''modeloption = tkinter.ttk.Combobox(root, textvariable=sel, justify="center")
    modeloption['state'] = 'readonly'
    modeloption['values'] = mdellist///
    modeloption.place(x=400, y=10)'''


    # modeloption = ttk.OptionMenu(root, fast, *mdellist, command=selection)


    # modeloption.configure(compound="bottom",anchor="center",direction="below",)

    '''if fast.get() != str('model'):
        logfield.insert(tkinter.END, f'scanning for {fast.get()}')
        print({fast.get()})

    else:
     return 0'''

def fastbootpane():
    try:
        model_selection.modeloption.place_forget()
        itemremover = [Detect, BackUp, BackUpEfs, RestoreEfs, Restore, fix, mount]
        for item in itemremover:
            item.grid_forget()

        if not hasattr(fastbootpane, "detectfb"):
            fastbootpane.detectfb = butt('Detect Fastboot', 'detectfb')
            fastbootpane.detectfb.config(command=fastbootpy.fbdevices)
            fastbootpane.detectfb.grid(column=0, row=0)

    except:
        if hasattr(fastbootpane, "detectfb"):
            fastbootpane.detectfb.grid(column=0, row=0)
        pass

#samsung pane frame
def samsungpane():
    Listpackages.grid_forget()
    try:

        detectfb.grid_forget()
    except:
        RestoreEfs.grid(row=6, column=0,pady=10, padx=10, sticky=W)

        BackUpEfs.grid(row=5, column=0,pady=10, padx=10, sticky=W)
        mount.grid(row=4, column=0,pady=10, padx=10, sticky=W)
        fix.grid(row=3, column=0,pady=10, padx=10, sticky=W)
        BackUp.grid(row=1, column=0,pady=10, padx=10, sticky=W)
        Detect.grid(row=0, column=0, pady=10, padx=10, sticky=W)
        Restore.grid(row=2, column=0,pady=10, padx=10, sticky=W)


menubar = tk.Menu(root,activeborderwidth='20')
adbmenu = menubar.add_command(label='Adb Tools')
samenu = menubar.add_command(label='samsung Tools')
fbootmenu = menubar.add_command(label='Fastboot tools',command=fastbootpane)
root.config(menu=menubar)

'''firmwarefield = tk.Frame(root,width=600,height=300)
firmwarefield.config(bg='white')
firmwarefield.grid(row=1,column=0)'''
#flashfiled for samsung

#. This will allow you to allocate more space to other widgets in the grid.
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=5)
#logging part


root.mainloop()
