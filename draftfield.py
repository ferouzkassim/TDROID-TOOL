import usb.core
import usb.backend.libusb1 as libusb1

# Set the backend to libusb1
backend = libusb1.get_backend()

# Find the USB device using vendor and product IDs
vendor_id = 0x18d1
product_id = 0x4ee0

# Find the USB device based on vendor ID and product ID with libusb1 backend
device = usb.core.find(idVendor=vendor_id, idProduct=product_id, backend=backend)

if device is None:
    print("Device not found.")
else:
    print("Device found:", device)
