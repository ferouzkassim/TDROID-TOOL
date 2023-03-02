import subprocess
from ppadb.client import Client as AdbClient

def startDaemon():
    client = AdbClient(host="127.0.0.1", port=5037)
    device = None
    for dev in client.devices():
        device = dev.serial
    if device is None:
        subprocess.run(["adb", "start-server"])
        for dev in client.devices():
            device = dev.serial
    return device

