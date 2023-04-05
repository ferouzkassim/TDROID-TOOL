import os
import subprocess
import shutil as shtl
import tkinter
import asyncio
import threading
from tkinter import END
import py7zr
from py7zr import py7zr as pyz
import pathlib as pth
from adbcon import startDaemon, host, port, client, stopDaemon
#py7zr a module to use for compressing snd decompressing with password
#importing the class to do detecting and exposing the srial number
def adbConnect():
    print('starting dameon')
    startDaemon()
    prop = []
    resultprop = {}
    filteredprops={}
    #the filtered keys to look for in prop
    filter_keys = [

        'ro.product.model',
        'ro.product.name',
        'ro.build.id',
        'ro.product.product.model',
        'ro.build.product',
        'ro.build.version.release',
        'ro.build.version.security_patch',
        'ro.build.PDA',
        'ro.carrier',
        'ro.config.knox',
        'ro.csc.country_code',
        'ro.frp.pst',
        'ro.hardware.chipname',
        'ro.serialno',
        'sys.usb.config',
        'Build.BRAND',
        'gsm.version.baseband',
        'knox.kg.state',
        'ril.modem.board',
        'gsm.network.type',
        'gsm.operator.iso-country',
        'gsm.version.baseband',
        'gsm.operator.alpha',
        'gsm.operator.iso-country',

    ]
    devices = client.devices()
    output = ''
    for dev in devices:
        # This will allow the GUI to update while the function is running
        if dev.serial is None:
            # This will allow the GUI to update while the function is running
            asyncio.sleep(0)
            output += 'No Device Found\n'
        else:
            propstr = dev.shell('getprop')
            prop.append(propstr.split('\n'))
            for sublist in prop:
                for stringprop in sublist:
                    clean_string = stringprop.strip().replace("[", "").replace("]", "")
                    if clean_string and ':' in clean_string:
                        key, value = clean_string.split(': ')
                        resultprop[key] = value
                        if key in filter_keys:
                            filteredprops[key] = value
                output += f"{dev.serial}\n"
                for prop, answer in filteredprops.items():
                    output += f"{prop} = {answer}\n\n"
        print(output)

    return output


#first things frst start the server then get devices
#then enumrate to get index and enumerate to get the respondent app
#apend it to a blank list the return the listy with the index and app appnended to it
class detect:
    def __init__(self,dev):
        self.dev =dev

    def applister(self):

        applist = []
        if client.devices():

         for dev in client.devices():
            dev.get_state()
            for appindex,app in enumerate(dev.list_packages()):
              applist.append(f'{appindex}: -> {app}')

#rto ad a new line on each app and index

        else:
         applist.append('No Device Found')
        return '\n'.join(applist)


    def searcher(self,holder):
        self.holder = holder
        search = tkinter.Entry(holder)

        search.place(relx=1.0,rely=0,anchor=tkinter.NE,width=300)
def rootfs():
    device =startDaemon()
    locations = 'dev/block/platform'
    for dev in client.devices():
        if dev.serial == device:
            # su - c breaks out of the su waiting time and lets you execute once
            devloc = dev.shell(f'su -c cd {locations}/')

            # response = dev.shell(f'su -c "dd if=/{locations}'

            ls_output = dev.shell(f'su -c ls {locations}/')
            partition_path = f'/{locations}/{ls_output.strip().split()[-1]}/by-name/'
            print(partition_path)
            return  partition_path
class BackUP(detect):
    def __init__(self, pclocation,Part_name,devlocation):
        super().__init__()
        startDaemon()
        self.devloaction = devlocation
        self.pclocation = pclocation
        self.Part_name = Part_name
        files_to_zip = []
        backup_files = []
