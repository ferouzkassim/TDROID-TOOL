import asyncio
import os
import subprocess
import usb
import fastbootpy as fb

class fboot:
    def __init__(self):
        pass

    async def fboot(self):
        check_fb = await asyncio.create_subprocess_exec("daemon/fastboot.exe",'devices'
                                                        ,stdout=asyncio.subprocess.PIPE,
                                                       stderr=asyncio.subprocess.PIPE)
        output = await check_fb.stdout.read()
        print(output.decode())
        return output.decode()

fbb  = fboot()
asyncio.run(fbb.fboot())
