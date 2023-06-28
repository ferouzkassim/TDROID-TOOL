import getpass
import os
import shutil
import tarfile
import tempfile
import time
import serial
import serial.tools.list_ports as prtlist
import subprocess
import shutil as shtl

import py7zr

from py7zr import py7zr as pyz
import pathlib as pth

import fastboot
from adbcon import startDaemon, host, port, client, stopDaemon
#py7zr a module to use for compressing snd decompressing with password
#importing the class to do detecting and exposing the srial number



#first things frst start the server then get devices
#then enumrate to get index and enumerate to get the respondent app
#apend it to a blank list the return the listy with the index and app appnended to it
class detect:
    def __init__(self,dev):
        self.dev =dev

    def adbConnect(self):
        startDaemon()
        prop = []
        resultprop = {}
        filteredprops = {}
        # the filtered keys to look for in prop
        prop_names = {
            'ro.product.model': 'Model',
            'ro.product.name': 'Product Name',
            'ro.build.id': 'Build ID',
            'ro.product.product.model': 'Product Code',
            'ro.build.product': 'Product',
            'ro.build.version.release': 'Android-Release',
            'ro.build.version.security_patch': 'Security Patch',
            'ro.build.PDA': 'Pda',
            'ro.carrier': 'Carrier',
            'ro.config.knox': 'Knox Version',
            'ro.csc.country_code': 'CSC',
            'ro.frp.pst': 'Frp Block',
            'ro.hardware.chipname': 'Hardware Chip',
            'ro.serialno': 'Serial Number',
            'sys.usb.config': 'Usb Config',
            'Build.BRAND': 'Brand',
            'gsm.version.baseband': 'Baseband',
            'knox.kg.state': 'Kg State',
            'ril.modem.board': 'Modem',
            'gsm.network.type': 'Network Type',
            'gsm.operator.iso-country': 'Gsm Operator',
            'gsm.version.baseband': 'Gsm Baseband',
            'gsm.operator.alpha': 'Gsm operator',
            'gsm.operator.iso-country': 'Country', }

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
        output = 'Reading info\n '
        output += 'starting dameon\n'
        for dev in devices:
            output += f'device found on {port} \n at {host}\n'
            # This will allow the GUI to update while the function is running
            if dev.serial is None:
                # This will allow the GUI to update while the function is running
                output += 'No Device Found\n'
            else:
                propstr = dev.shell('getprop')
                prop.append(propstr.split('\n'))
                for sublist in prop:
                    for stringprop in sublist:
                        clean_string = stringprop.strip().replace("[", "").replace("]", "")
                        if clean_string and ':' in clean_string:
                            key_value_pair = clean_string.split(': ', 1)
                            # to split the first occurence hence the :1 just incaase it doesnt split it can skip
                            if len(key_value_pair) == 2:
                                key, value = key_value_pair
                                resultprop[key] = value
                                if key in filter_keys:
                                    filteredprops[key] = value
                    output += f"\n{dev.serial}\n"
                    for prop, answer in filteredprops.items():
                        short_prop = prop_names.get(prop, prop)
                        output += f"{short_prop} = {answer}\n\n"

        return output
    def adbfrpreset(self):

        startDaemon()
        response=''
        for dev in client.devices():
            print(dev.serial)
            response += dev.serial
            dev.shell('am start -n com.google.Android.gsf.login/')
            dev.shell('am start -n com.google.Android.gsf.login.LoginActivity')
            dev.shell('content insert –uri content://settings/secure –bind name:s:user_setup_complete –bind value:s:1')
            dev.reboot()
            response+='resting frp done in adb'
            return response

    def applister(self):
        startDaemon()
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
            qlmpartition = f'/{locations}/{ls_output.strip().split()[-1]}'


            return  partition_path,qlmpartition
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

    def ExynosPartBackup(self, pclocation, part_name,):
            response = ''
            response +='Backing up Exynos\n'
            device = startDaemon()
            backup_files = []
            locations = 'dev/block/platform'
            if client.devices()==None:
                response+='No adb rooted device found'

            for dev in client.devices():
                board_make = dev.shell('getprop ril.modem.board').strip()
                if dev.serial == device:
                    # su - c breaks out of the su waiting time and lets you execute once
                    response += f'\ndevice found is {board_make}\n'
                    # response = dev.shell(f'su -c "dd if=/{locations}'
                    # f'/bootdevice/by-name/efs of=/sdcard/efs.tdf"')'''
                    pcdir, pcfile = os.path.split(pclocation)
                    dev.shell(f'su -c mkdir /storage/emulated/0/td')
                    new_pclocation = os.path.join(pcdir, dev.serial)
                    otherfiles = []
                    for par in part_name:
                        backup_command = f'su -c dd if=/dev/block/by-name/{par} of=/storage/emulated/0/td/{par}.tdf'
                        new_pclocation = os.path.join(pcdir, pcfile)
                        dev.shell(backup_command)
                        locate = f'/storage/emulated/0/td/{par}.tdf'
                        otherfiles.append(locate)
                        #print(otherfiles)
                    for loc in otherfiles:
                        pcfile = f"{loc.split('/')[-1][:-4]}+{dev.serial}"
                        new_pclocation = os.path.join(pcdir, pcfile)
                        #print(new_pclocation)
                        #print(pcfile)
                        dev.pull(loc, new_pclocation)

                    #print(locate)
                    # dev.pull(src=f'/storage/emulated/0/td/{part}.tdf', dest=new_pclocation)
                    os.chdir(pcdir)
                    response += f'\n {part_name} back up saved as' \
                        # Do backup here
                    # sybcing to pc location
                    # dev.pull(src=part_name_backup, dest=f'{pclocation}')
                    # print(dev.shell(f'su -c cd /{locations}'))
                    # bckup = dev.shell((f'su -c "dd if=/{locations}/{ls_output}by-name/efs" of=/storage/emulated/0/{part_name}.tdf'))
                    # Do backup here
                    # print(ls_output)
                    # print(bckup)
                response += f'\n using {board_make} spring board' \
                            f' \n working from {pclocation}' \
                            f'\n compressing as {pclocation}_{dev.serial}'
                response
                #print(pcdir)
            return response, backup_files,pcdir,pclocation


    def mtkPartBackup(self,partfiles):
        startDaemon()
        response=''
        backup_files = []

        for dev in client.devices():
            response +='checking for device'
            dev.shell(f'su -c mkdir /storage/emulated/0/td/')
            for part in partfiles:
                    backup_command = f'su -c "dd if={rootfs()[0]}/{part} of=/storage/emulated/0/td/{part}.tdf"'
                    bckup = dev.shell(backup_command)
                    response += 'exploiting..... '
                    backup_files.append(f'/storage/emulated/0/td/{part}.tdf')
                    dev.shell('cd /storage/emulated/0/td/')


        return backup_files,response

    def puller(self, backup_files, pclocation):
        response = ''
        for dev in client.devices():
            for part in backup_files:
                # Change to the backup directory on the device
                dev.shell('cd /storage/emulated/0/td/')

                # Extract the directory and filename components of pclocation
                #
                # Construct the new filename with the device serial number
                new_filename = f"{part.split('/')[-1]}_{dev.serial}"
                print(new_filename)
                # Construct the full path of the destination file on the PC
                new_pclocation = os.path.normpath(os.path.join(pclocation, dev.serial, new_filename))


                # Check if the directory exists and create it if it doesn't
                os.makedirs(os.path.dirname(new_pclocation), exist_ok=True)
                print(new_pclocation)
                # Pull the file from the device to the modified pclocation
                dev.pull(src=part, dest=new_pclocation)
                print(new_filename,new_pclocation)
                # Add the filename to the response string
                response += f'\n{new_filename}\t'
                print(pclocation)
        return response, pclocation

    def zipper(self, location,pclocation):
        response = ''
        print(location)
        os.path.curdir = location
        for dev in client.devices():
            if not os.path.exists(dev.serial):
                os.mkdir(dev.serial)
            files_to_zip = []
            for f in os.listdir():
                if f.endswith(dev.serial):
                    files_to_zip.append(f)

            for fil in files_to_zip:
                shtl.move(fil, dev.serial)
                if fil.endswith(f"-{dev.serial}"):
                    print(fil)

            shtl.make_archive(f'{pclocation}_{dev.serial}', 'tar', root_dir=dev.serial)
            shtl.rmtree(dev.serial, True)
            response += f'\n compressing as {location}_{dev.serial}' \
                        f'\n files saved to archive and ready for further use '
        return response

    def exynosrestore(self, pcfile,):
        startDaemon()
        files_to_send = []
        pcdir,pcf =os.path.split(pcfile)
        os.mkdir(f'{pcdir}/temp')
        os.chdir(f'{pcdir}/temp')
        working_dir=os.getcwd()
        shtl.unpack_archive(pcfile,working_dir)
        if pcf.endswith('.tar'):
            print('using tar format')
            for file in os.listdir(working_dir):
                try:
                    part, sn = file.split('+')
                    newname=file.replace(f'+{sn}','')
                    os.rename(file, newname)
                except:
                    pass
        elif pcf.endswith('.zip'):
            print('using zip format')
            for file in os.listdir(working_dir):
                if file.endswith('.bin'):
                    newname = file.replace('.bin','')
                else:
                    newname = file.replace('.img','')

                os.rename(file,newname)
                print(files_to_send)
        else:
            pass
        for file in os.listdir(working_dir):
            files_to_send.append(file)
            print(files_to_send)
        for dev in client.devices():
            if dev:
                for file in files_to_send:
                    oa=os.path.join(file)
                    print(oa)
                    dev.push(src=oa, dest=f'/storage/emulated/0/{file}')
                    dev.shell(f'su -c umount mnt/vendor/{file}')
                    dev.shell(f'su -c dd if=/storage/emulated/0/{file} of=/dev/block/by-name/{file}')
                    dev.shell(f'su rm -rR /storage/emulated/0/{file}')
                dev.reboot()
                return 0
        shtl.rmtree(working_dir,True)
    def qlmbackup(self,pclocation,part_name):
        response = ''
        response += 'Backing up Exynos\n'
        device = startDaemon()
        backup_files = []
        locations = 'dev/block/platform'
        if client.devices() == None:
            response += 'No adb rooted device found'

        for dev in client.devices():
            board_make = dev.shell('getprop ril.modem.board').strip()
            if dev.serial == device:
                # su - c breaks out of the su waiting time and lets you execute once
                response += f'\ndevice found is {board_make}\n'
                # response = dev.shell(f'su -c "dd if=/{locations}'
                # f'/bootdevice/by-name/efs of=/sdcard/efs.tdf"')'''
                pcdir, pcfile = os.path.split(pclocation)
                dev.shell(f'su -c mkdir /storage/emulated/0/td')
                new_pclocation = os.path.join(pcdir, dev.serial)
                otherfiles = []
                for par in part_name:
                    print(f'{rootfs()[1]}/{par}')
                    backup_command = f'su -c dd if=/{rootfs()[1]}/{par} of=/storage/emulated/0/td/{par}.tdf'
                    new_pclocation = os.path.join(pcdir, pcfile)
                    dev.shell(backup_command)
                    locate = f'/storage/emulated/0/td/{par}.tdf'
                    otherfiles.append(locate)
                    # print(otherfiles)
                for loc in otherfiles:
                    pcfile = f"{loc.split('/')[-1][:-4]}_{dev.serial}"
                    new_pclocation = os.path.join(pcdir, pcfile)
                    # print(new_pclocation)
                    # print(pcfile)
                    dev.pull(loc, new_pclocation)
                # print(locate)
                # dev.pull(src=f'/storage/emulated/0/td/{part}.tdf', dest=new_pclocation)
                os.chdir(pcdir)
                response += f'\n {part_name} back up saved as' \
                    # Do backup here
                # sybcing to pc location
                # dev.pull(src=part_name_backup, dest=f'{pclocation}')
                # print(dev.shell(f'su -c cd /{locations}'))
                # bckup = dev.shell((f'su -c "dd if=/{locations}/{ls_output}by-name/efs" of=/storage/emulated/0/{part_name}.tdf'))
                # Do backup here
                # print(ls_output)
                # print(bckup)
            response += f'\n using {board_make} spring board' \
                        f' \n working from {pclocation}' \
                        f'\n compressing as {pclocation}_{dev.serial}'
            response
            # print(pcdir)
        return response, backup_files, pclocation
    def mtkrestore(self,pclocation):
        startDaemon()
        response =''
        files_to_send = []
        pcdir, pcfile = os.path.split(pclocation)
        os.chdir(pcdir)
        workingdir = ''
        for dev in client.devices():
            if dev:
             os.chdir(pcdir)
             response += f'working \n' \
                        'directory \n' \
                        'changed to \n ' \
                        f'{pcdir}\n'

            # print(pcfile,pcfile,pclocation,pcdir)
            os.chdir(pcdir)
            if not os.path.exists(f'{dev.serial}'):
                os.mkdir(f'{dev.serial}')
                os.chdir(f'{dev.serial}')
                shtl.unpack_archive(pclocation, '.')
                workingdir = f'{pcdir}\\{dev.serial}'
                response += 'unparking restoring zip' \
                            'to \n' \
                            f'{dev.serial}'
            filed = os.listdir(f'{pcdir}\\{dev.serial}')
            response += '\nchecking for file convention'
            for fr in filed:
                response += f'\nfolder contains {fr}\n'
                # fr.split(os.getcwd())
                files_to_send.append(fr)
    def qlmrestore(self,pcfile):
        username = getpass.getuser()
        paramdir=os.getcwd()
        for dev in client.devices():
            os.makedirs(f'{dev.serial}', exist_ok=True)
            os.chdir(f'{dev.serial}')
            with tarfile.open(pcfile, 'r') as tar:
                bj = tar.getmembers()
                tar.extractall('modem', bj)

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
    def part_mountmtk(self, partname):
        device = startDaemon()

        response = ''
        response +='Fixing Mtk Baseband\n'
        for dev in client.devices():
            if dev.serial == device:
                    board_make = dev.shell('getprop ril.modem.board').strip()

                    partname = ['nvdata', 'nvram', 'protect1', 'protect2','ncvcfg']
                    pmt = {}
                    for part in partname:
                        dev.shell('cd /mnt/vendor')
                        dev.shell(f'su -f umount {part}')
                        dev.shell(f'su -c umount {part}')
                        print('unmounted data')
                        response+='Unmounted\n'
                        partition_path = f'{rootfs()}/{part}'
                        dev.shell(f'su -c y | "mke2fs {partition_path}"')
                        response+='Clearing springboard\n'
                        dev.shell(f'su -c y | "mkfs.ext4 {partition_path}"')
                        dev.shell(f'su -c "tune2fs -c0 -i0 {partition_path}"')
                        print('formatting')
                        response+='Tuning File system\n'

                       #S print(formumount)
                        dev.shell(f"su -c echo y | 'mke2fs {partition_path}'")

                    dev.shell('reboot nvrestore')
        return response

    def part_mountex(self, partname):
         device = startDaemon()
         response = ''
         response+='Fixing Exynos baseband \n'
         print('exynosing')
         for dev in client.devices():
            board_make = dev.shell('getprop ril.modem.board').strip()
            response+=f'\n device found {dev.serial}\n' \
                    f'\n using {board_make} Criteria\n'
            #partition_path = f'{rootfs()}{partname}\n'
            print(dev.shell(f'su -c "umount /mnt/vendor/{partname}"'))
            print('unmounted')
            #dev.shell(f'su -c umount {partname}')
            #print(dev.shell(f'su -c "cd mnt/vendor" && "umount {partname}" &&"ls"'))
            #print(dev.shell(f'su -c umount -l /mnt/vendor/{partname}'))
            response+=f'\n device is being prepared\n'
            response +=f'\nunmounting security\n'
            #dev.shell(f'su -c "umount /mnt/vendor/{partname}"'
            #print(dev.shell(f"mount | grep {partname}"))
            #print(dev.shell(f'su -c "umount /mnt/vendor/{partname}"'))
            #print(dev.shell(f'su -c "umount /dev/block/by-name/{partname}"'))
            #print(dev.shell(f'su -c "umount /mnt/vendor/{partname}"'))
            '''dev.shell(f'cd mnt/vendor')
            print(dev.shell(f'su -c umount {partname}'))
            dev.shell(f'umount efs')
            dev.shell('cd')'''
            #print(dev.shell(f'cd /dev/block/by-name'))
            print(dev.shell(f'su -c y | mkfs.ext4 dev/block/by-name/efs'))
            print(dev.shell(f'su -c "tune2fs -c0 -i0 /dev/block/by-name/{partname}"'))
            response +="\nDiscarding device blocks: done \n" \
                       "\nDiscard takes 0.00110s.\n" \
                       "\nCreating filesystem with 5120 4k blocks and 1280 inode\n" \
                       "\nAllocating group tables: done\n " \
                       "\nWriting inode tables: done     \n " \
                       "\nWriting superblocks and filesystem accounting information: done\n"
            response +=f'\nfixing security and tuning file system\n'
            dev.reboot()
            response+='\nrebooting\n'

            # the above line auto inputs the y as prompted in cmdline with echo y



         return response
