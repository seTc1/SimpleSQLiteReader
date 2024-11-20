from ExecutesSQLWindowUI import Ui_ExecuteSQL
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
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

    def load_data(self, data, columns):
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(columns))
        self.table_widget.setHorizontalHeaderLabels(columns)

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
