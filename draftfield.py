import threading
import os
import shutil
from gui import update_logfield
def pull_partition(partition_path, part, pcdir, device):
    backup_command = f'su -c "dd if={partition_path}/by-name/{part} of=/storage/emulated/0/td/{part}.tdf"'
    dev = device()
    dev.shell(f'su -c mkdir /storage/emulated/0/td')
    bckup = dev.shell(backup_command)
    dev.pull(src=f'/storage/emulated/0/td/{part}.tdf', dest=os.path.join(pcdir, f"{part.split('/')[-1][:-4]}_{dev.serial}"))
    print(f"Pulled partition {part} and saved as {part.split('/')[-1][:-4]}_{dev.serial}.")
    update_logfield(f"Pulled partition {part} and saved as {part.split('/')[-1][:-4]}_{dev.serial}.")
def zip_partitions(pclocation, device):
    pcdir, pcfile = os.path.split(pclocation)
    files_to_zip = []
    for file in os.listdir(pcdir):
        files_to_zip.append(file)
    file_ch = [f for f in files_to_zip if f.endswith(f"{device.serial}" )]
    os.chdir(pcdir)
    if not os.path.exists(f'{device.serial}'):
        os.mkdir(f'{device.serial}')
        for f in file_ch:
            shutil.move(src=(os.path.join(pcdir,f)), dst=f'{device.serial}')
    shutil.make_archive(f'{pclocation}_{device.serial}', 'tar', root_dir=f'{pcdir}\\{device.serial}')
    shutil.rmtree(f'{device.serial}', True)
    print(f"Zipped partitions and saved as {pclocation}_{device.serial}.")

def PartBackup(self, pclocation, part_name):
    device = startDaemon()
    locations = 'dev/block/platform'

    for dev in client.devices():
        if dev.serial == device:
            response = f"Device found is {dev.shell('getprop Build.BRAND').strip()}\n"
            partition_path = f'/{locations}/{dev.shell(f"su -c ls {locations}/").strip().split()[-1]}'
            threads = []

            for part in part_name:
                t = threading.Thread(target=pull_partition, args=(partition_path, part, pcdir, type(dev)))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            t = threading.Thread(target=zip_partitions, args=(pclocation, type(dev)))
            t.start()
            t.join()

            response += f"Backup completed and saved as {pclocation}_{dev.serial}\n"
            break

    return response
