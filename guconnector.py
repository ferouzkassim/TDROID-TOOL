from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton

from detect import adbConnect, detector, BackUP, backuping
from gui import Ui_main


class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)

        # Connect button click signal to function
        self.ui.Read_info_adb.clicked.connect(self.read_info_adb)
        self.ui.readefs.clicked.connect(self.read_efs)
        self.ui.writeefs.clicked.connect(self.open_backup)

    def read_info_adb(self):
        # Call adbConnect function
        output_list = []
        for output in adbConnect():
            output_list.append(output)
        # Append entire output to logfield
        self.ui.logfield.append(''.join(output_list))
        self.ui.logfield.repaint()
    def save_backup(self):
        file,_ = QtWidgets.QFileDialog.getSaveFileName(
            filter=("files (*.img *.bin *.tdf *.tar)"),initialFilter=('*.tdf')
     )
        return file
    def open_backup(self):
        fiel,_ = QtWidgets.QFileDialog.getOpenFileName(filter="files (*.img *.bin *.tdf *.tar)",initialFilter='.tdf')
        print(fiel)
        return fiel

    def read_efs(self):
        loging = ''
        backup = BackUP.ExynosPartBackup(BackUP, self.save_backup(), ['efs', 'sec_efs', 'cpefs'])
        ziper = BackUP.zipper(BackUP, backup[2])
        for output in backup, ziper:
            loging += ''.join(map(str, output))

        self.ui.logfield.append(loging)
        self.ui.logfield.repaint()


if __name__ == "__main__":
    app = QApplication([])
    main = MainDialog()
    main.show()
    app.exec()
