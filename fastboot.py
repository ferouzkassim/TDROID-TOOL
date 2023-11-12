import asyncio
import os
import subprocess
import threading
import xml.etree.ElementTree as et

import fastbootpy.usb_device
import usb
from PyQt6.QtWidgets import QApplication
from usb.backend import libusb1
import fastbootpy as pyfb


'''class fbpy:
    def __int__(self):
        pass

    def info(self):
        dev = pyfb.FastbootManager.devices()
        print('logginh')
        print(dev)
        for i in dev:
            print(i)
            
            pyfb.FastbootDevice.getvar(i,'all')


fb = fbpy()
fb.info()
'''

class Fboot:
    def __init__(self):
        self.fastb = None
        self.cmd = "daemon/fastboot.exe"
        self.batreaded = []

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

    async def fastbootinfo(self, logfield):
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

    def batfile(self,part,file,widget):
        fastbootpy.FastbootDevice.flash(self,part)
    async def fbloger(self, stream,widget):
        lines = stream.splitlines()
        for line in lines:
            # Process each line as it arrives
            await asyncio.sleep(0)  # Allow other tasks to run concurrently
            widget.append(line.replace('(bootloader)', '->'))
            # the missing glotch in realtime processing is QApplication.processEvents()
            QApplication.processEvents()

    async def fbtflasher(self, part,file,widget):
        #with disabled popus

        tflasher = await asyncio.to_thread(subprocess.run, [self.cmd, 'flash', part, file],
                                           stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                           creationflags=subprocess.CREATE_NO_WINDOW)

        td = tflasher.stderr.decode()
        await self.fbloger(td, widget)
        """tflasher = await asyncio.create_subprocess_exec(self.cmd, 'flash',part,file,
                                                        stderr=asyncio.subprocess.PIPE,
                                                        stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await tflasher.communicate()
        td = stderr.decode()
        stdout_task = asyncio.create_task(self.fbloger(td,widget))
        await stdout_task"""
       # await asyncio.wait([stdout_task, ], return_when=asyncio.FIRST_COMPLETED)


    def xmlreader(self,file,widget):
        flashingDict = {}
        fileparse = et.parse(file)
        for partition_index in fileparse.findall('partition_index'):
            partition_name = partition_index.find('partition_name').text
            file_name = partition_index.find('file_name').text
            partition_size = partition_index.find('partition_size').text
            storage = partition_index.find('storage').text
            isdownload = partition_index.find('is_download').text
            if file_name != 'NONE' and isdownload =='true' :
                widget.append(f'file_name : {file_name}')
                flashingDict[partition_name] = f'{file_name}'
                widget.append(f"Partition Size: {partition_size}")
                widget.append(f"Partition Name: {partition_name}")
                widget.append("_" * 15)
        return flashingDict
    def ext_parser(self, ext,widget):
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
                flashdict =self.xmlreader(x,widget)
                return flashdict
        return files_to_flash



fbb = Fboot()


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
    #USB\VID_18D1&PID_4EE0
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
