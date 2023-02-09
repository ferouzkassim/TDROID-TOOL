import subprocess

from ppadb.client import Client as client
from ppadb.connection import Connection
from ppadb.client import Client as AdbClient

# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)

def startserver():
    starting = subprocess.run(['daemon/adb.exe','start-server'])
    logs = starting.stdout
    return logs
