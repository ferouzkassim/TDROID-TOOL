import tkinter
from adbcon import startDaemon,host,port,client
#importing the class to do detecting and exposing the srial number
def adbConnect():
    startDaemon.start

    client.devices()
    for dev in client.devices():
        dev.shell('getprop')
        return dev.serial
#first things frst start the server then get devices
#then enumrate to get index and enumerate to get the respondent app
#apend it to a blank list the return the listy with the index and app appnended to it
class detect:
    def __init__(self):
        for dev in client.devices():
          return dev[0]

    def applister(self):
        startDaemon.start
        applist=[]
        for dev in client.devices():
            dev.get_state()
            for appindex,app in enumerate(dev.list_packages()):
              applist.append(f'{appindex}: -> {app}')
#rto ad a new line on each app and index
        return '\n'.join(applist)


    def shellconnector(self):
        def readfromdev(connection):
            data = []
            try:
                while True:
                    chunk = connection.read(1024)
                    if not chunk:
                        break
                    data.append(chunk.decode('utf-8'))
                return ''.join(data)

            except Exception as error:
                pass
            finally:
                    connection.close()


class partmount(detect):
    def __init__(self):
        super(self).__init__()
        super().shellconnector()

    pass





suchecker = detect
suchecker.shellconnector(suchecker)



