import subprocess
import tkinter

from ppadb.client import Client as AdbClient
import os.path


def startDaemon():
    try:
        subprocess.run(['daemon/adb.exe','start-server'],)
    except '':
        subprocess.run(['daemon/adb.exe', 'usb'])
        subprocess.run(['daemon/adb.exe','kill-server'])

#starting the adb server using adb.exe
startDaemon()
client = AdbClient(host="127.0.0.1", port=5037)








