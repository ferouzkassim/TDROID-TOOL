import subprocess
import sys
import tkinter
from adbcon import startDaemon, host, port, client
import time


#importing the class to do detecting and exposing the srial number
def adbConnect():

    prop = []
    resultprop = {}
    filteredprops={}
    #the filtered keys to look for in prop
    filter_keys = [

        'ro.product.model',
        'ro.product.name',
        'ro.build.id',
        'ro.build.product'
        'ro.build.version.release',
        'ro.build.version.security_patch',
        'ro.build.PDA',
        'ro.carrier',
        'ro.config.knox',
        'ro.csc.country_code',
        'ro.frp.pst',
        'ro.hardware.chipname',
        'ro.serialno',
        'sys.usb.config',
        'Build.BRAND',
        'gsm.version.baseband',
        'knox.kg.state',
        'ril.modem.board',
        'gsm.network.type',
        'gsm.operator.iso-country',
        'gsm.version.baseband',
        'gsm.operator.alpha',
        'gsm.operator.iso-country',

    ]
    for dev in client.devices():
        propstr = dev.shell('getprop')
        prop.append(propstr.split('\n'))
        for sublist in prop:
            for stringprop in sublist:
                clean_string = stringprop.strip()\
                    .replace("[", "").replace("]", "")

                if clean_string and ':' in clean_string:
                    key, value = clean_string.split(': ')

                    resultprop[key] = value
                    if key in filter_keys:
                        filteredprops[key] = value
                    output = f"{dev.serial}\n"
                    for prop, answer in filteredprops.items():
                        output += f"{prop} = {answer}\n\n"



    return f'{output}'

#first things frst start the server then get devices
#then enumrate to get index and enumerate to get the respondent app
#apend it to a blank list the return the listy with the index and app appnended to it
class detect:
    def __init__(self):

        pass

    def applister(self):

        applist = []
        if client.devices():

         for dev in client.devices():
            dev.get_state()
            for appindex,app in enumerate(dev.list_packages()):
              applist.append(f'{appindex}: -> {app}')

#rto ad a new line on each app and index

        else:
         applist.append('No Device Found')
        return '\n'.join(applist)


    def searcher(self,holder):
        self.holder = holder
        search = tkinter.Entry(holder)

        search.place(relx=1.0,rely=0,anchor=tkinter.NE,width=300)
    def shellconnector(self,):






        return




class partmount(detect):
    def __init__(self):
        super().__init__()
        super().shellconnector()

    def efsmount(self):
        device = super().shellconnector()


class BackUP(detect):
    def __init__(self, pclocation,PartName):
        super().__init__()
        startDaemon()
        self.pclocation = pclocation
        self.Partname = PartName
# a function that is gonna find the rootfs of the device and return t
    #the location so taht any part can be backed up regardless of the chip or device
    def PartBackup(self, pclocation,part_name):
        device = startDaemon()
        locations = 'dev/block/platform'
        for dev in client.devices():
            if dev.serial == device:
                #su - c breaks out of the su waiting time and lets you execute once
                devloc = dev.shell(f'su -c cd {locations}/')
                #response = dev.shell(f'su -c "dd if=/{locations}'
                #f'/bootdevice/by-name/efs of=/sdcard/efs.tdf"')'''
                print(devloc)
                print(locations)
                ls_output = dev.shell(f'su -c ls {locations}/')
                partition_path = f'/{locations}/{ls_output.strip().split()[-1]}'
                backup_command = f'su -c "dd if={partition_path}/by-name/{part_name} of=/storage/emulated/0/{part_name}.tdf"'
                bckup = dev.shell(backup_command)
                # Do backup here
                print(partition_path)
                print(bckup)
                return bckup
                #print(dev.shell(f'su -c cd /{locations}'))
                #bckup = dev.shell((f'su -c "dd if=/{locations}/{ls_output}by-name/efs" of=/storage/emulated/0/{part_name}.tdf'))
                # Do backup here
                #print(ls_output)
                #print(bckup)
                break
                return response
            else:
                response = 'device not found'
                print('Device not found')
                break
                return response




detector = detect()
backuping  = BackUP
backuping.PartBackup(BackUP,'/c','efs')


'''import ppadb.client
import time

adb = ppadb.client.Client()
devices = adb.devices()
if len(devices) == 0:
    print('No device found')
    quit()

device = devices[0]

# Start the ADB daemon on the device
device.shell('su -c "cd /data/local/tmp && ./adb_daemon" &')

# Wait for the daemon to start
time.sleep(1)

# Connect to the daemon using a new ADB connection
daemon_device = adb.device(serial=device.serial)

# Get a root shell
shell = daemon_device.shell('su')
print(shell)

# Send some commands to the shell
shell.send('ls\n')
response = shell.receive()
print(response)

shell.send('id\n')
response = shell.receive()
print(response)

shell.send('exit\n')
response = shell.receive()
print(response)

# Close the shell
shell.close()
'''

