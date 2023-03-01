import subprocess
import tkinter
import time
from ppadb.client import Client as AdbClient

# Default is "127.0.0.1" and 5037
logs = open('logs/logs.txt', 'w')
host = '127.0.0.1'
port = 5037


class startDaemon:
    # try:
    start = subprocess.run(['daemon/adb.exe', 'start-server'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)



client = AdbClient(host, port)


# starting
#
# the adb server using adb.exe
