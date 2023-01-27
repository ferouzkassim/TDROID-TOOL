import usb
import usb1
from usb import *
'''for dev in usb.core.find(find_all=True):
    print (dev.serial_number)'''

dev_list = usb.core.show_devices()
usb.TYPE_VENDOR
vend= usb.busses()
#for dev in vend:
 #   print(dev)

