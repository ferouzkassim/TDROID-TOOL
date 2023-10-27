import ast
import asyncio
import numbers
import re
import subprocess
import threading
from pathlib import Path
import ctypes
def file_areng():
    pass
async def readpit():
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    samstrt = await asyncio.create_subprocess_exec("daemon/sam.exe",'--reboot',stdout=asyncio.subprocess.PIPE,
                                                    stderr =asyncio.subprocess.PIPE,startupinfo=startup_info)
    stdout, stderr = await samstrt.communicate()
    text = stdout.decode()
    return text
async def read_output(stream, logfield, progress_bar):
    while True:
        line = await stream.readline()
        if not line:
            break
        log = line.decode().strip()
        try:
            log_as_int = int(log)
            if 0 <= log_as_int <= 100:
                progress_bar.setValue(log_as_int)
            else:
                logfield.append(log)
        except ValueError:
            logfield.append(log)



async def flashpart(part, file, logfield,progress_bar):
    cmd = "daemon/sam"
    progress_bar.setValue=0
    progress_bar.setMaximum=100
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = await asyncio.create_subprocess_exec(
        cmd,'--ignore-md5', part, file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,startupinfo=startup_info
    )

    stdout_task = asyncio.create_task(read_output(process.stdout, logfield,progress_bar))
    stderr_task = asyncio.create_task(read_output(process.stderr, logfield,progress_bar))

    await asyncio.wait([stdout_task,stderr_task ], return_when=asyncio.FIRST_COMPLETED)

    process.terminate()
    await process.wait()

    await asyncio.gather(stdout_task,stderr_task)
async def run_flashpart(part, file, logfield,pbar):
    await flashpart(part, file, logfield,pbar)

async def flash_parts(logfield,progresbar,*args):
    cmd = Path("daemon/sam.exe")
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    flasher = await subprocess.run([cmd,args],)
    """asyncio.create_subprocess_exec(("daemon/sam.exe"),*args,stderr=asyncio.subprocess.PIPE,
                                             stdout=asyncio.subprocess.PIPE)"""
    stdout_task = asyncio.create_task(read_output(flasher.stdout, logfield,progresbar))
    stderr_task = asyncio.create_task(read_output(flasher.stderr, logfield,progresbar))
    await asyncio.wait([stdout_task,stderr_task ], return_when=asyncio.FIRST_COMPLETED)


    #await flasher.wait()
    await asyncio.gather(stderr_task,stdout_task)
    #flasher.terminate()

def pitanalyzer(pit):
    with open(pit,'r')as p:
        cont = p.readlines()
        for li in cont:
            print(li)
def flashing_thread(*args):
    flash_preccess = subprocess.run(['daemon/sam.exe',*args])
    print(flash_preccess.stdout)
    print(flash_preccess.stderr)
#pitanalyzer('sample/orgnala03s.pit')
