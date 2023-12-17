import asyncio
import os.path
import pathlib
import subprocess
import threading
import time
from pathlib import Path

import serial.tools.list_ports as prtlist
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QThread, QEventLoop, QObject
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QDialog
import detect
import fastboot
import samsungflasher
import usbcom
from detect import BackUP, backuping
from gui import Ui_main
from samsungflasher import readpit


class Dmode(QThread):
    resultReady = pyqtSignal(list)
    updateProgress = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        for i in range(1, 101):  # Adjust the range based on the duration
            time.sleep(0.01)  # Wait for 0.5 seconds
        self.updateProgress.emit(i)
        result = detect.modem.downloadinfo(detect.modem)

        self.resultReady.emit(result)


# samsung flashing log thread
class LogEmitter(QObject):
    logReady = pyqtSignal(str)


class baseband(QThread):
    def __init__(self, partnem, logfield):
        super().__init__()
        self.partnem = partnem
        self.logfield = logfield

    def run(self):
        asyncio.run(detect.backuping.part_mountex(BackUP, self.partnem, self.logfield))


class basbeband_sam_mtk(QThread):
    def __init__(self, log):
        super().__init__()
        self.logfield = log

    def run(self):
        asyncio.run(detect.BackUP.part_mountmtk(self, self.logfield))

class write_backup(QThread):
    def __init__(self, file_to_write, logfield, soc_Type):
        super().__init__()
        self.file_to_write = file_to_write
        self.logfield = logfield
        self.soc_type = soc_Type

    def run(self):
        asyncio.run(detect.BackUP.backup_restore(BackUP, self.file_to_write, self.logfield, self.soc_type))


class exynos_write(QThread):
    def __init__(self, logfield, file_to_write):
        super().__init__()
        self.file_to_write = file_to_write
        self.logfield = logfield

    def run(self):
        asyncio.run(detect.BackUP.exynosrestore(BackUP, self.file_to_write, self.logfield))


class fastboot_flasher(QThread):
    def __init__(self, part, file, widget):
        super().__init__()
        self.part = part
        self.file = file
        self.widget = widget

    def run(self):
        asyncio.run(fastboot.fbb.fbtflasher(self.part, self.file, self.widget))


class srialrepair(QThread):
    def __init__(self, newsn, logfield):
        super().__init__(None)
        self.newsn = newsn
        self.logfield = logfield

    def run(self):
        task1 = asyncio.run(detect.boot.snrepair(self, self.newsn, self.logfield))


