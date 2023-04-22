import time,threading

import serial
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton
import serial.tools.list_ports as prtlst
from PyQt6.QtSerialPort import QSerialPortInfo

import detect
from samsungflasher import flasher
import usbcom
from detect import adbConnect, detector, BackUP, backuping
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
        self.exynolist = ['Exynos General', 'SM-A127F', 'SM-A217f', 'SM-A135F']
        self.qlmlist = ['SM-A235F']
        self.qlmlist.sort()
        self.exynolist.sort()
        self.mtklist.sort()
        self.modelist = sorted(self.mtklist + self.exynolist + self.qlmlist)
        # Connect button click signal to function
        self.ui.Read_info_adb.clicked.connect(self.read_info_adb)
        self.ui.Read_info_cp.clicked.connect(self.cpreader)
        self.ui.readd.clicked.connect(self.dmodeinfo)
        self.ui.Read_Efs.clicked.connect(self.readexynosecurity)
        # self.ui.writeefs.clicked.connect(self.open_backup)
        if self.ui.Read_security.text() == 'Read Nv' and self.ui.modelselector.currentText() in self.mtklist:
            self.ui.Read_security.clicked.connect(lambda :self.readmtk())
        if self.ui.modelselector.currentText() in self.exynolist:
            self.ui.Fixbaseband.clicked.connect(lambda:self.exynosbb())

        elif self.ui.modelselector.currentText() in self.mtklist:
            self.ui.Fixbaseband.clicked.connect(lambda:[self.fixbbmtk()])
            self.ui.Read_security.clicked.connect(lambda :[self.readmtk(),print('mtkread')])
        self.ui.Write_Efs.clicked.connect(self.exynoswrtefs)
        self.ui.modelselector.addItems(self.modelist)
        self.ui.comboBox.addItem(self.detect_unplug())
        self.ui.reset_frp.clicked.connect(self.resetfrp)
        # self.ui.qlmreadefs.clicked.connect(self.readqlmsec)
        self.ui.modelselector.activated.connect(self.modelselector)
        '''self.ui.blcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.blline, self.fileloader()))
        self.ui.apcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.apline, self.fileloader()))
        self.ui.cpcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.cpline, self.fileloader()))
        self.ui.csccheckbox.clicked.connect(lambda: self.loadedfile(self.ui.cscline, self.fileloader()))
        self.ui.userdtacheckbox.clicked.connect(lambda: self.loadedfile(self.ui.userdataline, self.fileloader()))
        self.ui.pitcheckbox.clicked.connect(lambda: self.loadedfile(self.ui.pitline, self.fileloader()))'''

    def resetfrp(self):
        logging = ''
        usbcom.enableADB()
        detect.detc.adbfrpreset(detect.detc)
        '''for log in detect.detc.adbfrpreset(detect.detc):
            self.ui.logfield.append(log)'''

    def save_backup(self):
        file, _ = QtWidgets.QFileDialog.getSaveFileName(
            filter=("files (*.img *.bin *.tdf *.tar)"), initialFilter=('*.tdf')
        )
        return file
    def fileloader(self):
        fiel, _ = QtWidgets.QFileDialog.getOpenFileName(filter="files (*.pit *.md5 *.tar)",
                                                        initialFilter='.tar')
        print(fiel)
        return fiel

    def loadedfile(self, part, fiel):
        fileloaded = part.setText(fiel)
        return fileloaded

    def modelselector(self):
        model = self.ui.modelselector.currentText()
        if model in self.mtklist:
            self.ui.Read_security.setText('Read Nv')
            self.ui.write_security.setText('Write Nv')
            self.ui.Read_security.clicked.connect(lambda: self.readmtk())
            self.ui.Fixbaseband.clicked.connect(self.fixbbmtk)
            if not self.ui.MountNetwork.isVisible():
                self.ui.MountNetwork.show()

        if model in self.exynolist:
            self.ui.Read_security.setText('Read Security')
            self.ui.write_security.setText('Write Security')
            self.ui.MountNetwork.hide()
        if model in self.qlmlist:
            self.ui.MountNetwork.hide()

    def readmtk(self):
        print('reading mtk')
        loging =''
        back = backuping.mtkPartBackup(BackUP, ['nvdata', 'nvram', 'protect1', 'protect2'])
        pull = backuping.puller(BackUP,back[0],self.save_backup())
        ziper = BackUP.zipper(BackUP, pull[1])
        for output in back, ziper:
            loging += ''.join(map(str, output))

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
        for output in adbConnect():
            output_list.append(output)
        # Append entire output to logfield
        self.ui.logfield.append(f'logging for {self.ui.modelselector.currentText()}\n')
        self.ui.logfield.append(''.join(output_list))
        self.ui.logfield.repaint()

    def cpreader(self):
        output = ''
        replace_dict = {"MN:": "MODEL:\t",
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
        info = detect.mode.Readmodem(detect.mode, detect.mode.samport(detect.mode))
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
        for otp in detect.mode.downloadinfo(detect.mode):
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
        # Get list of all available serial ports
        ports = prtlst.comports()
        for port in ports:
            # Check if the device is connected;
            if serial.Serial(port.device).is_open:
                # Device is still connected
                print(port.description)
                connected = True
            else:
                # Device has been unplugged
                connected = False
                # Call the update_serial_ports() function
                self.update_serial_ports()
    def update_serial_ports(self):
        # Clear existing items in the combo box
        self.ui.comboBox.clear()
        # Get list of all available serial ports
        ports = prtlst.comports()
        while ports:
            for port in ports:
                # add current devices to combo box
                self.ui.comboBox.addItem(port.description)
                # Add each port name to the combo box
            break

        time.sleep(1)


    def readexynosecurity(self):
        loging = ''
        backup = BackUP.ExynosPartBackup(BackUP, self.save_backup(), ['efs', 'sec_efs', 'cpefs'])
        ziper = BackUP.zipper(BackUP, backup[2])
        for output in backup, ziper:
            loging += ''.join(map(str, output))

        self.ui.logfield.append(loging)
        self.ui.logfield.repaint()

    def exynosbb(self):
        loging = ''
        exnos = BackUP.part_mountex(BackUP, 'efs')
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



if __name__ == "__main__":
    app = QApplication([])
    main = MainDialog()
    main.show()
    app.exec()
