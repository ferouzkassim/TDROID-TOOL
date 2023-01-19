import tkinter

from adbcon import *
#from gui import logfield


def Dtect():
    startDaemon()
    from gui import logfield
    logfield.insert(tkinter.END,f'    connecting through {client.host}:{client.port}')

