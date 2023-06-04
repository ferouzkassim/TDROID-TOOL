import time,threading
import serial
import serial.tools.list_ports as prtlist
import asyncio
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer, pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication, QDialog, QPushButton
import serial.tools.list_ports as prtlst
import detect
import gui
import samsungflasher
from samsungflasher import flasher
import usbcom
from detect import detector, BackUP, backuping
from gui import Ui_main


# import pyudev
# pyudev to monitor the behaviour of attathecd devices

class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)
        # cpu lists
        self.mtklist = ['Mtk General', 'SM-A013G', 'SM-A037F', 'SM-A125F', 'SM-A225F', ]
        self.exynolist = ['Exynos General', 'SM-A127F', 'SM-A217f', 'SM-A135F','SM-A047F']
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
        # self.ui.writeefs.clicked.connect(self.open_backup)
        if self.ui.modelselector.currentText() in self.exynolist:
            self.ui.Fixbaseband.clicked.connect(lambda:self.exynosbb)
            self.ui.Write_Efs.clicked.connect(lambda:self.exynoswrtefs)
            self.ui.Read_security.clicked.connect(lambda:self.readexynosecurity)
            #self.ui.Read_security.clicked.connect(self.)

        elif self.ui.modelselector.currentText() in self.mtklist:
            self.ui.Fixbaseband.clicked.connect(lambda :self.fixbbmtk)
            self.ui.Read_security.clicked.connect(lambda :[self.readmtk(),print('mtkread')])

        self.ui.modelselector.addItems(self.modelist)
        self.ui.comboBox.addItem(self.detect_unplug())

        self.ui.reset_frp.clicked.connect(self.resetfrp)
        # self.ui.qlmreadefs.clicked.connect(self.readqlmsec)
        self.ui.flashsmsng.clicked.connect(self.samsung_flasher)
        self.ui.modelselector.activated.connect(self.modelselector)
        self.ui.blcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.blline, self.fileloader()))
        self.ui.apcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.apline, self.fileloader()))
        self.ui.cpcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.cpline, self.fileloader()))
        self.ui.csccheckbox.clicked.connect(lambda: self.loadedfile(self.ui.cscline, self.fileloader()))
        self.ui.userdtacheckbox.clicked.connect(lambda: self.loadedfile(self.ui.userdataline, self.fileloader()))
        self.ui.pitcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.pitline, self.fileloader()))

    def logthread(self,loge):
        self.ui.logfield.append(loge)

    def resetfrp(self):
        logging = ''
        usbcom.enableADB()
        detect.detc.adbfrpreset(detect.detc)
        '''for log in detect.detc.adbfrpreset(detect.detc):
            self.ui.logfield.append(log)'''
    def snrepair(self,):
        newsno=self.ui.snEdit.text()

        self.ui.progressBar.setValue(10)
        print(56)
        self.ui.progressBar.setValue(50)
        detect.repair.partrepair(detect.repair,f'serial_no',self.ui.snEdit.text())
        self.ui.progressBar.setValue(100)

    def bootfix(self):
        detect.boot.bootfixer(detect.boot)
    def save_backup(self):
        file, _ = QtWidgets.QFileDialog.getSaveFileName(
            filter=("files (*.img *.bin *.tdf *.tar)"), initialFilter=('*.tdf')
        )
        return file
    def fileloader(self):
        fiel, _ = QtWidgets.QFileDialog.getOpenFileName(filter="files (*.pit *.md5 *.tar *.zip)",
                                                        initialFilter='.tar')
        print(fiel)
        return fiel

    def loadedfile(self, part, fiel):
        fileloaded = part.setText(fiel)
        return fileloaded,fiel

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
        loging =''
        back = backuping.mtkPartBackup(BackUP, ['nvdata', 'nvram', 'protect1', 'protect2'])
        self.ui.progressBar.setValue(25)
        pull = backuping.puller(BackUP,back[0],self.save_backup())
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

    def read_info_adb(self):
        # Call adbConnect function
        output_list = []
        for output in BackUP.adbConnect(BackUP):
            output_list.append(output)
        # Append entire output to logfield
        #log = threading.Thread(concut,args=('hte logfield'))
        #log.start()
        self.ui.logfield.append(f'logging for {self.ui.modelselector.currentText()}\n')
        self.ui.logfield.append(''.join(output_list))
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
        response = ''
        response += 'Reading info in download Mode\n'
        for otp in detect.modem.downloadinfo(detect.modem):
            for data in otp:
             response+=f'{data}\n'
        self.ui.logfield.append(response)
        self.ui.logfield.repaint()
    def read_dv(self):
      restr=''
      cmd=detect.mode.downloadinfo(detect.mode)
      for otp in cmd:
          restr+=otp
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
    def detect_unplug(self):
        ports = prtlst.comports()
        # Get list of all available serial ports
        while prtlst.comports():
            for prt in prtlst.comports():
                print(prt.hwid)
            return f'{prt.manufacturer}({prt.name})'





    #asyncio.run(portactivator())
    def readexynosecurity(self):
        loging = ''
        backup = BackUP.ExynosPartBackup(BackUP, self.save_backup(), ['efs', 'sec_efs', 'cpefs'])
        #pulwy =BackUP.puller(BackUP,['efs', 'sec_efs', 'cpefs'],backup[2])
        ziper = BackUP.zipper(BackUP,backup[2],backup[3])
        for output in backup, ziper:
            loging += ''.join(map(str, output))

        self.ui.logfield.append(loging)
        self.ui.logfield.repaint()

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
        backuping.exynosrestore(BackUP,self.fileloader())
    def samsung_flasher(self):
        bl = self.ui.blline.text()
        ap = self.ui.apline.text()
        cp = self.ui.cpline.text()
        csc = self.ui.cscline.text()
        userdata = self.ui.userdataline.text()
        firmware = {
            bl: "-b",
            ap: "-a",
            cp: "-c",
            csc: "-s",
            userdata: "-u"
        }
        for file,prt in firmware.items():
            sam = samsungflasher.run_flasher(part=prt, file=file)
            self.logthread(sam)
            return





if __name__ == "__main__":
    app = QApplication([])
    main = MainDialog()
    main.show()
    app.exec()
