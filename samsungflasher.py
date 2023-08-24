import asyncio
import numbers


async def readpit():
    samstrt = await asyncio.create_subprocess_exec("daemon/sam.exe",'--reboot',stdout=asyncio.subprocess.PIPE,
                                                    stderr =asyncio.subprocess.PIPE)
    stdout, stderr = await samstrt.communicate()
    text = stdout.decode()
    return text
async def read_output(stream, logfield,progress_bar):
    while True:
        line = await stream.readline()
        if not line:
            break
        log = line.decode().strip()
        if log is type(numbers):
            progress_bar.setValue(log)
        else:
            logfield.append(log)


async def flashpart(part, file, logfield,progress_bar):
    cmd = "daemon/sam.exe"
    progress_bar.setValue=0
    progress_bar.setMaximum=100

    process = await asyncio.create_subprocess_exec(
        cmd, part, file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout_task = asyncio.create_task(read_output(process.stdout, logfield,progress_bar))
    stderr_task = asyncio.create_task(read_output(process.stderr, logfield,progress_bar))

    await asyncio.wait([stdout_task, ], return_when=asyncio.FIRST_COMPLETED)

    process.terminate()
    await process.wait()

    await asyncio.gather(stdout_task,stderr_task)
async def run_flashpart(part, file, logfield,pbar):
    await flashpart(part, file, logfield,pbar)

async def flash_parts(cmd2,logfield):
    cmd = "daemon/sam.exe"
    flasher = await asyncio.create_subprocess_exec(cmd,cmd2,stderr=asyncio.subprocess.PIPE,
                                             stdout=asyncio.subprocess.PIPE)
    stdout_task = asyncio.create_task(read_output(flasher.stdout, logfield))
    stderr_task = asyncio.create_task(read_output(flasher.stderr, logfield))

    await asyncio.wait([stdout_task, ], return_when=asyncio.FIRST_COMPLETED)

    flasher.terminate()
    await flasher.wait()
    await asyncio.gather(stderr_task,stdout_task)

def pitanalyzer(pit):
    with open(pit,'r')as p:
        cont = p.readlines()
        for li in cont:
            print(li)
#pitanalyzer('sample/orgnala03s.pit')
