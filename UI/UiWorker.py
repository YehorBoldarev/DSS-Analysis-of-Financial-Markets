from PyQt6.QtCore import QObject, pyqtSignal, QRunnable


class WorkerSignals(QObject):
    set_enabled = pyqtSignal(bool)
    set_generate_report_show = pyqtSignal(bool)
    update_output = pyqtSignal(str)
    error_occurred = pyqtSignal(str)


class Worker(QRunnable):
    def __init__(self, func):
        super(Worker, self).__init__()
        self.functional = func
        self.signals = WorkerSignals()

    def run(self):
        try:
            self.functional()
        except Exception as e:
            self.signals.error_occurred.emit(f'Error: {e}')
