import ast
import asyncio
import numbers
import os
import pathlib
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
    #if stream is type
    logfield.append(stream)
    print(stream)


cmd = "daemon/sam.exe"
async def flashpart(part, file, logfield,progress_bar):
    progress_bar.setValue=0
    progress_bar.setMaximum=100
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        proces = await asyncio.to_thread(subprocess.run,[cmd,part,file,'--ignore-md5'],
                                         stderr= subprocess.PIPE,
                                         stdout = subprocess.PIPE,
                                         creationflags =subprocess.CREATE_NO_WINDOW)


        await read_output(proces.stdout.decode(),logfield,progress_bar)
        #await read_output(proces.stdout,logfield,progress_bar)
    except Exception as xcv:
        print(f'the problem is f {xcv}')
        logfield.append(f'An Error occurred Check File Paths or {xcv}')


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
