import usb
import usb1
from usb import *
'''for dev in usb.core.find(find_all=True):
    print (dev.serial_number)'''

print (usb.core.show_devices())

for dev in usb1.USBContext.getDeviceList():
    print(dev)
    