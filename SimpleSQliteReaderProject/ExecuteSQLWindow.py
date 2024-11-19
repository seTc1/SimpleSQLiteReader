from ExecutesSQLWindowUI import Ui_ExecuteSQL
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import pyqtSignal, QObject


class Comunicator(QObject):
    query = pyqtSignal(object)


class ExecuteSQLWindow(QMainWindow, Ui_ExecuteSQL):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_execute_query.clicked.connect(self.send_execution_query)
        self.comunicator = Comunicator()

    def send_execution_query(self):
        self.comunicator.query.emit(self.textEdit_sql_query.toPlainText())

    def get_execution_data(self, data_log):
        print(data_log)
        self.logs_data_output_text.insertPlainText(data_log)
