import asyncio
from tkinter.constants import END
from tkinter import filedialog as filer
from detect import adbConnect, backuping, Partbck
from detect import BackUP

def filedialog():
    backup = filer.asksaveasfilename(defaultextension='.td',initialdir=('/backup'),
                                 filetypes=[(('bin file','*.bin'),
                                              ('td file','*.tdf')
                                             )])


    return backup
def fileres():
    part_restore_file = filer.askopenfilename(defaultextension='.tar',initialdir=('/backup'),
                                 filetypes=[('bin file', '*.bin'),
        ('td file', '*.tdf'),
        ('tar files', '*.tar'),
                                            ('img files','*.img')])

    return part_restore_file
async def detectadb(textfield):
    async for result in adbConnect():
        # Update your GUI with the new result here
        textfield.delete(1.0, END)

        textfield.insert(END, f"\n{result}\n")
        await asyncio.sleep(1)


async def adinfo(texfield):
    # Run the adb function in the background
    adb_task = asyncio.create_task(detectadb(texfield))
    # Run the event loop
    await asyncio.gather(adb_task, return_exceptions=True)
'''async  def backup(textfield):
    backuping.PartBackup(BackUP, filedialog('efs'), 'efs')
    print(backuping.PartBackup(BackUP,filedialog('efs'),'efs'))

    async for result in backuping.PartBackup(BackUP,filedialog('efs'),'efs'):
        print(result)
        textfield.delete(1.0, END)
        textfield.insert(END, f"\nDevice found with properties:\n{result}\n")
        print(result)'''
async def backupinfo(texfield):
    texfield.delete(1.0,END)
    texfield.insert(1.0,'Starting inject')

    # Run the adb function in the background
    sector = 'efs'
    partbakup = asyncio.create_task(Partbck.PartBackup(BackUP,filedialog('efs'),'[nvdata,nvram,protect1,protect2]'))
    print('backing to temp fs')
    print(partbakup)
    await partbakup
    pullbackup = asyncio.create_task(Partbck.puller(BackUP,filedialog('efs'),'efs'))
    zipper = asyncio.create_task(Partbck.zipper(BackUP,[],filedialog('efs')))
    print('zipping necesitties to serial zip')
    texfield.insert(1.0,partbakup)
    texfield.insert(END,pullbackup)
    texfield.insert(END,zipper)
    # Run the event loop



