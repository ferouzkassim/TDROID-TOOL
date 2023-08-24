import asyncio
import subprocess
import threading
import usb
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

    def batfile(self):
        flashing_threads = []
        for i in self.batreaded:
            flashing_threads.append(i.replace('fastboot', ''))
        for p in flashing_threads:
            str(p)
            pthread = threading.Thread(target=fbb.fboot, args=())
            # pthread.start()

    async def fbloger(self, stream,widget):
        print(f'the streams is{stream}')
        widget.append(stream.replace('(bootloader)','->'))

    async def fbtflasher(self, part,file,widget):
        tflasher = await asyncio.create_subprocess_exec(self.cmd, 'flash',part,file,
                                                        stderr=asyncio.subprocess.PIPE,
                                                        stdout=asyncio.subprocess.PIPE)
        stdout, stderr = await tflasher.communicate()
        td = stderr.decode()
        stdout_task = asyncio.create_task(self.fbloger(td,widget))

        await asyncio.wait([stdout_task, ], return_when=asyncio.FIRST_COMPLETED)

    def ext_parser(self, ext):
        files_to_flash = []
        for i in ext:
            files_to_flash.append(i)
        for x in files_to_flash:
            print(x)
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

    # Convert the USB ID string to integer values
    # libusb install filer
    # install-filter install "--device=USB\VID_18D1&PID_4EE0&REV_0100"
    vendor_id, product_id, revision = parse_usb_id(usb_id_string)
    vid = [0x18d1, 0x0E8D]
    pid = [0x4ee0, 0xd001, 0x201C]
    bckedn = libusb1.get_backend()
    while True:
        # Check if the device with the specified vendor ID and product ID is connected
        device = usb.core.find(idVendor=0x18D1, idProduct=0X4EE0, backend=bckedn)
        if device is not None:
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

            devices = usb.core.find(find_all=True)
            """for device in devices:
                print(f"Found device: VID={hex(device.idVendor)}, PID={hex(device.idProduct)}")
                print(device)"""
            break
        # Wait for 2 seconds before checking again
        await asyncio.sleep(0.005)
