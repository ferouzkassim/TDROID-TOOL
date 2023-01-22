import subprocess
import tkinter
import time
from ppadb.client import Client as AdbClient
    # Default is "127.0.0.1" and 5037
logs = open('logs/logs.txt', 'w')
host='127.0.0.1'
port=5037
client = AdbClient(host,port)

class startDaemon:
    # try:
    start = subprocess.run(['daemon/adb.exe', 'start-server'])

# starting
#
# the adb server using adb.exe
def startShell():
    startDaemon.start
    #client.create_connection(timeout=200)
    client.devices()
    for device in client.devices():
        print(device.serial)
    '''for package in device.list_packages():
            package = logs'''




