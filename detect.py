
from adbcon import *
import tkinter as tk


#importing the class to do detecting and exposing the srial number
class detecting :
    def __init__(self):
        pass
    @classmethod
    def detectfunc(cls):
        devices = client.devices()
        if devices:

         for dev in devices:
            serial = dev.serial
         return serial


    def listApps(self):
        pass


#writitng /pprinting function


def detct():
    detect = detecting.detectfunc()
    with open('logs/logs.txt', 'a') as log:
           log.write(detect)
    return detect
    print('bingo')
#detct()
def listApps():
    detect = detecting.detectfunc()
    applist=[]
    for dev in  client.devices():
        dev.list_packages()
        for app in dev.list_packages():
             applist.append(app)
             print(applist)
             return applist,app
listApps()

