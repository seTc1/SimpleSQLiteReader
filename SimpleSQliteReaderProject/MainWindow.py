from PyQt6.QtSql import QSqlDatabase

from MainWindowUI import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow
from ExecuteSQLWindow import ExecuteSQLWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_execute_sql.clicked.connect(self.open_sqlexecute_window)
        self.executeSQlWindow = ExecuteSQLWindow()
        self.database = None
        self.model = None


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

        if self.database:
            self.database.close()

        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName(database_name)

        if not self.database.open():
            self.statusBar().showMessage("Ошибка открытия базы данных!")
            return

        self.statusBar().showMessage(f"База данных {database_name} успешно открыта!")
        #self.populate_table_combobox()

