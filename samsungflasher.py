import os
import subprocess
import threading
from queue import Queue
import asyncio
import serial
import serial.tools.list_ports as liport
import asyncio
import subprocess

async def readpit():
    samstrt = await asyncio.create_subprocess_exec("daemon/sam.exe",'--reboot',stdout=asyncio.subprocess.PIPE,
                                                    stderr =asyncio.subprocess.PIPE)
    stdout, stderr = await samstrt.communicate()
    text = stdout.decode()
    return text
def flashpart(part,file):
    cmd = "daemon/sam.exe"
    process = subprocess.Popen([cmd, part, file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(f'starting {cmd}{part}{file}')
    print(os.curdir)
    for line in process.stdout:
        text = line.decode()
        print(text)

        #logfield.insertPlainText(text)

    process.communicate()
    #print(process.stdin)
def pitanalyzer(pit):
    with open(pit,'r')as p:
        cont = p.readlines()
        for li in cont:
            print(li)
#pitanalyzer('sample/orgnala03s.pit')
def samsung_protocol():
    for ser in liport.comports():
        pid=ser.pid
        print(hex(ser.pid))
        print(hex(pid))
        print(hex(ser.vid))
        if ser.vid==hex(1256):
            print(ser)
#samsung_protocol()