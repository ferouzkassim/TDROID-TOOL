import asyncio
import os
import threading
import time

import serial.tools.list_ports as prtlist
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QDialog

import detect
import fastboot
import samsungflasher
import usbcom
from detect import BackUP, backuping
from gui import Ui_main
from samsungflasher import readpit


# import pyudev
# pyudev to monitor the behaviour of attathecd devices
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


class Adb_thread(QThread):
    logresponse = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        adbfunc = detect.detect.adbConnect(detect.detect)[0]
        self.logresponse.emit(adbfunc)

class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)
        # threading download mode slotsss
        self.dmodethread = Dmode()
        self.dmodethread.resultReady.connect(self.loghandler)
        self.dmodethread.updateProgress.connect(self.updateProgressBar)
        # threading adb
        self.Adbthread = Adb_thread()
        self.Adbthread.logresponse.connect(self.Adb_handler)
        # fastboot uitk
        # cpu lists
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
        self.ui.readd.clicked.connect(self.dmodeinfo)
        self.ui.fixbootloader.clicked.connect(self.bootfix)
        self.ui.Readinfofb.clicked.connect(self.runFbootinfo)
        # self.ui.writeefs.clicked.connect(self.open_backup)
        if self.ui.modelselector.currentText() in self.exynolist:
            self.ui.Fixbaseband.clicked.connect(lambda: self.exynosbb)
            self.ui.Write_Efs.clicked.connect(lambda: self.exynoswrtefs)
            self.ui.Read_security.clicked.connect(lambda: self.readexynosecurity)
            # self.ui.Read_security.clicked.connect(self.)

        elif self.ui.modelselector.currentText() in self.mtklist:
            self.ui.Fixbaseband.clicked.connect(lambda: self.fixbbmtk)
            self.ui.Read_security.clicked.connect(lambda: [self.readmtk(), print('mtkread')])

        self.ui.modelselector.addItems(self.modelist)
        self.ui.comboBox.addItem(asyncio.run(self.detect_unplug()))

        self.ui.reset_frp.clicked.connect(self.resetfrp)
        # self.ui.qlmreadefs.clicked.connect(self.readqlmsec)
        self.ui.flashsmsng.clicked.connect(self.samsung_flasher)
        self.ui.modelselector.activated.connect(self.modelselector)
        self.ui.fixdload.clicked.connect(self.readpit)
        self.ui.blcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.blline, self.fileloader()))
        self.ui.apcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.apline, self.fileloader()))
        self.ui.cpcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.cpline, self.fileloader()))
        self.ui.csccheckbox.clicked.connect(lambda: self.loadedfile(self.ui.cscline, self.fileloader()))
        self.ui.userdtacheckbox.clicked.connect(lambda: self.loadedfile(self.ui.userdataline, self.fileloader()))
        self.ui.pitcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.pitline, self.fileloader()))
        self.ui.fbload.clicked.connect(lambda: self.fbloader())
    def updateProgressBar(self, value):
        self.ui.progressBar.setValue(value)

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
        self.ui.logfield.setStyleSheet('color:brown')
        self.Adbthread.start()
        self.ui.logfield.append(f'logging for {self.ui.modelselector.currentText()}\n')
        self.ui.logfield.repaint()

    def Adb_handler(self, res):
        response = ''
        time.sleep(0.5)
        for otp in res:
            response += otp

        self.ui.logfield.setText(response)
        self.ui.logfield.repaint()

    def cpreader(self):
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
                        "HVID:\t": "DATA TREE:\t"}
        self.ui.logfield.append('reading in MTP Mode')
        info = detect.modem.Readmodem(detect.modem, detect.modem.samport(detect.modem))
        if info == ['']:
            info
            info
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
        return output

    def dmodeinfo(self):

        self.ui.logfield.setStyleSheet("color: blue")
        self.ui.logfield.append('Reading info in download Mode\n')
        '''dmodethread = threading.Thread(target=detect.modem.downloadinfo(detect.modem),args=[None])
        dmodethread.start()'''
        self.dmodethread.start()

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

    def samsung_flasher(self):
        self.ui.logfield.setStyleSheet("color: purple")
        bl = self.ui.blline.text()
        ap = self.ui.apline.text()
        cp = self.ui.cpline.text()
        csc = self.ui.cscline.text()
        userdata = self.ui.userdataline.text()

        # Create a list of firmware parts
        firmlist = [bl, ap, cp, csc, userdata]

        # Remove empty spaces from firmware parts
        # firmlist = [part.replace(" ", "") for part in firmlist]

        # Define the firmware dictionary
        firmware = {
            bl: " -b ",
            ap: " -a ",
            cp: " -c ",
            csc: " -s ",
            userdata: " -u"
            # userdata: "-u"rea
        }

        for firmware_file, firmware_part in firmware.items():
            print(firmware_file)
            print(firmware_part)
            if firmware_file:
                print(os.curdir)
                # Create a thread to run flashpart
            flash_thread = threading.Thread(target=samsungflasher.flashpart,
                                            args=(firmware_part, firmware_file))
            flash_thread.start()

    def flash_and_set_text(self, part, file, logfield):
        text = samsungflasher.flashpart(part, file)
        self.ui.logfield.setText(logfield, text)

    def readpit(self):
        self.ui.logfield.setText('Fixing odin Error')
        read_pit = asyncio.run(readpit())
        self.ui.logfield.setStyleSheet("color: green")
        self.ui.logfield.setText(read_pit)

    # fastboot session started here
    #after u create the async funtion then go ahead and create the runner
    async def runFbootinfo(self):
        self.ui.progressBar.setValue(0)
        #fb = fastboot.fbb.Fbootinfo(self.ui.logfield_3)
        fbbinfo =asyncio.create_task(fastboot.usb_monitor(self.ui.logfield_3))
        asyncio.run(fbbinfo)
                #
        loop = asyncio.get_event_loop()

        loop.run_until_complete(asyncio.wait(fbbinfo))
        loop.close()
        self.ui.progressBar.setValue(100)
    def fbloader(self):
        firmware = QtWidgets.QFileDialog.getOpenFileName(caption='Load Firmware File ',
                                                         initialFilter='.yml',
                                                         )
        self.ui.fbfirmware.append(str(firmware))
        self.ui.fbfirmware.repaint()
        fb_var = fastboot.fbb.ext_parser(firmware)
        for i in fb_var:
            i.replace('','fastboot')
            self.ui.fblistWidget.addItem(i)
            self.ui.fblistWidget.setStyleSheet('color:white;background-color:black;font-size:10pt'
                                               ';font-weight:bold')
            self.ui.fblistWidget.repaint()

        return firmware


if __name__ == "__main__":
    app = QApplication([])
    main = MainDialog()
    main.show()
    app.exec()
