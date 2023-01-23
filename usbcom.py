import usb
from usb import *
for dev in usb.core.find(find_all=True):
    prod = dev.port_number
    conf=dev.configurations()
usb.core.show_devices(True)