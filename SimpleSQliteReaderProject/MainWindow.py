from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
import sqlite3
from MainWindowUI import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from ExecuteSQLWindow import ExecuteSQLWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_execute_sql.clicked.connect(self.open_sqlexecute_window)
        self.buttons_connection()
        self.executeSQlWindow = ExecuteSQLWindow()
        self.database_connection = None
        self.model = None

    def buttons_connection(self):
        self.btn_open_database.clicked.connect(self.open_database)
        self.combobox_chose_window.currentIndexChanged.connect(self.load_table)

    def open_sqlexecute_window(self):
        self.executeSQlWindow.show()

    def open_database(self):
        database_name = self.lineEdit_database_name.text()
        if not database_name:
            self.statusBar().showMessage("Ошибка, не указано название файла!")
            return
        elif not database_name.endswith((".db", ".sqlite3", ".sqlite", ".db3")):
            self.statusBar().showMessage("Ошибка, неверное расширение файла!")
            return

        if self.database_connection:
            self.database_connection.close()

        self.database_connection = sqlite3.connect(database_name)

        self.load_table_names() 
        self.load_table()
        self.statusBar().showMessage(f"База данных {database_name} успешно открыта!")

    def load_table_names(self):
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        self.combobox_chose_window.clear()
        for table in tables:
            self.combobox_chose_window.addItem(table[0])

    def load_table(self):
        table_name = self.combobox_chose_window.currentText()
        if not table_name:
            return

        cursor = self.database_connection.cursor()
        sql_query = f"SELECT * FROM {table_name}"
        result = cursor.execute(sql_query).fetchall()

        self.tableWidget_database_content.setRowCount(len(result))
        self.tableWidget_database_content.setColumnCount(len(cursor.description))

        headers = [description[0] for description in cursor.description]
        self.tableWidget_database_content.setHorizontalHeaderLabels(headers)

        for row_idx, row in enumerate(result):
            for col_idx, value in enumerate(row):
                self.tableWidget_database_content.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

