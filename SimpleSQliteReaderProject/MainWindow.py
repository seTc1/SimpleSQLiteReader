from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
import sqlite3
import os
import shutil
from MainWindowUI import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from ExecuteSQLWindow import ExecuteSQLWindow

from PyQt6.uic.properties import QtGui


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_execute_sql.clicked.connect(self.open_sqlexecute_window)
        self.buttons_connection()
        self.executeSQlWindow = ExecuteSQLWindow()
        self.database_connection = None
        self.journaldb_name = None
        self.tableupdate_count = 1
        self.database_name = None
        self.saved_before_chancges = True

    def buttons_connection(self):
        self.btn_open_database.clicked.connect(self.open_database)
        self.combobox_chose_window.currentIndexChanged.connect(self.load_table)
        self.btn_update_table.clicked.connect(self.load_table)
        self.btn_create_database.clicked.connect(self.create_database)
        self.btn_save_bd.clicked.connect(self.save_database)

    def open_sqlexecute_window(self):
        self.executeSQlWindow.show()

    def open_database(self):
        self.database_name = self.lineEdit_database_name.text()
        if not self.database_name:
            self.statusBar().showMessage("Ошибка, не указано название файла!")
            return
        elif not self.database_name.endswith((".db", ".sqlite3", ".sqlite", ".db3")):
            self.statusBar().showMessage("Ошибка, неверное расширение файла!")
            return

        if self.database_connection:
            self.database_connection.close()

        if not os.path.exists(self.database_name):
            self.statusBar().showMessage("Ошибка, файл базы данных не существует!")
            return

        self.journaldb_name = f"JOURNAL_{self.database_name}"
        shutil.copy(self.database_name, self.journaldb_name)
        self.database_connection = sqlite3.connect(self.journaldb_name)

        self.load_table_names()
        self.load_table()
        self.statusBar().showMessage(f"База данных {self.database_name} успешно открыта!")
        self.tableupdate_count = 1

    def create_database(self):
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
        self.statusBar().showMessage(f"Пустая база данных успешно создана!")
        self.tableupdate_count = 1

    def save_database(self):
        os.remove(self.database_name)
        self.database_connection.close()
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Указываем начало имени файла
        prefix = 'JOURNAL_'

        # Проходим по файлам в директории
        for filename in os.listdir(current_directory):
            if filename.startswith(prefix):
                old_path = os.path.join(current_directory, filename)
                new_filename = self.database_name
                new_path = os.path.join(current_directory, new_filename)
                os.rename(old_path, new_path)
                break

        self.unload_table()

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

        if self.tableupdate_count == 1:
            self.statusBar().showMessage(f"Таблица обновилась")
            self.tableupdate_count += 1
        else:
            self.statusBar().showMessage(f"Таблица обновилась x{self.tableupdate_count}")
            self.tableupdate_count += 1

    def unload_table(self):
        self.tableWidget_database_content.setRowCount(0)
        self.tableWidget_database_content.setColumnCount(0)
        self.combobox_chose_window.clear()
        self.lineEdit_database_name.clear()

    def closeEvent(self, event):
        if not self.saved_before_chancges:
            quit_msg = "Внимание, все несохранённые данные будут утеряны!"
            reply = QMessageBox.question(self, 'Вы уверенны что хотите закрыть программу?', quit_msg,
                                         QMessageBox.StandardButton.Yes,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.database_connection.close()
                current_directory = os.path.dirname(os.path.abspath(__file__))
                prefix = 'JOURNAL_'
                for filename in os.listdir(current_directory):
                    if filename.startswith(prefix):
                        file_path = os.path.join(current_directory, filename)
                        os.remove(file_path)
                event.accept()
            else:
                event.ignore()
