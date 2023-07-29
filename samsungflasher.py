import asyncio
import io
import subprocess


async def readpit():
    samstrt = await asyncio.create_subprocess_exec("daemon/sam.exe",'--reboot',stdout=asyncio.subprocess.PIPE,
                                                    stderr =asyncio.subprocess.PIPE)
    stdout, stderr = await samstrt.communicate()
    text = stdout.decode()
    return text
async def flashpart(part,file,logfield):
    def process_line(line):
        decoded_line = line
        logfield.append(decoded_line)

    cmd = "daemon/sam.exe"
    process = await asyncio.create_subprocess_exec(cmd,part,file,
                stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
    await process.communicate()
    samlog = await process.stderr.read()
    print(samlog)
    """ t2 = await asyncio.StreamReader.read(process.stderr)
    print(t2)
    logfield.append(t2.decode())
"""

def pitanalyzer(pit):
    with open(pit,'r')as p:
        cont = p.readlines()
        for li in cont:
            print(li)
#pitanalyzer('sample/orgnala03s.pit')
