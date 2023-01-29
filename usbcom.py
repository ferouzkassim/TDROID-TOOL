import usb
import usb1
from usb import *
'''for dev in usb.core.find(find_all=True):
    print (dev.serial_number)'''

devList = usb.core.show_devices()
busses = usb.TYPE_VENDOR.bit_length()
tx = usb1.USBTransfer
print(usb1.Version._fields.count())
