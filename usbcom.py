import usb
import usb.core
import usb.control,usb.legacy
import usb1
from usb import *
'''for dev in usb.core.find(find_all=True):
    print (dev.serial_number)'''
def usbdevices():
    devList = usb.core.find(True)
    devusb = {}
    busses = usb.TYPE_VENDOR.bit_length()
    tx = usb1.USBTransfer
    for indic,usbdev in enumerate(devList):
     devusb[indic]=(f'Vendor  {hex(usbdev.idVendor)}',
                    f'Product  {hex(usbdev.idProduct)}')
    return f'\n{devusb}'

detectusb = usbdevices
#devList = usb.core.find(True)
#print(usb.core.show_devices(True))

