import usb
import usb.core
import usb.control,usb.legacy
import usb1
from usb import *
'''for dev in usb.core.find(find_all=True):
    print (dev.serial_number)'''
def usbdevices():
    devList = usb.core.find(True)
    devusb = []
    busses = usb.TYPE_VENDOR.bit_length()
    tx = usb1.USBTransfer
    for indic,usbdev in enumerate(devList):
     devusb.append(f'{indic}:->vendor {hex(usbdev.idVendor)}  '
                   f' product ->{hex(usbdev.idProduct)}  '
                   f'usb :->{usbdev.iManufacturer}')
    for de in devusb:
        print(de)
    return f'\n{de}'
