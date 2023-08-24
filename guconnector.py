import asyncio
import os.path
import threading
import time
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
#samsung flashing log thread
class LogEmitter(QObject):
    logReady = pyqtSignal(str)

class SamsungFlasherThread(QThread):
    def __init__(self, prt, nme,lf,pbar):
        super().__init__()
        self.lf = lf
        self.part = prt
        self.nme = nme
        self.pbar = pbar
    def run(self):
        emitter = LogEmitter()
        #emitter.logReady.connect(self.logToGUI)
        asyncio.run(samsungflasher.run_flashpart(self.part, self.nme, self.lf,self.pbar))
class fastboot_flasher(QThread):
    def __init__(self,part,file,widget):
        super().__init__()
        self.part=part
        self.file = file
        self.widget = widget

    def run(self):
        asyncio.run(fastboot.usb_monitor(fastboot.fbb.fbtflasher(self.part,self.file,self.widget)))



class MainDialog(QDialog):
    def __init__(self):
        self.fastboot_flasher = None
        self.draftli = []
        super().__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)
        # threading download mode slotsss
        """self.dmodethread = Dmode()
        self.dmodethread.resultReady.connect(self.loghandler)
        self.dmodethread.updateProgress.connect(self.updateProgressBar)"""
        #self.samsung_thread = SamsungFlasherThread(self.ui.blline.text(), self.ui.logfield)
        # Connect to the slot method
        self.mtklist = ['Mtk General', 'SM-A013G', 'SM-A037F', 'SM-A125F', 'SM-A225F', ]
        self.exynolist = ['Exynos General', 'SM-A127F', 'SM-A217f', 'SM-A135F', 'SM-A047F']
        self.qlmlist = ['SM-A235F']
        self.qlmlist.sort()
        self.exynolist.sort()
        self.mtklist.sort()
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
            # self.ui.Read_security.clicked.connect(self.)

        elif self.ui.modelselector.currentText() in self.mtklist:
            self.ui.Fixbaseband.clicked.connect(lambda: self.fixbbmtk)
            self.ui.Read_security.clicked.connect(lambda: [self.readmtk(), print('mtkread')])
        else :
            self.ui.modelselector.currentText() in self.qlmlist
            self.ui.write_security.clicked.connect(lambda:self.writeqlm())

        self.ui.modelselector.addItems(self.modelist)
        self.ui.comboBox.addItem(asyncio.run(self.detect_unplug()))

        self.ui.reset_frp.clicked.connect(self.resetfrp)
        # self.ui.qlmreadefs.clicked.connect(self.readqlmsec)
        self.ui.flashsmsng.clicked.connect(self.samlog)
        self.ui.modelselector.activated.connect(self.modelselector)
        self.ui.fixdload.clicked.connect(self.readpit)
        self.ui.blcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.blline, self.fileloader()))
        self.ui.apcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.apline, self.fileloader()))
        self.ui.cpcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.cpline, self.fileloader()))
        self.ui.csccheckbox.clicked.connect(lambda: self.loadedfile(self.ui.cscline, self.fileloader()))
        self.ui.userdtacheckbox.clicked.connect(lambda: self.loadedfile(self.ui.userdataline, self.fileloader()))
        self.ui.pitcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.pitline, self.fileloader()))
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
        self.ui.progressBar.setValue(50)
        detect.repair.partrepair(detect.repair, f'serial_no', self.ui.snEdit.text())
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
        print(fiel)
        return fiel

    def loadedfile(self, part, fiel):
        fileloaded = part.setText(fiel)
        return fileloaded, fiel

    def modelselector(self):
        model = self.ui.modelselector.currentText()
        self.ui.Fixbaseband.disconnect()  # remove any previous connections
        if model in self.mtklist:
            self.ui.Read_security.setText('Read Nv')
            self.ui.write_security.setText('Write Nv')
            self.ui.Read_security.clicked.connect(lambda: self.readmtk())
            self.ui.Fixbaseband.clicked.connect(self.fixbbmtk)
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
        loging = ''
        print('mtking')
        exnos = BackUP.part_mountmtk(BackUP, 'efs')
        for outp in exnos:
            loging += ''.join(outp)
        self.ui.logfield.append(loging)
        self.ui.logfield.repaint()

    def read_info_adb(self, Rres):
        # Call adbConnect function
        self.ui.progressBar.setValue(0)
        self.ui.logfield.setText(f'logging for {self.ui.modelselector.currentText()}\n')
        self.ui.progressBar.setValue(50)
        t2 = asyncio.run(detect.detc.adbConnect(detect, self.ui.logfield))
        self.ui.logfield.repaint()
        self.ui.progressBar.setValue(100)

    def cpreader(self):
        self.ui.logfield.append('reading in MTP Mode')
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

        for ifn in info:
            for dat in ifn:
                fida = dat.replace('(', ':\t').replace(')', "").replace('AT+DEVCONINFO', '').replace('+DEVCONINFO',
                                                                                                     '').replace('#OK#',
                                                                                                                 '').replace(
                    'OK', '')
                fida.replace(')', "")
                for key, value in replace_dict.items():
                    fida = fida.replace(key, value)
                output += fida + "\n"
                self.ui.logfield.append(fida)
                self.ui.logfield.repaint()
        self.ui.progressBar.setValue(100)
        return output

    async def dmodeinfo(self):

        self.ui.logfield.setStyleSheet("color: green;font-weight:bold")
        self.ui.logfield.append('Reading info in download Mode\n')
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
        fiel, _ = QtWidgets.QFileDialog.getOpenFileName(filter="files (*.img *.bin *.tdf *.tar *.*)",
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
        asyncio.run(detect.BackUP.qlmrestore(BackUP,bckupfile))
        self.ui.logfield.append('Creating restoration folder')
        self.ui.logfield.append('Extracting to Folder')

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
        loging = ''
        exnos = BackUP.part_mountex(BackUP, 'efs')
        print('eewr')
        for outp in exnos:
            loging += ''.join(outp)
        self.ui.logfield.append(loging)
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
        backuping.exynosrestore(BackUP, self.fileloader())

    async def samsung_flasher(self):
        bl = self.ui.blline.text()
        """ap = self.ui.apline.text()
        cp = self.ui.cpline.text()
        csc = self.ui.cscline.text()
        userdata = self.ui.userdataline.text()"""
        firmware = {
            "-b ": bl,
        }
        sam = asyncio.run(samsungflasher.flashpart('-b', bl,))
        # Wait for the task to complete
        self.ui.logfield.append(bl)

    def samlog(self):

        bl = self.ui.blline.text()
        ap = self.ui.apline.text()
        cp = self.ui.cpline.text()
        csc = self.ui.cscline.text()
        userdata = self.ui.userdataline.text()
        firmware = {
            "-b ": bl,
            "-a":ap,
            "-c":cp,
            "-s":csc,
            "-u":userdata
        }
        for name,value in firmware.items():
            if value:
                print(f'{name} is flashng {value}')
        self.samsung_thread = SamsungFlasherThread("-b",bl, self.ui.logfield,self.ui.progressBar)
        self.samsung_thread.start()
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
        t2 = asyncio.create_task(fastboot.usb_monitor(fastboot.fbb.fastbootinfo
                                                      (self.ui.logfield_3),))
        await t2

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
        fb_var = fastboot.fbb.ext_parser(firmware)
        self.ui.fblistwidget.setStyleSheet('color:white;background-color:black;'
                                           'font-size:8pt'
                                           ';font-weight:bold')
        for i in fb_var:
            if i.startswith('tf'):
                self.ui.fblistwidget.append(
                    i.replace('tf', '') or
                    i.replace('tf', ''))
            elif i.startswith('fastboot'):
                self.ui.fblistwidget.append(i.replace('fastboot',''))

            self.ui.fblistwidget.repaint()

        return firmware


    def fbFlashing(self):
        pth = ''
        cmd=[]
        file=[]
        self.ui.logfield_3.setStyleSheet('color: green;'
                                         ' background-color: black;'
                                         'font-size: 8pt;'
                                         ' font-weight: bold; '
                                         )
        self.ui.logfield_3.append('waiting for fastboot')
        self.ui.progressBar.setValue(0)
        #problem is here
        li = self.ui.fblistwidget.toPlainText()
        fbpath = self.ui.fbfirmware
        filepath = fbpath.toPlainText().split()
        if filepath:
            path = os.path.dirname(filepath[0])
            print(path)
            pth+=path
        else:
            self.ui.logfield_3.setStyleSheet('Firmware Link invalid ')
        split_li=li.split('\n')
        print(split_li)
        for i in split_li:
            if i.startswith(' flash') or i.startswith(' -w'):
                print(i)
            else:
                print('no flashing found')


        self.fastboot_flasher = fastboot_flasher("bootloader","C:\\Users\\DROID\\Desktop\\sargo-sp2a.220505.008\\bootloader-sargo-b4s4-0.4-8048689.img",self.ui.logfield_3)
        self.fastboot_flasher.start()

#06/02/2023 stopped lookign for fastboot ttesm to flash
#09082023 stuck wth using diferent threads to execute the job


if __name__ == "__main__":
    app = QApplication([])
    main = MainDialog()
    main.show()
    app.exec()
