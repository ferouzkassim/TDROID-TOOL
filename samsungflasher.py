import subprocess
import threading
from queue import Queue

import serial
import serial.tools.list_ports as liport
def flasher(part, file,output_queue):
    """
    Flashes a device with the given partition and file.

    Args:
        part (str): The partition to flash.
        file (str): The file to flash.

    Returns:
        str: The output of the flash operation.
    """
    outpt = ""

    # Check if the daemon is running.
    com = subprocess.run(["daemon/sam.exe", "-l"])
    if com.returncode != 0:
        print("Error: The daemon is not running.")
        return None

    # Flash the device.
    par = subprocess.run(["daemon/sam.exe", f"{part}", file],
                         universal_newlines=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if par.returncode != 0:
        print("Error: The flash operation failed.")
        return None

    # Iterate over output lines.
    output_lines = par.stdout
    outpt = par.stdout.strip() + par.stderr.strip()

    #print(output_lines)
    #print(outpt)

    output_queue.put(outpt)
    #return outpt

def run_flasher(part,file):
    output_queue = Queue()
    thread = threading.Thread(target=flasher, args=(part, file,output_queue))
    thread.start()
    thread.join()
    flasher_output = output_queue.get()
    return flasher_output

#run_flasher(part='b',file='C:\\Users\\DROID\\Desktop\\A125F U2\\offici\\BL_A125FXXS2BVA3_CL22457755_QB48025674_REV00_user_low_ship_MULTI_CERT.tar.md5')

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