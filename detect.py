from adbcon import *
from ppadb.device import Device
logs=open('logs/logs.txt','w')

def detectfunc():
    startDaemon.start
    client.devices()
    for device in client.devices():
        snmbr = device.serial
        print(type(snmbr),snmbr)
detectfunc()