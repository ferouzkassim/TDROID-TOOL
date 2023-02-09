import tkinter
from adbcon import startDaemon,host,port,client
#importing the class to do detecting and exposing the srial number
def adbConnect():
    startDaemon.start

    client.devices()
    for dev in client.devices():

        return dev.serial
#first things frst start the server then get devices
#then enumrate to get index and enumerate to get the respondent app
#apend it to a blank list the return the listy with the index and app appnended to it


def applister():
    startDaemon.start
    applist=[]
    for dev in client.devices():
        dev.get_state()
        for appindex,app in enumerate(dev.list_packages()):
         applist.append(f'{appindex}: -> {app}')
#rto ad a new line on each app and index
    return '\n'.join(applist)

def adbshellroot():
    startDaemon
    '''connection object. The function reads data from the connection in 1024-byte chunks and decodes it using the utf-8 encoding. The decoded data is then printed to the console.

The function uses a while loop to continuously read data from the connection until there is no more data available (indicated by the not data condition). If no more data is available, the loop 
breaks and the function closes the connection using the close() method.'''
    def readfromdev(connec):
        while True:
            data = connec.read(1024)
            if not data:
                break
            return data.decode('utf-8')

            readfromdev.close()
        for dev in client.devices():
         sn = dev.get_serial_no()
         print(connector.read(all()))
         dev.shell('su',handler=None)

adbshellroot()

'''for dev in client.devices():
    sn = dev.get_serial_no()
    #  print(connector.read(all()))
dev.shell('su', handler=readfromdev)'''