# a function that is gonna find the rootfs of the device and return t
    #the location so taht any part can be backed up regardless of the chip or device

    def PartBackup(self, pclocation, part_name,):
            response = ''
            device = startDaemon()
            backup_files = []
            locations = 'dev/block/platform'
            for dev in client.devices():
                board_make = dev.shell('getprop Build.BRAND').strip()
                if dev.serial == device:
                    # su - c breaks out of the su waiting time and lets you execute once
                    response += f'\ndevice found is {board_make}\n'
                    # response = dev.shell(f'su -c "dd if=/{locations}'
                    # f'/bootdevice/by-name/efs of=/sdcard/efs.tdf"')'''
                    pcdir, pcfile = os.path.split(pclocation)
                    if board_make == 'MTK':
                        dev.shell(f'su -c mkdir /storage/emulated/0/td/')
                        for part in part_name:
                            backup_command = f'su -c "dd if={rootfs()}/{part} of=/storage/emulated/0/td/{part}.tdf"'
                            bckup = dev.shell(backup_command)
                            backup_files.append(f'/storage/emulated/0/td/{part}.tdf')
                        dev.shell('cd /storage/emulated/0/td')
                    else:
                        dev.shell(f'su -c mkdir /storage/emulated/0/td')
                        new_pclocation = os.path.join(pcdir, dev.serial)
                        otherfiles = []
                        for par in part_name:
                            backup_command = f'su -c dd if=/{rootfs()}/{par} of=/storage/emulated/0/td/{par}.tdf'
                            new_pclocation = os.path.join(pcdir, pcfile)
                            dev.shell(backup_command)
                            locate = f'/storage/emulated/0/td/{par}.tdf'
                            otherfiles.append(locate)
                            print(otherfiles)
                        for loc in otherfiles:
                            pcfile = f"{loc.split('/')[-1][:-4]}_{dev.serial}"
                            new_pclocation = os.path.join(pcdir,pcfile)
                            print(new_pclocation)
                            print(pcfile)
                            dev.pull(loc,new_pclocation)
                        print(locate)
                        #dev.pull(src=f'/storage/emulated/0/td/{part}.tdf', dest=new_pclocation)
                        os.chdir(pcdir)
                        response += f'\n {part_name} back up saved as' \
                            # Do backup here
                    #sybcing to pc location
                    #dev.pull(src=part_name_backup, dest=f'{pclocation}')
                    #print(dev.shell(f'su -c cd /{locations}'))
                    #bckup = dev.shell((f'su -c "dd if=/{locations}/{ls_output}by-name/efs" of=/storage/emulated/0/{part_name}.tdf'))
                    # Do backup here
                    #print(ls_output)
                    #print(bckup)
                    response +=f'\n using {board_make} spring board'\
                                f' \n working from {pclocation}' \
                               f'\n compressing as {pclocation}_{dev.serial}'
                    response
                    print(pcdir)
                return response,backup_files

    def puller(self, backup_files, pclocation):
        response = ''
        for part in backup_files:
            for dev in client.devices():
                # print(part)
                # Get the directory and filename components of pclocation
                pcdir, pcfile = os.path.split(pclocation)
                # Insert the partition name into the filename component
                pcfile = f"{part.split('/')[-1][:-4]}_{dev.serial}"
                # Rejoin the directory and modified filename components
                new_pclocation = os.path.join(pcdir, pcfile)
                # Pull the file from the device to the modified pclocation
                dev.pull(src=part, dest=new_pclocation)
                # print(directory)            #with py7zr.SevenZipFile(f'{pclocation}.7z', mode='w') as archname:
            response += f' \n{pcfile} \t'
            return response

    def zipper(self, pclocation):
        files_to_zip = []

        responce = ''
        pcdir, pcfilr = os.path.split(pclocation)
        print(pcdir, pcfilr)
        for dev in client.devices():
            for file in os.listdir(pcdir):
                files_to_zip.append(file)
                # print(files_to_zip)
                file_ch = [f for f in files_to_zip if f.endswith(f"{dev.serial}")]
                print(file_ch)
                os.chdir(pcdir)
                if not os.path.exists(f'{dev.serial}'):
                    os.mkdir(f'{dev.serial}')
                for f in file_ch:
                    print(f)
                    shtl.move(src=(os.path.join(pcdir, f))
                              , dst=f'{dev.serial}')
                    print('moving')
                    shtl.make_archive(f'{pclocation}_{dev.serial}', 'tar', root_dir=f'{pcdir}\\{dev.serial}')
                    shtl.rmtree(f'{dev.serial}', True)
                    responce += f'\n compressing as {pclocation}_{dev.serial}' \
                                f'\n files saved to archive and ready for further use '

                    break
                else:
                    response = 'device not found'
                return response


    def part_restore(self,pclocation,partname):
        #device = startDaemon()
        files_to_send=[]
        pcdir, pcfile = os.path.split(pclocation)
        os.chdir(pcdir)
        workingdir=''
        for dev in client.devices():
            if dev.serial is not None:
                response = ''
                board_make = dev.shell('getprop Build.BRAND').strip()
                if board_make == 'MTK':
                    os.chdir(pcdir)
                    response +=f'working \n'\
                               'directory \n'\
                               'changed to \n '\
                               f'{pcdir}\n'

                    #print(pcfile,pcfile,pclocation,pcdir)
                    os.chdir(pcdir)
                    if not os.path.exists(f'{dev.serial}'):
                        os.mkdir(f'{dev.serial}')
                        os.chdir(f'{dev.serial}')
                        shtl.unpack_archive(pclocation, '.')
                        workingdir = f'{pcdir}\\{dev.serial}'
                        response +='unparking restoring zip' \
                                   'to \n' \
                                   f'{dev.serial}'
                    filed = os.listdir(f'{pcdir}\\{dev.serial}')
                    response +='\nchecking for file convention'
                    for fr in filed:
                        response+=f'\nfolder contains {fr}\n'
                        #fr.split(os.getcwd())
                        files_to_send.append(fr)

                else:
                    dev.shell('cd /storage/emulated/0/td && mkdir -p ' + partname)
                    locations = 'dev/block/platform'
                    ls_output = dev.shell(f'su -c ls {locations}/')
                    partition_path = f'/{locations}/{ls_output.strip().split()[-1]}/by-name/{partname}'
                    dev.push(src=pclocation,dest=f'/storage/emulated/0/td/{partname}/{partname}.tdf')
                    dev.shell(f'su -c "umount /mnt/vendor/*"')
                    dev.shell(f'su -c dd if=/storage/emulated/0/td/{partname}/{partname}.tdf of=/{partition_path}')
                    #part_location = dev.shell(f'su -c cd /storage/emulated/0/td/{partname}.bin')
                    #print(part_location)
                    #dev.shell(f'su -c dd=if=/storage/emulated/0/td/{} of=/{partition_path }')
                    dev.shell('reboot')
                    stopDaemon()
                return response,files_to_send,workingdir

    def pusher(self,filed_to_send,workingdir):
        response = ''
        startDaemon()

        cwd = os.getcwd()
        #print(cwd)
        for dev in client.devices():
            relpath =os.path.join(workingdir, f'{dev.serial}')
            os.chdir(relpath)

            if dev.serial is not None:

                dev.shell('su -c mkdir /storage/emulated/0/td')


            for file in filed_to_send:

                dev.push(file,f'/storage/emulated/0/td/{file}')

                response += f'\npacket sent to device'
        return response
    def part_mount(self, partname):
        device = startDaemon()

        response = ''
        for dev in client.devices():
            if dev.serial == device:
                board_make = dev.shell('getprop Build.BRAND').strip()
                if rootfs() == '/dev/block/platform/bootdevice/by-name/':
                    partname = ['nvdata', 'nvram', 'protect1', 'protect2','ncvcfg']
                    pmt = {}
                    for part in partname:
                        dev.shell('cd /mnt/vendor')
                        dev.shell(f'su -f umount {part}')
                        dev.shell(f'su -c umount {part}')
                        print('unmounted')
                        partition_path = f'{rootfs()}{part}'
                        print(partition_path)
                        dev.shell(f'su -c y | "mke2fs {partition_path}"')
                        print(dev.shell(f'su -c y | "mke2fs {partition_path}"'))
                        dev.shell(f'su -c "tune2fs -c0 -i0 {partition_path}"')
                       #S print(formumount)
                        response += dev.shell(f"su -c echo y | 'mke2fs {partition_path}'")
                    dev.shell('reboot nvrestore')

                else:
                    print(f'dealing with {board_make}')
                    partition_path = f'/{rootfs()}/{partname}'
                    dev.shell(f'su -c "umount /mnt/vendor/{partname}"')
                    print(dev.shell(f'su -c "umount/mnt/vendor/{partname}"'))
                    dev.shell(f'su -c echo y | "mkfs.ext4 {partition_path}"')
                    dev.shell(f'su -c "tune2fs -c0 -i0 {partition_path}"')
                    print(dev.shell(f'su -c "echo y | mkfs.ext4 {partition_path}"'))
                    dev.shell('reboot')

                    # the above line auto inputs the y as prompted in cmdline with echo y
                    print('device formatted')

            else:
                response += 'No adb device Found'

        response += f'\n device found {dev.serial}' \
                        f'\n {board_make}' \
                        f'\n using {board_make} Criteria' \
                        f'\n device is being prepared' \
                        f'\n device should reboot if not manually reboot'

        return response
