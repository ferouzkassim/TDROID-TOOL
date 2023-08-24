class LogEmitter(QObject):
    logReady = pyqtSignal(str)


class SamsungFlasherThread(QThread):
    def run(self):
        # Perform the processing...
        log_message = "This is a log message from SamsungFlasherThread"
        emitter = LogEmitter()
        emitter.logReady.emit(log_message)

class MainDialog(QDialog):
    def __init__(self):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main()
        self.ui.setupUi(self)
        self.samsung_thread = SamsungFlasherThread()
        self.samsung_thread.start()
        self.samsung_thread.finished.connect(self.samsung_thread.deleteLater)
        self.samsung_thread.finished.connect(self.on_samsung_thread_finished)

    def on_samsung_thread_finished(self):
        self.ui.logfield.append("SamsungFlasherThread has finished.")

    @pyqtSlot(str)
    def update_logfield(self, log_message):
        self.ui.logfield.append(log_message)

        # Inside the MainDialog class (where you instantiate SamsungFlasherThread):
        emitter = LogEmitter()
        emitter.logReady.connect(self.update_logfield)
