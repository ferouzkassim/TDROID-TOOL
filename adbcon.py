import subprocess
import tkinter
import time
from ppadb.client import Client as AdbClient
import os.path

import gui.logfield

logs = open("logs/logs.txt",'w')

def startDaemon(bing=None):
    #try:
        subprocess.run(['daemon/adb.exe','start-server'])
        subprocess.run(['daemon/adb.exe','devices'],
                       stdout= bing
                       )
        #logfield.insert(tkinter.END, bing)
                       #stdout=logs)
    ##except '':
      #  subprocess.run(['daemon/adb.exe', 'usb'])
       # subprocess.run(['daemon/adb.exe','kill-server'])
        #return logs

#starting the adb server using adb.exe
startDaemon()
client = AdbClient(host="127.0.0.1", port=5037)








