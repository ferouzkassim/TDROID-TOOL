import subprocess
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