import usb
from usb.backend import libusb1


def usbsni():
    for i in usb.core.find(True,libusb1):
        print(i)

usbsni()