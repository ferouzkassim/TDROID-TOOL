import subprocess
import tkinter
import time
from ppadb.client import Client as AdbClient
from subprocess import PIPE

# Default is "127.0.0.1" and 5037
logs = open('logs/logs.txt', 'w')
host = '127.0.0.1'
port = 5037

def startDaemon():
    start = subprocess.run(['daemon/adb.exe', 'start-server'], capture_output=True)
    device = None
    shell_output = start.stdout.decode()
    for dev in client.devices():
        device = dev.serial
    return device


host = '127.0.0.1'
port = 5037
client = AdbClient(host, port)
device0 = startDaemon()




# starting
#
# the adb server using adb.exe
