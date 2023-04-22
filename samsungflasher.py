import subprocess
import serial
import serial.tools.list_ports as liport
def flasher(part,file):
    com=subprocess.run(['daemon/sam.exe','-l'])
    bl = subprocess.run(['daemon/sam.exe',f'-{part}',file])
    logg = bl.stdout
    print(logg)
    return logg
'''flasher(part='b',file='C:\\Users'
                      '\\DROID\\Desktop\\'
                      'A135F\\A136F OFFICIA\\U1 A135F\\'
                      'BL_A135FXXU1AVB5_CL23696854_QB49342530_REV00_user_low_ship_MULTI_CERT.tar.md5')'''

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


samsung_protocol()