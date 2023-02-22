import tkinter
from adbcon import startDaemon,host,port,client
#importing the class to do detecting and exposing the srial number
def adbConnect():
    startDaemon.start
    prop = []
    client.devices()
    for dev in client.devices():

        return (dev.serial,
                dev.shell('getprop'))
#first things frst start the server then get devices
#then enumrate to get index and enumerate to get the respondent app
#apend it to a blank list the return the listy with the index and app appnended to it
class detect:
    def __init__(self):
       pass

    def applister(self):
        startDaemon.start
        applist=[]
        for dev in client.devices():
            dev.get_state()
            for appindex,app in enumerate(dev.list_packages()):
              applist.append(f'{appindex}: -> {app}')
#rto ad a new line on each app and index
        return '\n'.join(applist),dev

    def shellconnector(self,):
        device = []





        return device




class partmount(detect):
    def __init__(self):
        super().__init__()
        super().shellconnector()

    def efsmount(self):
        device = super().shellconnector()
        print(device[0])


detector = detect()

mounter = partmount()




