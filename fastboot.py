import asyncio
import subprocess
import threading
import time

import usb



class Fboot:
    def __init__(self):
        self.fastb = None
        self.cmd = 'daemon/fastboot.exe'

    def fboot(self, cmd1, cmd2, cmd3):
        command = [self.cmd, cmd1, cmd2, cmd3]
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

    def fastbootinfo(self,logfield):
        fbb = Fboot()
        fbb.fboot('getvar','all','')
        result = fbb.get_output()
        logfield.setStyleSheet('color: green;'
                                         ' background-color: black;'
                                         'font-size: 8pt;'
                                         ' font-weight: bold; '
                                           )

        logfield.append(result)
    #after u create the async funtion then go ahead and create the runner
    """ def Fbootinfo(self,logfield):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.fastbootinfo(logfield))
            loop.close()"""
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
        batreaded=[]
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

                                batreaded.append(p)
        print(batreaded)
        return batreaded

    def bat_flasher(self,):
        pass
fbb = Fboot()

def usb_monitor(logfield):
        device = usb.core.find(idVendor=0x18d1, idProduct=0x4ee0)
        if device:
            #fastboot pids USB\VID_18D1&PID_4EE0&REV_0100
            #Found device: VID=0x18d1, PID=0x4ee0,Pixel 3,Google

            print('devcie found')

            if device is not None:
                # The device is connected, run the function
                fb = fbb.fastbootinfo(logfield)

            else:
                print('no fastboot device connected')
                devices = usb.core.find(find_all=True)

                if devices:
                    # Iterate over the devices and print their VID and PID
                    for device in devices:
                        print(f"Found device: VID={hex(device.idVendor)}, PID={hex(device.idProduct)},")
                # Wait for some time before checking again
            # Wait for some time before checking again
            time.sleep(2)
