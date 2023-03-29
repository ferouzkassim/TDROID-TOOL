import usb
import usb.core
import usb.control,usb.legacy
import usb1
from usb import *
'''for dev in usb.core.find(find_all=True):
    print (dev.serial_number)'''
def usbdevices():
    devList = usb.core.find(True)
    samdev = usb.core.find( idVendor = 0x04e8,
 idProduct=0x6860)
    atatched_devices = []
    for dev in devList:
        atatched_devices.append(dev)
    if samdev:
        print('samsung device found')
        print(samdev)
        endpoint = dev[0][(0, 0)][0]
        endpoint = dev[0][(0, 0)][0]
        endpoint = dev[0][(0, 0)][0]

