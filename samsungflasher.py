import asyncio
async def readpit():
    samstrt = await asyncio.create_subprocess_exec("daemon/sam.exe",'--reboot',stdout=asyncio.subprocess.PIPE,
                                                    stderr =asyncio.subprocess.PIPE)
    stdout, stderr = await samstrt.communicate()
    text = stdout.decode()
    return text
async def read_output(stream, logfield):
    while True:
        line = await stream.readline()
        if not line:
            break
        logfield.append(line.decode().strip())

async def flashpart(part, file, logfield):
    cmd = "daemon/sam.exe"
    process = await asyncio.create_subprocess_exec(
        cmd, part, file,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout_task = asyncio.create_task(read_output(process.stdout, logfield))
    stderr_task = asyncio.create_task(read_output(process.stderr, logfield))

    await asyncio.wait([stdout_task, ], return_when=asyncio.FIRST_COMPLETED)

    process.terminate()
    await process.wait()

    await asyncio.gather(stdout_task,stderr_task)
async def run_flashpart(part, file, logfield):
    await flashpart(part, file, logfield)



def pitanalyzer(pit):
    with open(pit,'r')as p:
        cont = p.readlines()
        for li in cont:
            print(li)
#pitanalyzer('sample/orgnala03s.pit')
