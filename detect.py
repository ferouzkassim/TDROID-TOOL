
from adbcon import startDaemon,host,port,client
#importing the class to do detecting and exposing the srial number
def adbConnect():
    client.devices()
    for dev in client.devices():
        print(
            dev.serial
        )
        return dev.serial










