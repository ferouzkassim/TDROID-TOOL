import tkinter

from adbcon import *
#from gui import logfield


def Dtect():
    startDaemon()
    #managing loggs

    from gui import logfield
    with open(logs,"r") as txt:
        logging=txt.read()
        print(logging)
    logfield.insert(tkinter.END,f'' )


