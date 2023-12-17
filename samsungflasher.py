import ast
import asyncio
import numbers
import os
import pathlib
import re
import subprocess
import threading
from pathlib import Path
from PyQt6.QtCore import QThread, QEventLoop, QObject
from PyQt6.QtCore import pyqtSignal,pyqtSlot


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


main_loop = asyncio.get_event_loop()
class SamsungFlasherThread(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    def __init__(self, lf, pbar):
        super().__init__()
        self.lf = lf  # logfield
        #self.part_file = prt  # part file and file
        self.pbar = pbar  # progress bar

    def set_part_file(self, part_file):
        self.part_file = part_file
    def run(self):
        asyncio.run(self.samflashing())
    async def read_stream(self, stream):
        while True:
            line = await stream.readuntil(b'\n')  # Read until a newline character is encountered
            if not line:
                break
            self.process_output(line)

    def process_output(self, line):
        print(line)
        try:
            decoded_line = line.decode().strip()

            if decoded_line.startswith('('):
                # Lines starting with '(' are printed
                print(f'the {decoded_line}')
            elif decoded_line.endswith('%)'):
                # Lines ending with '%)' are progress values
                progress_value = int(decoded_line.split('(')[-1].split('%)')[0])
                self.progress_signal.emit(progress_value)
                print(f'fuohlk{decoded_line}')
            elif 'cannot find device' in decoded_line.lower():
                # Lines containing 'cannot find device' are handled separately
                self.log_signal.emit(decoded_line)
            else:
                # All other lines are emitted as logs
                print('mhkgj')
                self.log_signal.emit(decoded_line)
        except ValueError as e:
            print(f"Error decoding line: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    async def samflashing(self):
        try:
            samflasher = await asyncio.create_subprocess_shell(
                f'daemon\\sam.exe --ignore-md5 {self.part_file}',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout_reader = asyncio.create_task(self.read_stream(samflasher.stdout))
            #stderr_reader = asyncio.create_task(self.read_stream(samflasher.stderr))

            await samflasher.wait()

            # Ensure that the output readers have finished
            await asyncio.gather(stdout_reader)
            self.log_signal.emit('Flashing Samsung device completed')
        except Exception as e:
            print(e)
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
