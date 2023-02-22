import usb
import usb.core
import usb.control,usb.legacy
import usb1
from usb import *
'''for dev in usb.core.find(find_all=True):
    print (dev.serial_number)'''
def usbdevices():
    devList = usb.core.find(True)
    samdev = usb.core.find(idVenor='0x4E8',idProvider='0x685D')
    for dev in devList:
        print(dev.parent)
        print(type(dev.parent))
    print(samdev)

