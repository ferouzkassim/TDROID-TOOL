import subprocess

from ppadb.client import Client as client
from ppadb.connection import Connection
from ppadb.client import Client as AdbClient

# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
print(client.devices())
client.features()
def startserver():
    subprocess.run(['daemon/adb.exe','start-server'])
#startserver()
