import subprocess
import asyncio
import time
from adb_shell.adb_device import *
from ppadb.client import Client as AdbClient
from subprocess import PIPE

# Default is "127.0.0.1" and 5037
#logs = open('logs/logs.txt', 'w')
host = '127.0.0.1'
port = 5037
def startDaemon():
    # Start the adb server
    try:
        subprocess.run(['daemon/adb.exe', 'start-server'], capture_output=True)
    except FileNotFoundError:
        print('restarting server at')
        subprocess.run(['daemon/adb.exe', 'kill-server'])
    # Find the first connected device
    device = None
    for dev in client.devices():
        device = dev.serial
        print(device)
    return device

def stopDaemon():
    subprocess.run(['daemon/adb.exe','kill-server'])

host = '127.0.0.1'
port = 5037
client = AdbClient(host, port)

# starting
#
# the adb server using adb.exe
