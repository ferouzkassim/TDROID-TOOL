import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton
import serial.tools.list_ports as prtlst
from PyQt6.QtSerialPort import QSerialPortInfo

from detect import adbConnect, detector, BackUP, backuping
from gui import Ui_main
#import pyudev
#pyudev to monitor the behaviour of attathecd devices



class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)
        #cpu lists
        self.mtklist=['Mtk General','SM-A013G','SM-A037F','SM-A125F','SM-A225F',]
        self.exynolist=['Exynos General','SM-A127F','SM-A217f','SM-A135F']
        self.qlmlist=['SM-A235F']
        self.qlmlist.sort()
        self.exynolist.sort()
        self.mtklist.sort()
        self.modelist=sorted(self.mtklist+self.exynolist+self.qlmlist)
        # Connect button click signal to function
        self.ui.Read_info_adb.clicked.connect(self.read_info_adb)
        self.ui.Read_Efs.clicked.connect(self.readexynosecurity)
        #self.ui.writeefs.clicked.connect(self.open_backup)
        self.ui.Fixbaseband.clicked.connect(self.exynosbb)
        self.ui.Write_Efs.clicked.connect(self.exynoswrtefs)
        self.ui.modelselector.addItems(self.modelist)
        self.ui.comboBox.addItem(self.update_serial_ports())
        #self.ui.qlmreadefs.clicked.connect(self.readqlmsec)
        self.ui.modelselector.activated.connect(self.modelselector)

    def modelselector(self):
        model=self.ui.modelselector.currentText()
        if model in self.mtklist:
            self.ui.Read_security.setText('Read Nv')
            self.ui.write_security.setText('Write Nv')
            if not self.ui.MountNetwork.isVisible():
                self.ui.MountNetwork.show()

        if model in self.exynolist:
            self.ui.Read_security.setText('Read Security')
            self.ui.write_security.setText('Write Security')
            self.ui.MountNetwork.hide()
    def read_info_adb(self):
        # Call adbConnect function
        output_list = []
        for output in adbConnect():
            output_list.append(output)
        # Append entire output to logfield
        self.ui.logfield.append(f'logging for {self.ui.modelselector.currentText()}\n')
        self.ui.logfield.append(''.join(output_list))
        self.ui.logfield.repaint()
    def save_backup(self):
        file,_ = QtWidgets.QFileDialog.getSaveFileName(
            filter=("files (*.img *.bin *.tdf *.tar)"),initialFilter=('*.tdf')
     )
        return file
    def open_backup(self):
        fiel,_ = QtWidgets.QFileDialog.getOpenFileName(filter="files (*.img *.bin *.tdf *.tar *.*)",initialFilter='.tdf')
        return fiel
    def readqlmsec(self):
        response = ''
        response+='reading qualcom security'
        print('reading qlm device')
        cmd = backuping.qlmbackup(BackUP,self.save_backup(),['efs','sec_efs'])
        for outp in cmd:
            response += ''.join(outp)
        self.ui.logfield.append(response)
        self.ui.logfield.repaint()

        return response

    def update_serial_ports(self):
        # Clear existing items in the combo box
        self.ui.comboBox.clear()
        # Get list of all available serial ports
        ports = prtlst.comports()
        # add current devices to combo box
        # Add each port name to the combo box
        for port in ports:
            self.ui.comboBox.addItem(port.description)
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
        loging =''
        exnos=BackUP.part_mount(BackUP,'efs')
        for outp in exnos:

            loging+=''.join(outp)
        self.ui.logfield.append(loging)
        self.ui.logfield.repaint()

    def exynoswrtefs(self):
        loging = ''
        backup_file =BackUP.exynosrestore(BackUP,self.open_backup(),'efs')
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
