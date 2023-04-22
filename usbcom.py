import usb.core
import usb.core
import usb.backend.libusb1
import serial.tools.list_ports as prtlist
import usb.util
from PyQt6 import QtSerialPort
from typing import List
import serial
import serial.tools.list_ports as prtlst
import usb1
from serial.tools import list_ports_common
import time

# borrowing from https://github.com/FICS/atcmd
# borrowing also from https://github.com/riskeco/Samsung-FRP-Bypass
# define SAMSUNG_VENDOR_ID  	0x04e8
# define SAMSUNG_PRODUCT_ID 	0x6860
# USB\VID_1782&PID_4D00 spd device
# download mode samsung usb\vid_04e8&pid_685d

# Find the Samsung device in download mode
#dev = usb.core.find(idVendor=0x04e8, idProduct=0x685d, backend=usb.backend.libusb1.get_backend(find_library=lambda x: "libusb-1.0.dll"))
SERIAL_PORT = "/dev/ttyACM0"
GALAXY_ID_VENDOR = 0x04e8
GALAXY_ID_PRODUCT = 0x6860
#VID:PID=04E8:6860
# Set the configuration
'''dev.set_configuration()

# Get the first interface
interface = dev.get_active_configuration()[(0,0)]

# Get the first endpoint
endpoint = interface[0]

# Read the first 10 bytes from the endpoint
data = dev.read(endpoint.bEndpointAddress, 10)

# Print the data
print(data)



# Find the USB device in usb modem mode
dev = usb.core.find(idVendor=0x04e8, idProduct=0x685d)

# Set the active configuration
cfg = dev.get_active_configuration()
interface_number = cfg[(0,0)].bInterfaceNumber
alternate_setting = usb.control.get_interface(dev, interface_number)
intf = usb.util.find_descriptor(
    cfg, bInterfaceNumber = interface_number,
    bAlternateSetting = alternate_setting
)
dev.set_configuration(cfg)

# Now you can send/receive data from the device'''
# enable adb from atcommands using this functions

SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 12


def pyusbports():
    # print(dev[0].iConfiguration)
    # print(dev[0])
    dev = usb.core.find(idVendor=0x04e8, idProduct=0x6860)
    cfg = dev[0]
    interface = usb.util.find_descriptor(
        cfg,
        bInterfaceClass=0x2,  # CDC Communication interface
        bInterfaceSubClass=2,  # Abstract Control Model (ACM)
        bInterfaceProtocol=1,  # V.25ter
    )
    endpoint = dev[0][(interface, 0)][0]

    # Read data from the interrupt endpoint
    data = endpoint.read(endpoint.wMaxPacketSize)
    print(data)


def list_serial_ports() -> list_ports_common.ListPortInfo:
    response = ''
    ports = prtlst.comports()
    if len(ports) == 0:
        response += "No serial port available"
        exit(1)
    response += "####### Available serial ports #######"
    for port, desc, hwid in sorted(ports):
        ser = serial.Serial(port, 115200, timeout=1)
        # ser.write(b'AT+GSN')
        ser.write(b'AT+CLAC')
        response += desc
        # Read the response from the device
        respo = ser.read(1024).decode('ascii')

        # Print the response
        response += respo
    ports[0]

    response += "####### End of available serial ports #######"
    return port, response


def get_AT_serial(port: str) -> serial.Serial:
    return serial.Serial(port, baudrate=SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT)


def ATSend(io: serial.Serial, cmd: str) -> bool:
    if not io.isOpen():
        return False
    print(f"Sending {cmd.encode()}")
    io.write(cmd.encode())
    time.sleep(0.5)
    ret = io.read_all()
    print(f"Received {ret}")

    if b"OK\r\n" in ret:
        return True
    if b"ERROR\r\n" in ret:
        return False
    if ret == b"\r\n":
        return False
    if ret == cmd.encode():
        return True
    if ret == b'':
        return False
    return True


def tryATCmds(io: serial.Serial, cmds: List[str]):
    for i, cmd in enumerate(cmds):
        print(f"Trying method {i}")
        try:
            res = ATSend(io, cmd)
            if not res:
                print("OK")
        except:
            print(f"Error while sending command {cmd}")
    try:
        io.close()
    except:
        print("Unable to properly close serial connection")


def enableADB():
    response = ''
    default_port = list_serial_ports()
    port = list_serial_ports()[0]
    io = get_AT_serial(port)
    response += "Initial..."
    # Seems to check if we are in *#0*# mode but apparently not working on the samsung I have
    ATSend(io, "AT+KSTRINGB=0,3\r\n")
    print("Go to emergency dialer and enter *#0*#, press enter when done")

    response += "Enabling USB Debugging..."
    cmds = []
    cmds.append("AT+CLAC\r\n")
    cmds.append("AT+DUMPCTRL=1,0\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")
    cmds.append("AT+SWATD=0\r\n")
    cmds.append("AT+ACTIVATE=0,0,0\r\n")
    cmds.append("AT+SWATD=1\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")
    tryATCmds(io, cmds)

    response += "USB Debugging should be enabled"
    response += "If USB Debugging prompt does not appear, try unplug/replug the USB cable"
    return response


# enableADB()
# list_serial_ports()
# pyusbports()
'''in pyusb but you can decidd to use serial library or pysub
bLength: The length of this descriptor in bytes (9 bytes).
bDescriptorType: The type of descriptor (configuration descriptor).
wTotalLength: The total length of this configuration descriptor and all of its associated descriptors (136 bytes).
bNumInterfaces: The number of interfaces in this configuration (4).
bConfigurationValue: The value used to select this configuration (1).
iConfiguration: The index of a string descriptor that describes this configuration. In this case, the descriptor cannot be accessed due to an error ("Error Accessing String").
bmAttributes: The attributes of this configuration. The 0x80 value indicates that the device is bus-powered (i.e. draws power from the USB bus).
bMaxPower: The maximum amount of current that this configuration may draw, in units of 2 mA. In this case, the value is 0xfa, which corresponds to 500 mA.'''


def seriyo():
    # USB\VID_18D1&PID_4EE8&REV_0404&MI_01
    # USB\VID_18D1&PID_4EE8&REV_0404&MI_00
    # USB\VID_1FC9&PID_82B3&MI_01\7&1E3640A&2&0001

    # find the Samsung device by vendor and product IDs
    dev = usb.core.find(idVendor=0x1fc9, idProduct=0x82b3)
    # print(dev)
    if dev is None:
        raise ValueError('Device not found')
    interface = dev.get_active_configuration().interfaces()[0]

    # Set the interface to be the active one
    print(interface)
    interface.set_altsetting()
    endpoint = interface.endpoints()[0]

    # read data from the endpoint
    while True:
        try:
            data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
            print(data)
        except usb.core.USBError as e:
            if e.args == ('Operation timed out',):
                continue


def pyqtserial():
    port = QtSerialPort.QSerialPortInfo.availablePorts()
    print(port)
    for ort in port:
        print(ort)


# seriyo()
# enableADB()
# pyusbports()
def spddiag():
    ports = serial.tools.list_ports
    prt = prtlist.comports()
    for port, desc, hwid in sorted(prt):
        dev = port
        print(desc)
        spddev = serial.Serial(port,baudrate=9600)
        print(spddev.readline())
        print(spddev.write(b'hello samung'))


#spddiag()
