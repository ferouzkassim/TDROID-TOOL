import asyncio
import subprocess
import threading
import time

import libusb1
import usb
import usb1


class Fboot:
    def __init__(self):
        self.fastb = None
        self.cmd = 'daemon/fastboot.exe'
        self.batreaded = []

    def fboot(self, cmd1, cmd2 ):
        command = [self.cmd, cmd1,cmd2]
        process = subprocess.run(command, capture_output=True)
        # Assign the output streams directly to self.fastb
        self.fastb = (process.stderr, process.stdout)

    def get_output(self):
        stdout_output, stderr_output = self.fastb
        decoded_line = ''
        if stdout_output:

            decoded_line += stdout_output.decode().replace('(bootloader)','')


        if stderr_output:
            decoded_line += stderr_output.decode().replace('(bootloader)','')

        return decoded_line

    async def fastbootinfo(self,logfield):
        fbb = Fboot()
        fbb.fboot('getvar','all',)
        result = fbb.get_output()
        logfield.setStyleSheet('color: green;'
                                         ' background-color: black;'
                                         'font-size: 8pt;'
                                         ' font-weight: bold; '
                                           )

        logfield.setText(result)
    #after u create the async funtion then go ahead and create the runner

        return result
    def bootloadr_unlocker(self,logfield):
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
            fbb.fboot('oem','unlock')
        logfield.append(result)
    def fbscripter(self, firmwarepath):

            matching_ext = None
            li_firmware_parsers = ['.bat', '.xml', '.cfg']
            print(firmwarepath)
    async def fastbut_flasher(self,flashcmd,logfield):
            fbb = Fboot()
            logfield.append('Waiting for fastboot arrival')
            await fbb.fboot(flashcmd,"","","")
            result = fbb.get_output()
            logfield.setStyleSheet('color: green;'
                                             ' background-color: black;'
                                             'font-size: 8pt;'
                                             ' font-weight: bold; '
                                             )
            logfield.append(result)

    def fastbut_flasher(self,file_ext):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                #loop.run_until_complete(self.ext_parser('.bat'))
                if self.ui.fbflash.text() == 'Flash .bat':
                    print('matching indoce founf')
                    parsing_Ext =self.ext_parser(self.fbscripter)

                else:
                    #loop.run_until_complete(self.fastbut_flasher('-h'))
                    #loop.close()
                    pass
    def ext_parser(self,ext):
        files_to_flash = []

        for i in ext:
            files_to_flash.append(i)
        for x in files_to_flash:
                print(x)
                if x.endswith(".bat") or x.endswith(".sh"):
                    print("bat file found")
                    with open(x,"r") as batopener:
                        line=batopener.readlines()
                        for p in line :
                            if p.startswith('fastboot'):
                                p.replace('fastboot','')
                                self.batreaded.append(p)
                        print(self.batreaded)
                        return self.batreaded

    def bat_flasher(self,):
        pass
fbb = Fboot()
#fbb.fastbootinfo()
def parse_usb_id(usb_id):
    vendor_id = int(usb_id.split("&")[0].split("_")[1],16)
    product_id = int(usb_id.split("&")[1].split("_")[1],16)
    revision = int(usb_id.split("&")[2].split("_")[1], 16)
    print(vendor_id,product_id)
    return vendor_id, product_id,revision
async def usb_monitor(func_to_run,logfield):
    # Define the USB device ID string
    usb_id_string = "USB\VID_18D1&PID_4EE0&REV_0100"
    # Convert the USB ID string to integer values
    vendor_id, product_id, revision = parse_usb_id(usb_id_string)
    vid=[0x18d1,]
    pid=[0x4ee0,0xd001]
    while True:
        # Check if the device with the specified vendor ID and product ID is connected
        device = usb.core.find(idVendor= 0x18d1, idProduct=0x4ee0)

        if device is not None:
            # The device is connected, run the function asynchronously
            await func_to_run
            break  # Exit the loop once the function is run
        else:
            # No fastboot device is connected
            logfield.setText('waiting for fastboot arrival')
            logfield.repaint()
            devices = usb.core.find(find_all=True)
            """for device in devices:
                print(f"Found device: VID={hex(device.idVendor)}, PID={hex(device.idProduct)}")
                print(device)"""
        # Wait for 2 seconds before checking again
        await asyncio.sleep(0.005)