class MainDialog(QDialog):
    def __init__(self):
        self.fastboot_flasher = None
        self.write_backup = None
        self.draftli = []
        self.baseband = None
        super().__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)
        # threading download mode slotsss
        self.samthread = samsungflasher.SamsungFlasherThread(self.ui.logfield, self.ui.progressBar)
        self.samthread.log_signal.connect(self.logupdater)
        self.samthread.progress_signal.connect(self.updateProgressBar)
        #flashng thread
        self.fastbootThread  = fastboot.Fboot(self.ui.logfield_3)
        self.mtklist = ['Mtk General', 'SM-A013G', 'SM-A037F', 'SM-A125F', 'SM-A225F', 'SM-A022F']
        self.exynolist = ['Exynos General', 'SM-A127F', 'SM-A217f', 'SM-A135F', 'SM-A047F']
        self.qlmlist = ['SM-A235F']
        self.qlmlist.sort()
        self.exynolist.sort()
        self.mtklist.sort()
        samlog = self.ui.logfield.verticalScrollBar()
        samlog.setValue(samlog.maximum())
        fblog = self.ui.logfield_3.verticalScrollBar()
        fblog.setValue(fblog.maximum())
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.show()
        self.ui.repairsn.clicked.connect(self.snrepair)
        self.modelist = sorted(self.mtklist + self.exynolist + self.qlmlist)
        # Connect button click signal to function
        self.ui.Read_info_adb.clicked.connect(self.read_info_adb)
        self.ui.Read_info_cp.clicked.connect(self.cpreader)
        self.ui.readd.clicked.connect(self.dmodeasync)
        self.ui.fixbootloader.clicked.connect(self.bootfix)
        self.ui.Readinfofb.clicked.connect(self.fastbooinfo)
        self.ui.fbBootUnlocker.clicked.connect(self.fb_unlocking)
        self.ui.fbflash.clicked.connect(self.fbFlashing)
        # self.ui.writeefs.clicked.connect(self.open_backup)
        if self.ui.modelselector.currentText() in self.exynolist:
            self.ui.Fixbaseband.clicked.connect(lambda: self.exynosbb)
            self.ui.Write_Efs.clicked.connect(lambda: self.exynoswrtefs)
            self.ui.Read_security.clicked.connect(lambda: self.readexynosecurity)
            self.ui.write_security.clicked.connect(self.exynosRestor)

        if self.ui.modelselector.currentText() in self.mtklist:
            self.ui.Fixbaseband.clicked.connect(lambda: self.fixbbmtk)
            self.ui.Read_security.clicked.connect(lambda: [self.readmtk(), print('mtkread')])
            self.ui.write_security.clicked.connect(self.writemtkBackup)
        elif self.ui.modelselector.currentText() in self.qlmlist:
            self.ui.write_security.clicked.connect(self.writeqlm)

        self.ui.modelselector.addItems(self.modelist)
        self.ui.comboBox.addItem(asyncio.run(self.detect_unplug()))

        self.ui.reset_frp.clicked.connect(self.resetfrp)
        # self.ui.qlmreadefs.clicked.connect(self.readqlmsec)
        self.ui.flashsmsng.clicked.connect(self.samlog)
        self.ui.modelselector.activated.connect(self.modelselector)
        self.ui.fixdload.clicked.connect(self.readpit)
        self.ui.blbtn.clicked.connect(lambda: [self.loadedfile(self.ui.blline, self.fileloader()),
                                               self.ui.blcheckbox.setChecked(True)])
        self.ui.apbtn.clicked.connect(lambda: [self.loadedfile(self.ui.apline, self.fileloader()),
                                               self.ui.apcheckbox.setChecked(True)])
        self.ui.cpbdtn.clicked.connect(lambda: [self.loadedfile(self.ui.cpline, self.fileloader()),
                                                self.ui.cpcheckbox.setChecked(True)])
        self.ui.cscbtn.clicked.connect(lambda: [self.loadedfile(self.ui.cscline, self.fileloader()),
                                                self.ui.csccheckbox.setChecked(True)])
        self.ui.databtn.clicked.connect(lambda: [self.loadedfile(self.ui.userdataline, self.fileloader()),
                                                 self.ui.userdtacheckbox.setChecked(True)])
        self.ui.pitcheckbox.clicked.connect(
            lambda: [self.loadedfile(self.ui.pitline, self.fileloader()), self.ui.pitcheckbox.nextCheckState(True)])
        self.ui.fbload.clicked.connect(lambda: self.fbloader())
        self.ui.logfield.setStyleSheet("color: green;font-weight:bold")

    def updateProgressBar(self, value):
        self.ui.progressBar.setValue(value)

    def logupdater(self, value):
        self.ui.logfield.append(value)

    def resetfrp(self):
        logging = ''
        usbcom.enableADB()
        detect.detc.adbfrpreset(detect.detc)
        '''for log in detect.detc.adbfrpreset(detect.detc):
            self.ui.logfield.append(log)'''

    def snrepair(self, ):
        newsno = self.ui.snEdit.text()
        self.ui.progressBar.setValue(10)
        print(56)
        self.snrepairer = srialrepair(newsno, self.ui.logfield)
        self.snrepairer.start()
        """detect.repair.partrepair(detect.repair, f'serial_no', self.ui.snEdit.text())"""
        self.ui.progressBar.setValue(100)

    def bootfix(self):
        detect.boot.bootfixer(detect.boot)

    def save_backup(self):
        file, _ = QtWidgets.QFileDialog.getSaveFileName(
            filter=("files (*.img *.bin *.tdf *.tar)"), initialFilter='*.tdf'
        )
        return file

    def fileloader(self):
        fiel, _ = QtWidgets.QFileDialog.getOpenFileName(filter="files (*.pit *.md5 *.tar *.zip)",
                                                        initialFilter='.tar')
        if fiel:
            return fiel
        else:
            # Handle the case where the user canceled the file dialog or an error occurred
            return None

    def loadedfile(self, part, file):
        if file:
            fileloaded = part.setText(file)
        else:
            # Handle the case where the file path is None (e.g., user canceled the file dialog)
            print("File loading canceled or failed.")

    def modelselector(self):
        model = self.ui.modelselector.currentText()
        self.ui.Fixbaseband.disconnect()  # remove any previous connections
        if model in self.mtklist:
            self.ui.Read_security.setText('Read Nv')
            self.ui.write_security.setText('Write Nv')
            self.ui.Read_security.clicked.connect(lambda: self.readmtk())
            self.ui.Fixbaseband.clicked.connect(self.fixbbmtk)
            self.ui.write_security.clicked.connect(self.writemtkBackup)
            if not self.ui.MountNetwork.isVisible():
                self.ui.MountNetwork.show()

        elif model in self.exynolist:
            self.ui.Read_security.setText('Read Security')
            self.ui.Read_security.clicked.connect(self.readexynosecurity)
            self.ui.write_security.setText('Write Security')
            self.ui.write_security.clicked.connect(self.exynosRestor)
            self.ui.Fixbaseband.clicked.connect(self.exynosbb)
            self.ui.MountNetwork.hide()

        elif model in self.qlmlist:
            self.ui.MountNetwork.hide()
            self.ui.write_security.clicked.connect(self.writeqlm)

    def readmtk(self):

        self.ui.progressBar.setValue(10)
        print('reading mtk')
        loging = ''
        back = backuping.mtkPartBackup(BackUP, ['nvdata', 'nvram', 'protect1', 'protect2'])
        self.ui.progressBar.setValue(25)
        pull = backuping.puller(BackUP, back[0], self.save_backup())
        self.ui.progressBar.setValue(60)
        ziper = BackUP.zipper(BackUP, pull[1])
        self.ui.progressBar.setValue(75)
        for output in back, ziper:
            loging += ''.join(map(str, output))
        self.ui.progressBar.setValue(100)
        self.ui.logfield.append(loging)
        self.ui.logfield.repaint()

    def fixbbmtk(self):
        self.ui.logfield.append('Loging for Mtk Baseband repair')
        self.basebandmtk = basbeband_sam_mtk(self.ui.logfield)
        self.basebandmtk.start()
        self.ui.logfield.repaint()

    def read_info_adb(self, Rres):
        # Call adbConnect function
        self.ui.progressBar.setValue(0)
        self.ui.logfield.setText(f'logging for {self.ui.modelselector.currentText()}\n')
        self.ui.progressBar.setValue(50)
        try:
            t2 = asyncio.run(detect.detc.adbConnect(detect, self.ui.logfield))
        except RuntimeError:
            self.ui.logfield.append("Check for confirmation dialog on device\n "
                                    "Or check if adb is enabled \n Lastly check for driver installation")
        self.ui.logfield.repaint()
        self.ui.progressBar.setValue(100)

    def cpreader(self):
        self.ui.logfield.setText('reading in MTP Mode')
        self.ui.progressBar.setValue(0)
        self.ui.logfield.setStyleSheet('color:green;font-weight:bold')
        output = ''
        replace_dict = {"MN": "MODEL:\t",
                        "BASE:": "BASE:\t",
                        "VER:": "VERSION:\t",
                        "HIDVER:": "DEVICE FIRMWARE\t",
                        "MNC:": "MNC:\t",
                        "MCC:": "MCC:\t",
                        "PRD:": "PRD:\t",
                        "AID:": "AID:\t",
                        "CC:": "CC:\t",
                        "OMCCODE:": "OMCCODE:\t",
                        "SN:": "SERIAL NUMBER:\t",
                        "IMEI:": "IMEI:\t",
                        "UN:": "UNIQUE ID:\t",
                        "PN:": "PN:\t",
                        "CON:": "USB CONNECTION:\t",
                        "LOCK:": "LOCK\t",
                        "LIMIT:": "LIMIT\t",
                        "SDP:": "SDP\t",
                        "HVID:": "DATA TREE:\t"}

        info = asyncio.run(detect.modem.Readmodem(detect.modem,
                                                  detect.modem.samport(detect.modem)))

        try:
            for ifn in info:
                for dat in ifn:
                    fida = dat.replace('(', ':\t').replace(')', "").replace('AT+DEVCONINFO', '').replace('+DEVCONINFO',
                                                                                                         '').replace(
                        '#OK#',
                        '').replace(
                        'OK', '')
                    fida.replace(')', "")
                    for key, value in replace_dict.items():
                        fida = fida.replace(key, value)
                    output += fida + "\n"
                    self.ui.logfield.append(fida)
                    self.ui.logfield.repaint()
        except:
            time.sleep(1.5)
            self.ui.logfield.append('No Modem port found')
        self.ui.progressBar.setValue(100)
        return output

    async def dmodeinfo(self):

        self.ui.logfield.setStyleSheet("color: green;font-weight:bold")
        self.ui.logfield.setText('Reading info in download Mode\n')
        '''dmodethread = threading.Thread(target=detect.modem.downloadinfo(detect.modem),args=[None])
        dmodethread.start()
        self.dmodethread.start()'''
        dmo = asyncio.create_task(detect.modem.downloadinfo(detect.modem, self.ui.logfield))
        await dmo
        self.ui.logfield.append(dmo.result())
        print(dmo.result())

    def dmodeasync(self):
        t1 = asyncio.run(self.dmodeinfo())

    def loghandler(self, result):
        response = ''
        for otp in result:
            for data in otp:
                response += f'{data}\n'
        self.ui.logfield.append(response)
        self.ui.logfield.repaint()

    def open_backup(self):
        fiel, _ = QtWidgets.QFileDialog.getOpenFileName(filter="files (*.img *.bin *.tdf *.tar *.* .*7z *.zip *.pit)",
                                                        initialFilter='.tdf')
        return fiel

    def readqlmsec(self):
        response = ''
        response += 'reading qualcom security'
        print('reading qlm device')
        cmd = backuping.qlmbackup(BackUP, self.save_backup(), ['efs', 'sec_efs'])
        for outp in cmd:
            response += ''.join(outp)
        self.ui.logfield.append(response)
        self.ui.logfield.repaint()

        return response

    def writeqlm(self):
        print('writing the qualcom backup')
        self.ui.logfield.append('Writing back qualcom security back up file ')
        bckupfile = self.open_backup()
        self.ui.logfield.append(f'Using backup {bckupfile}')
        " asyncio.run(detect.BackUP.qlmrestore(BackUP,bckupfile))"
        self.write_backup = write_backup(bckupfile, self.ui.logfield, 'qlm')
        self.write_backup.start()
        self.cpreader()

    def writemtkBackup(self):
        self.ui.logfield.setText("writing Mtk security Backup")
        bckupfile = self.open_backup()
        self.ui.logfield.append(f'Using {bckupfile}')
        self.write_backup = write_backup(bckupfile, self.ui.logfield, 'mtk')
        self.write_backup.run()

    # part for populating combo box
    async def detect_unplug(self):
        uplug = asyncio.create_task(self.portexistor())
        await uplug

        # Get list of all available serial ports

    async def serialloger(self):
        for prt in prtlist.comports():
            print(prt.manufacturer)
            return f'{prt.manufacturer}({prt.name})'

    async def portexistor(self):
        await self.serialloger()

    # asyncio.run(portactivator())
    def readexynosecurity(self):
        loging = ''
        backup = BackUP.ExynosPartBackup(BackUP, self.save_backup(), ['efs', 'sec_efs', 'cpefs'])
        # pulwy =BackUP.puller(BackUP,['efs', 'sec_efs', 'cpefs'],backup[2])
        ziper = BackUP.zipper(BackUP, backup[2], backup[3])
        for output in backup, ziper:
            loging += ''.join(map(str, output))

        self.ui.logfield.append(loging)
        self.ui.logfield.repaint()

    # serial = asyncio.create_task(self.serialloger())
    # await serial

    # asyncio.run(self.serialloger())
    def exynosbb(self):
        self.baseband = baseband('efs', self.ui.logfield)
        self.baseband.start()
        self.ui.logfield.repaint()

    def exynoswrtefs(self):
        loging = ''
        backup_file = BackUP.exynosrestore(BackUP, self.open_backup(), 'efs')
        rst = BackUP.exynosrestore(BackUP, backup_file, 'efs')
        for outp in rst:
            loging += ''.join(outp)
        self.ui.logfield.append(loging)
        self.ui.logfield.repaint()

    def exynosRestor(self):
        print('restoring exynos backup')
        self.ui.logfield.repaint()
        self.ui.logfield.append('Restoring Exynos Backup')
        self.exywrite = exynos_write(self.ui.logfield, self.fileloader())
        self.exywrite.start()

    def samlog(self):
        bl_path = self.ui.blline.text()
        ap_path = self.ui.apline.text()
        cp_path = self.ui.cpline.text()
        user_path = self.ui.userdataline.text()
        csc_path = self.ui.cscline.text()
        samsung_flashingcmmd = ''
        samsung_dict = {bl_path: '-b', ap_path: '-a',
                        cp_path: '-c', user_path: '-u', csc_path: '-s'}

        if bl_path:
            samsung_flashingcmmd += fr'{samsung_dict.get(bl_path)} "{bl_path}" '
        if ap_path:
            samsung_flashingcmmd += fr'{samsung_dict.get(ap_path)} "{ap_path}" '
        if cp_path:
            samsung_flashingcmmd += fr'{samsung_dict.get(cp_path)} "{cp_path}" '
        if user_path:
            samsung_flashingcmmd += fr'{samsung_dict.get(user_path)} "{user_path}" '
        if csc_path:
            samsung_flashingcmmd += fr'{samsung_dict.get(csc_path)} "{csc_path}" '

        try:
            if not self.samthread.isRunning():
                # Pass self.part_file as an argument to the thread
                self.samthread.set_part_file(samsung_flashingcmmd)
                self.samthread.start()
        except Exception as e:
            print(f"An error occurred: {e}")
            self.ui.logfield.setText('Error while flashing \n make sure the device is connected in download mode'
                                     '\n make sure you have Samsung drivers installed')

    def update_text_area(self, line):
        self.ui.logfield.append(line)

    def readpit(self):
        self.ui.logfield.setText('Fixing odin Error')
        read_pit = asyncio.run(readpit())
        self.ui.logfield.setStyleSheet("color: green")
        self.ui.logfield.setText(read_pit)

    # fastboot session started here
    # after u create the async funtion then go ahead and create the runner
    async def runfboot(self):
        self.ui.logfield_3.append("waiting for fastboot device")
        self.ui.progressBar.setValue(0)

        # t1 = asyncio.create_task(fastboot.fbb.fastbootinfo(self.ui.logfield_3))
        try:
            t2 = asyncio.create_task(fastboot.fbb.fastbootinfo
                                 (self.ui.logfield_3), )
            await t2
        except:
            self.ui.logfield.append('Device Not connected ')
    def fastbooinfo(self):

        asyncio.run(self.runfboot())
        self.ui.progressBar.setValue(100)

    def fb_unlocking(self):
        self.ui.progressBar.setValue(10)
        thh = threading.Thread(target=fastboot.usb_monitor, args=(self.ui.logfield_3
                                                                  ,
                                                                  fastboot.fbb.bootloadr_unlocker(self.ui.logfield_3)))

    def fbloader(self):
        firmware = QtWidgets.QFileDialog.getOpenFileName(caption='Load Firmware File '
                                                         )
        self.ui.fbfirmware.setText(firmware[0])
        self.ui.fbfirmware.repaint()
        fb_var = fastboot.ext_parser(firmware, self.ui.fblistwidget)
        self.ui.fblistwidget.setStyleSheet('color:white;background-color:black;'
                                           'font-size:8pt'
                                           ';font-weight:bold')
        for i in fb_var:
            if i.startswith('tf'):
                self.ui.fblistwidget.append(
                    i.replace('tf', '') or
                    i.replace('tf', ''))
            elif i.startswith('fastboot'):
                self.ui.fblistwidget.append(i.replace('fastboot', ''))

            self.ui.fblistwidget.repaint()

        return fb_var

    def fbFlashing(self):
        pth = ''
        cmd = []
        flashfiles = []
        self.ui.logfield_3.setStyleSheet('color: green;'
                                         ' background-color: black;'
                                         'font-size: 8pt;'
                                         ' font-weight: bold; '
                                         )
        self.ui.logfield_3.append('waiting for fastboot')
        self.ui.progressBar.setValue(0)
        # problem is here
        li = self.ui.fblistwidget.toPlainText()
        fbpath = self.ui.fbfirmware
        filepath = fbpath.toPlainText()
        if filepath:
            dirname = os.path.dirname(filepath)
            # print(dirname)
            t12 = os.listdir(dirname)
            firmware_parser = fastboot.xmlreader(filepath, self.ui.fblistwidget)
            file_count = 0
            for part, file in firmware_parser.items():
                file_count += 1
                if file in t12:
                    filename = os.path.join(dirname, file)
                    print(f'fastboot flash {part} {file}')
                    fbb = fastboot.Fboot.setfile(self,part,file)

                else:
                    self.ui.logfield.setText('Fastboot flasher broken')

            self.ui.progressBar.setValue(100)
        else:
            self.ui.logfield_3.setStyleSheet('Firmware Link invalid ')
        split_li = li.split('\n')
        # print(flashfiles)
        ''' self.fastboot_flasher = fastboot_flasher("bootloader","C:\\Users\\DROID\\Desktop\\sargo-sp2a.220505.008\\bootloader-sargo-b4s4-0.4-8048689.img",
                                                 self.ui.logfield_3)
        self.fastboot_flasher.start()'''


# 06/02/2023 stopped lookign for fastboot ttesm to flash
# 09082023 stuck wth using diferent threads to execute the job


if __name__ == "__main__":
    app = QApplication([])
    main = MainDialog()
    main.show()
    app.exec()
