from PyQt5.QtWidgets import QApplication, QDialog, QPushButton

from detect import adbConnect
from gui import Ui_main


class MainDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)

        # Connect button click signal to function
        self.ui.Read_info_adb.clicked.connect(self.read_info_adb)

    def read_info_adb(self):
        # Call adbConnect function
        output_list = []
        for output in adbConnect():
            output_list.append(output)
        # Append entire output to logfield
        self.ui.logfield.append(''.join(output_list))


if __name__ == "__main__":
    app = QApplication([])
    main = MainDialog()
    main.show()
    app.exec()
