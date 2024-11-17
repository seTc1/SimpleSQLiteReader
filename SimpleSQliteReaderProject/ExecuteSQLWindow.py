
from ExecutesSQLWindowUI import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow

class ExecuteSQLWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)