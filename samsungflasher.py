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
    samstrt = await asyncio.create_subprocess_exec("daemon/sam.exe", '--reboot', stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE, startupinfo=startup_info)
    stdout, stderr = await samstrt.communicate()
    text = stdout.decode()
    return text


def read_output(stream, logfield, progress_bar):
    # if stream is type
    logfield.append(stream)
    print(stream)



def flashpart(part_file, logfield, progress_bar):
    progress_bar.setValue(0)
    progress_bar.setMaximum(100)
    cmd ='daemon\sam.exe'
    try:
        def read_stream(stream, logfield):
            for line in stream:
                logfield.append(line.strip())

        def samflashing(part_file, logfield, progress_bar):
            sampop = subprocess.Popen([cmd ,f' {part_file}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Start threads to read stdout and stderr concurrently
            stdout_thread = threading.Thread(target=read_stream, args=(sampop.stdout, logfield))
            stderr_thread = threading.Thread(target=read_stream, args=(sampop.stderr, logfield))

            stdout_thread.start()
            stderr_thread.start()

            # Wait for the process to complete and retrieve stdout and stderr
            stdout, stderr = sampop.communicate()

            # Wait for threads to complete
            stdout_thread.join()
            stderr_thread.join()

            # Optionally, you can append stdout and stderr to the logfield
            logfield.append(stdout.strip())
            logfield.append(stderr.strip())

        # Start the flashing thread
        samthread = threading.Thread(target=samflashing, args=(part_file, logfield, progress_bar))
        samthread.start()

        # Wait for the flashing thread to complete
        samthread.join()

        # Once the thread completes, update the logfield
        logfield.append('Flashing Samsung device completed')

    except Exception as xcv:
        print(f'The problem is: {xcv}')
        logfield.append(f'An Error occurred')
async def flash_parts(logfield, progresbar, *args):
    cmd = "daemon/sam.exe"
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    flasher = await subprocess.run([cmd, args], )
    """asyncio.create_subprocess_exec(("daemon/sam.exe"),*args,stderr=asyncio.subprocess.PIPE,
                                             stdout=asyncio.subprocess.PIPE)"""
    stdout_task = asyncio.create_task(read_output(flasher.stdout, logfield, progresbar))
    stderr_task = asyncio.create_task(read_output(flasher.stderr, logfield, progresbar))
    await asyncio.wait([stdout_task, stderr_task], return_when=asyncio.FIRST_COMPLETED)

    # await flasher.wait()
    await asyncio.gather(stderr_task, stdout_task)
    # flasher.terminate()


def pitanalyzer(pit):
    with open(pit, 'r') as p:
        cont = p.readlines()
        for li in cont:
            print(li)


def flashing_thread(*args):
    flash_preccess = subprocess.run(['daemon/sam.exe', *args])
    print(flash_preccess.stdout)
    print(flash_preccess.stderr)
# pitanalyzer('sample/orgnala03s.pit')