detector = detect
backuping  = BackUP
def start_logging():
    t = threading.Thread(target=adbConnect)
    t.start()
'''def start_logging():
    logfield.delete('1.0', END)
    output = adbConnect()
    logfield.insert(END, f"\nDevice found with properties:\n{output}\n")'''

#backuping.PartBackup(BackUP,'C:',['nvdata','nvram''protect1','protect2'])


Partmnt = BackUP
#Partmnt.part_mount(Partmnt,'nvdata')
restoring  = backuping
Partbck = BackUP
'''response, files_to_send, workingdir = backuping.part_restore(
    BackUP, ,)'''
class repair(detect):
    def __init__(self,PartName):
        self.PartName = PartName
        super().__init__()
    def sn_repair(self,PartName):
        startDaemon()
        for device in client.devices():
            print(device.serial)
            locations = 'dev/block/platform'
            rootfs = device.shell(f'su -c "ls {locations}"')

            Partloc = f'{locations}/{rootfs.strip().split()[-1]}/by-name/{PartName}'
            device.shell(f'su -c "dd if={Partloc} of=storage/emulated/0/{device.serial}.tdf"')
            pat=os.getcwd()
            if os.path.dirname is not {device.serial}:
                os.mkdir(f'{pat}/{device.serial}')
                dire = os.path.curdir
                print(dire)
            print(pat)
            #device.pull(f'storage/emulated/0/{device.serial}',os.path.pardir)
            print(Partloc)

snRepair = repair
#snRepair.sn_repair(repair,'sec_efs')