detector = detect
backuping  = BackUP
detc = detect


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

    import getpass

    def partrepair(self, part_name,newsn):
        response=''
        startDaemon()
        username = getpass.getuser()
        home_dir = os.path.expanduser(f"~{username}")

        temp_dir = tempfile.mkdtemp(prefix='tempsn', dir=f'{os.getcwd()}\\Videos')

        try:
            for device in client.devices():

                device.shell(f'su -c "dd if=/efs/FactoryApp/{part_name} of=/storage/emulated/0/{device.serial}.txt"')
                destn = f'{temp_dir}\\{part_name}'
                # Pull the TDF file from the device to the temporary directory
                pul=device.pull(f'/storage/emulated/0/{device.serial}.txt', destn)
                time.sleep(2)
                print(pul)
                print('pulled')
                # f'{home_dir}\\Desktop\\{device.serial}'
                with open(destn, 'r+') as f:
                    content = f.read()
                    print(content)
                    print(f)
                    content.replace(f'{device.serial}', newsn)
                    f.seek(0)
                    #f.write(new_content)
                    f.truncate()
                device.push(destn, f'/storage/emulated/0/')
                device.shell(f'su -c "dd if=/storage/emulated/0/serial_no of=/efs/FactoryApp/serial_no"')
                time.sleep(1)

                try:
                    if os.path.isfile(destn) or os.path.islink(destn):
                        os.remove(destn)
                    elif os.path.isdir(destn):
                        shutil.rmtree(destn)
                except Exception as e:
                    print(f"Error deleting {destn}: {e}")


        finally:
         return temp_dir,destn,device
    def partrepair(self, part_name,newsn):
        response=''
        startDaemon()
        username = getpass.getuser()
        home_dir = os.path.expanduser(f"~{username}")

        temp_dir = tempfile.mkdtemp(prefix='tempsn', dir=f'{os.getcwd()}\\Videos')

        try:
            for device in client.devices():

                device.shell(f'su -c "dd if=/efs/FactoryApp/{part_name} of=/storage/emulated/0/{device.serial}.txt"')
                destn = f'{temp_dir}\\{part_name}'
                # Pull the TDF file from the device to the temporary directory
                pul=device.pull(f'/storage/emulated/0/{device.serial}.txt', destn)
                time.sleep(2)
                print(pul)
                print('pulled')
                # f'{home_dir}\\Desktop\\{device.serial}'
                with open(destn, 'r+') as f:
                    content = f.read()
                    print(content)
                    print(f)
                    content.replace(f'{device.serial}', newsn)
                    f.seek(0)
                    #f.write(new_content)
                    f.truncate()
                device.push(destn, f'/storage/emulated/0/')
                device.shell(f'su -c "dd if=/storage/emulated/0/serial_no of=/efs/FactoryApp/serial_no"')
                time.sleep(1)

                try:
                    if os.path.isfile(destn) or os.path.islink(destn):
                        os.remove(destn)
                    elif os.path.isdir(destn):
                        shutil.rmtree(destn)
                except Exception as e:
                    print(f"Error deleting {destn}: {e}")


        finally:
         return temp_dir,destn,device
    def edito(self, file_path, sn,new_sn):
        for device in client.devices():
         with open(file_path, 'r+',encoding='utf-8') as f:
            content = f.read()
            content.replace(sn, new_sn)
            f.close()
            print(f.read())
        '''device.push(file_path, f'/storage/emulated/0/serial_no')
        device.shell(f'su -c "dd if=/storage/emulated/0/serial_no of=/efs/FactoryApp/serial_no"')
        time.sleep(1)'''

        try:
             if os.path.isfile(file_path) or os.path.islink(file_path):
                 os.remove(file_path)
             elif os.path.isdir(file_path):
                 shutil.rmtree(file_path)
        except Exception as e:
             print(f"Error deleting {file_path}: {e}")

    def bootfixer(self):
        username = getpass.getuser()
        home_dir = os.path.expanduser(f"~{username}")
        renam=['svb_orange.jpg','booting_warning.jpg','orange_state.jpg','custom_warning.jpg']
        for dev in client.devices():
            os.makedirs(f'{dev.serial}', exist_ok=True)
            os.chdir(f'{dev.serial}')
            paramdir=os.getcwd()
            print(paramdir)
            dev.shell(f'su -c "dd if=/dev/block/by-name/up_param of=/storage/emulated/0/um.tar"')
            dev.pull('/storage/emulated/0/um.tar', os.path.join(paramdir,f'up.tar'))
            with tarfile.open(f'{paramdir}\\up.tar', 'r') as tar:
                obj=tar.getmembers()
                tar.extractall('up',obj)
                relpath = f'{dev.serial}\\up'
                print(relpath)
                print(os.listdir('up'))
                for file in os.listdir('up'):

                        if file in renam:
                            old_path = os.path.join('up', file)
                            new_name = file.replace('.jpg', '.tdf')
                            new_path = os.path.join('up', new_name)
                            os.rename(old_path, new_path)

                tar.close()

            with tarfile.open('newup.tar','w') as tar:
                for file in os.listdir('up'):
                    tar.add(os.path.join('up', file),arcname=file)
                tar.close()
            dev.push('newup.tar','/storage/emulated/0/td.tar')
            dev.shell('su -c "dd if=/storage/emulated/0/td.tar of=/dev/block/by-name/up_param"')
            dev.reboot()
            os.chdir("..")
            print(os.getcwd())
        try:
                os.remove(dev.serial)
        except PermissionError as e:
                print(e)
