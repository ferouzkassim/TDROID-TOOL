from adb_shell.adb_device import AdbDeviceTcp

# Connect to the device
device = AdbDeviceTcp('127.0.0.1' ,5037)
device.connect()

# Start the ADB server
#device.start_server()
device.reboot()
# Get a shell object
shell = device.shell("")
