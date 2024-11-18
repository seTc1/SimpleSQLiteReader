from ExecutesSQLWindowUI import Ui_ExecuteSQL
from PyQt6.QtWidgets import QMainWindow


class ExecuteSQLWindow(QMainWindow, Ui_ExecuteSQL):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_execute_query.clicked.connect(self.execute_query)

    def execute_query(self):
        pass
