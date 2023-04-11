import usb.core

# Find device with specific vendor ID and product ID
dev = usb.core.find(idVendor=0x04e8, idProduct=0x6860)
#samsung mtp USB\VID_04E8&PID_6860

if dev is None:
    print("Device not found.")
else:
    print("Device found.")
    print(dev)
    # Print iManufacturer descriptor
    try:
        ncd = usb.util.get_string(dev,dev.INTERFACE)
        print(ncd)
        manufacturer = usb.util.get_string(dev, dev.iManufacturer)
        print("Manufacturer: " + manufacturer)
    except:
        print("Manufacturer descriptor not available.")

    # Print iProduct descriptor
    try:
        product = usb.util.get_string(dev, dev.iProduct)
        print("Product: " + product)
    except:
        print("Product descriptor not available.")

    # Print iSerialNumber descriptor
    try:
        serial_number = usb.util.get_string(dev, dev.iSerialNumber)
        print("Serial number: " + serial_number)
    except:
        print("Serial number descriptor not available.")

    # Print the interface class string descriptor
    try:
        cfg = dev.get_active_configuration()
        intf = cfg[(0, 0)]
        bInterfaceClass = usb.util.get_string(dev, intf.bInterfaceClass)
        print("Interface class: " + bInterfaceClass)
    except:
        print("Interface class descriptor not available.")
