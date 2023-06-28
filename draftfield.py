import serial.tools.list_ports
def portlister():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        print(p.pid)
        print(p.hwid)
        #USB VID:PID=04E8:685D


portlister()