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
        if isinstance(line, int):
            self.progress_signal.emit(line)
        else:
            decoded_line = line.decode()
            if decoded_line.endswith('%') and decoded_line[:-1].isdigit():
                progress_value = int(decoded_line[:-1])
                print(progress_value)
                self.progress_signal.emit(decoded_line)
            else:
                self.log_signal.emit(decoded_line)
                print(decoded_line, end='')

    async def samflashing(self):
        try:
            samflasher = await asyncio.create_subprocess_shell(
                f'daemon\\sam.exe --ignore-md5 {self.part_file}',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout_reader = asyncio.create_task(self.read_stream(samflasher.stdout))
            stderr_reader = asyncio.create_task(self.read_stream(samflasher.stderr))

            await samflasher.wait()

            # Ensure that the output readers have finished
            await asyncio.gather(stdout_reader, stderr_reader)
            self.log_signal.emit('Flashing Samsung device completed')
        except Exception as e:
            print(e)

    @pyqtSlot(int)
    def updateProgressBar(self, value):
        self.pbar.setValue(value)


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
