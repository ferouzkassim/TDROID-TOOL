
from adbcon import *
import tkinter as tk


def detectfunc(self):
    devices = client.devices()
    for dev in devices:
        serial = dev.serial
    return serial


def listApps():
    devices = client.devices()
class detecting :
    def __init__(self):
        pass


#writitng /pprinting function



