import asyncio
import os
import subprocess
import threading
import xml.etree.ElementTree as et
import concurrent.futures
import fastbootpy.usb_device
import usb
from PyQt6.QtCore import QThread, QEventLoop, QObject
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from usb.backend import libusb1
import fastbootpy as pyfb


class Fboot(QThread):
    def __init__(self,widget):
        self.fastb = None
        self.cmd = "daemon\\fastboot.exe"
        self.batreaded = []
        """self.part = part
        self.file = file"""
        self.widget = widget
    def setfile(self,file,part):
        self.file = file
        self.part = part

    def fboot(self, cmd1, cmd2):
        command = [self.cmd, cmd1, cmd2]
        process = subprocess.run(command, capture_output=True)
        # Assign the output streams directly to self.fastb
        self.fastb = (process.stderr, process.stdout)

    def get_output(self):
        stdout_output, stderr_output = self.fastb
        decoded_line = ''
        if stdout_output:
            decoded_line += stdout_output.decode().replace('(bootloader)', '')

        if stderr_output:
            decoded_line += stderr_output.decode().replace('(bootloader)', '')

        return decoded_line

    async def fastbootinfo(self, logfield, ):
        fbb = Fboot()
        fbb.fboot('getvar', 'all', )
        result = fbb.get_output()
        logfield.setStyleSheet('color: green;'
                               ' background-color: black;'
                               'font-size: 8pt;'
                               ' font-weight: bold; '
                               )

        logfield.setText(result)
        # after u create the async funtion then go ahead and create the runner

        return result

    def bootloadr_unlocker(self, logfield):
        fbb = Fboot()
        try:
            fbb.fboot('flashing', 'unlock')
            result = fbb.get_output()
            logfield.setStyleSheet('color: green;'
                                   ' background-color: black;'
                                   'font-size: 8pt;'
                                   ' font-weight: bold; '
                                   )



        finally:
            fbb.fboot('oem', 'unlock')
        logfield.append(result)

    def fbscripter(self, firmwarepath):

        matching_ext = None
        li_firmware_parsers = ['.bat', '.xml', '.cfg', '.sh']
        print(firmwarepath)

    def batfile(self, part, file, widget):
        fastbootpy.FastbootDevice.flash(self, part)

    def fbloger(self, st_out, widget):
        widget.append(st_out.readline())
        print(f'the stout is {st_out}')

    async def fbtflasher(self, part, file, widget):
        try:
            # with disabled popups
            tflasher = await asyncio.create_subprocess_shell(
                f'{self.cmd} flash {part} {file}',
                stderr=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE
            )
            stdout_reader = asyncio.create_task(self.read_stream(tflasher.stdout, widget))
            await stdout_reader, tflasher.wait()

        except Exception as e:
            # Handle any exceptions that might occur during the subprocess execution
            widget.append(f"An error occurred: {str(e)}")

    async def read_stream(self, strem, widget):
        while True:
            line = await strem.readline()
            if not line:
                break
            decoded_line = line.decode('utf-8')
            widget.append(decoded_line)

def xmlreader( file, widget):
    flashing_dict = {}
    tree = et.parse(file)

    try:
        for partition_index in tree.findall('partition_index'):
            partition_name = partition_index.find('partition_name').text
            file_name = partition_index.find('file_name').text
            partition_size = partition_index.find('partition_size').text
            storage = partition_index.find('storage').text
            is_download = partition_index.find('is_download').text

            if file_name != 'NONE' and is_download == 'true':
                widget.append(f'file_name : {file_name}')
                flashing_dict[partition_name] = file_name
                widget.append(f"Partition Size: {partition_size}")
                widget.append(f"Partition Name: {partition_name}")
                widget.append("_" * 15)
    except Exception as e:
        # Handle specific exceptions, log the error, and decide on appropriate actions
        widget.append(f"Error parsing partition_index: {e}")

    try:
        for stor in tree.findall('.//storage_type'):

            partition_name = stor.findall('partition_name').text
            file_name = stor.findall('file_name').text
            partition_size = stor.findall('partition_size').text
            storage = stor.findall('storage').text
            is_download = stor.findall('is_download').text

            if file_name != 'NONE' and is_download == 'true':
                widget.append(f'file_name : {file_name}')
                flashing_dict[partition_name] = file_name
                widget.append(f"Partition Size: {partition_size}")
                widget.append(f"Partition Name: {partition_name}")
                widget.append("_" * 15)
    except:
        # Exception as :
        # Handle specific exceptions, log the error, and decide on appropriate actions
        # widget.append(f"Error parsing storage_type: {e}")
        print('e.args')
    return flashing_dict

def ext_parser(ext, widget):
    files_to_flash = []
    for i in ext:
        files_to_flash.append(i)
    for x in files_to_flash:
        if x.endswith(".bat") or x.endswith(".sh") or x.endswith('.tfb') or x.endswith('.txt'):
            with open(x, "r") as batopener:
                line = batopener.readlines()
                for p in line:
                    if p.startswith('tf'):
                        p.replace('tf', '')
                        self.batreaded.append(p)
                    if p.startswith('fastboot'):
                        p.replace('fastboot', ''
                                  )
                        self.batreaded.append(p)

                return self.batreaded
        elif x.endswith(".xml"):
            flashdict = xmlreader(x, widget)
            return flashdict
    return files_to_flash




# fbb.fastbootinfo()
def parse_usb_id(usb_id):
    vendor_id = int(usb_id.split("&")[0].split("_")[1], 16)
    product_id = int(usb_id.split("&")[1].split("_")[1], 16)
    revision = int(usb_id.split("&")[2].split("_")[1], 16)
    print(vendor_id, product_id)
    return vendor_id, product_id, revision


async def usb_monitor(func_to_run):
    # Define the USB device ID string
    usb_id_string = r"USB\VID_18D1&PID_4EE0&REV_0100"
    # USB\VID_0E8D&PID_201C&REV_0100
    # USB\VID_18D1&PID_D00D
    # USB\VID_0E8D&PID_201C
    # USB\VID_18D1&PID_4EE0&REV_0100
    # USB\VID_18D1&PID_4EE0
    # Convert the USB ID string to integer values
    # libusb install filer
    # install-filter install "--device=USB\VID_18D1&PID_4EE0&REV_0100"
    vendor_id, product_id, revision = parse_usb_id(usb_id_string)
    vid = [0x18d1, 0x0E8D]
    pid = [0x4ee0, 0xd001, 0x201C]
    bckedn = libusb1.get_backend()
    for i in fastbootpy.FastbootManager.devices():
        print(i)
    while True:
        # Check if the device with the specified vendor ID and product ID is connected
        devices = fastbootpy.FastbootManager.devices()
        device = usb.core.find(idVendor=0x18D1, idProduct=0X4EE0, backend=bckedn)
        if devices is not None:
            # The device is connected, run the function asynchronously
            await func_to_run
            break  # Exit the loop once the function is run
        else:
            # No fastboot device is connected
            print('no libusb found')

            for i in range(1, 101):
                await asyncio.sleep(0.00025)

            command = ['daemon/usbif.exe', f'install', f'--device={usb_id_string}']
            lbusb = subprocess.run(command, capture_output=True)

            # Print the output of the subprocess.
            print(lbusb.stdout)

            devic = usb.core.find(find_all=True)
            break
        # Wait for 2 seconds before checking again
        await asyncio.sleep(0.005)
