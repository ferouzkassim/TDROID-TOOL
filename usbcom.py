import usb.core
import serial.tools.list_ports as prtlist
import usb.util
from typing import List
import serial
import serial.tools.list_ports as prtlst
from serial.tools import list_ports_common
import time
#borrowing from https://github.com/FICS/atcmd
#borrowing also from https://github.com/riskeco/Samsung-FRP-Bypass
#define SAMSUNG_VENDOR_ID  	0x04e8
#define SAMSUNG_PRODUCT_ID 	0x6860
# Find the Samsung device in download mode
dev = usb.core.find(idVendor=0x04e8, idProduct=0x685d)
SERIAL_PORT = "/dev/ttyACM0"
GALAXY_ID_VENDOR = 0x04e8
GALAXY_ID_PRODUCT = 0x6860
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
#enable adb from atcommands using this functions

SERIAL_BAUDRATE = 115200
SERIAL_TIMEOUT = 12

def list_serial_ports() -> list_ports_common.ListPortInfo:
    ports = prtlst.comports()
    if len(ports) == 0:
        print("No serial port available")
        exit(1)
    print("####### Available serial ports #######")
    for port, desc, hwid in sorted(ports):
        print(port, desc, hwid)
    for port in ports:
        print(port)
    print("####### End of available serial ports #######")
    return ports[0]

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
    default_port = list_serial_ports()
    port = input(f"Choose a serial port (default={default_port.device}) :") or str(default_port.device)
    io = get_AT_serial(port)
    print("Initial...")
    # Seems to check if we are in *#0*# mode but apparently not working on the samsung I have
    ATSend(io, "AT+KSTRINGB=0,3\r\n")
    print("Go to emergency dialer and enter *#0*#, press enter when done")
    input()

    print("Enabling USB Debugging...")
    cmds = []
    cmds.append("AT+DUMPCTRL=1,0\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")
    cmds.append("AT+SWATD=0\r\n")
    cmds.append("AT+ACTIVATE=0,0,0\r\n")
    cmds.append("AT+SWATD=1\r\n")
    cmds.append("AT+DEBUGLVC=0,5\r\n")
    tryATCmds(io, cmds)

    print("USB Debugging should be enabled")
    print("If USB Debugging prompt does not appear, try unplug/replug the USB cable")
enableADB()
list_serial_ports()