boot =repair
#boot.partrepair(boot,'sec_efs','RWIZZSXCCVN')
def portsimple():
    while True:
        for prt in prtlist.comports():
            print(prt)
            #
            #
            #dev=serial.Serial.open(prt.device)
    return prt


#snRepair.partrepair(repair,'up_param')
class modem():
    def __init__(self,ports):
        self.ports = ports
    def samport(self):
        ports = prtlist.comports()
        for dport in ports:
            if dport.pid=='685D' and dport.vid=='04E8':
                print('domode found')

        return ports
    def Readmodem(self,ports):
        response=''
        responseli=[]
        for port in ports:
            #USB\VID_04E8 & PID_6860

            if port.vid==0x4E8 and port.pid==0x6860:
                response += str(port.hwid)
                ser = serial.Serial(port.name)
                print(f"Sending AT+DEVCONINFO\n")
                ser.write(b'AT+DEVCONINFO')
                time.sleep(0.5)
                ret = ser.read_all()
                response += ret.decode()
                print(f"Received{ret}")
            #else:
             #   pass
        responseli.append(response.split(';'))
        response = ''.join(responseli[0])  # join the list into a single string
        return responseli

    def downloadinfo(self, formatted_output=None):
        ports = prtlist.comports()
        response = []

        for port in ports:
            arranged_data = []
            if port.vid==0x4E8 and port.pid==0x685D:
                arranged_data.append(f"Found {port.hwid}'")
                arranged_data.append(f"At {port.name}")
                #USB VID:PID=04E8:685D
                ser = serial.Serial(port.name, baudrate=115200, timeout=1)
                ser.write(b'DVIF\n')
                time.sleep(0.0001)
                line_data = ser.read_until()
                ser.close()
                data = line_data.decode().split(';')
                print (data)
                for d in data:
                    d = d.replace('PRODUCT', 'EMMC NAME')  # assign the modified string to the same variable
                    d = d.replace('FWVER','AP VERSION')
                    d = d.replace('CAPA','CAPACITY')
                    d = d.replace('VENDOR','EMMC MAKE')
                    d = d.replace('SALES','COUNTRY CSC')
                    d= d.replace('=',':\t\t')

                    if "@#" in d:
                        d = d.replace("@#", "")

                    arranged_data.append(d.strip())
                response.append(arranged_data)
            else:
                data = 'No Dmode Device found with 0x4E8 / 0x685D'
                arranged_data.append(data.strip())
                response.append(arranged_data)

        return response

