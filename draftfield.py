import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QFileDialog


class PathSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.path_line_edit = QLineEdit(self)
        layout.addWidget(self.path_line_edit)

        select_button = QPushButton('Select Path', self)
        select_button.clicked.connect(self.show_dialog)
        layout.addWidget(select_button)

        self.setLayout(layout)

    def show_dialog(self):
        file_dialog = QFileDialog()
        selected_path = file_dialog.getExistingDirectory(self, 'Select Directory')

        if selected_path:
            self.path_line_edit.setText(selected_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    path_selector = PathSelector()
    path_selector.show()
    sys.exit(app.exec_())