class flasher():

    def __init__(self,part):
        self.part=part
    def partitionflasher(self,part):
        with tarfile.open(part,'r') as par:
            content=par.getmembers()
            #print(content)

            for port in serial.tools.list_ports.comports():
               print(port.name, port.manufacturer, port.vid, port.pid)
               dev = serial.Serial(baudrate=115200, port=port.name)
               print(dev.port)
               dev.write(b'ODIN\r\n')
               time.sleep(1)
               #dev.write(b'ODIN REBOOT_MODE_CHARGING\r\n')
               #dev.write(b'WRITE up_param.bin')
               dev.write(b'THOR\r\n')
               #dev.write(b'LOKE\r\n')
               #dev.write(b'FLSW,up_param.bin,up_param')
               print(dev.read_all().decode())


               #dev.close()


flash = flasher
#flash.partitionflasher(flash,f'C:\\Users\\DROID\\Desktop\\a127f\\U5\\BL_A127FXXU5AVC4_CL23021938_QB50163737_REV00_user_low_ship_MULTI_CERT.tar.md5')
#mode.Readmodem(mode,mode.samport(mode))
#mode.downloadinfo(mode)
class fb():
    def __init__(self):
        pass
    def Read_info(self):
        fb=fastboot.fbdevices()
frash = flasher
#frash.flash(frash,"C:\\Users\\DROID\\Desktop\\A035FXXU1AVD3-11-[KMDC6001DM-BXXX_8BD5CA4C]\\OFFICIAL\\A03_CIS_OPEN.pit")
