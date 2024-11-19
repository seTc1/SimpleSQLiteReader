from PyQt6.QtWidgets import QMessageBox
import sqlite3
import os
import shutil
from MainWindowUI import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from ExecuteSQLWindow import ExecuteSQLWindow


# Класс главного окна приложения
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Инициализация интерфейса из UI-файла
        self.buttons_connection()  # Подключение других кнопок
        self.executeSQlWindow = ExecuteSQLWindow()  # Создание экземпляра окна выполнения SQL
        self.database_connection = None  # Текущая активная база данных
        self.journaldb_name = None  # Журнал изменений для базы данных
        self.tableupdate_count = 1  # Счётчик обновлений таблицы
        self.database_name = None  # Имя текущей базы данных
        self.saved_before_changes = True  # Флаг сохранения данных перед изменениями

    # Метод для подключения сигналов к кнопкам
    def buttons_connection(self):
        self.btn_execute_sql.clicked.connect(self.open_sqlexecute_window)  # Подключение кнопки для окна выполнения SQL
        self.btn_open_database.clicked.connect(self.open_database)  # Открытие базы данных
        self.combobox_chose_window.currentIndexChanged.connect(self.load_table)  # Загрузка таблицы при выборе из списка
        self.btn_update_table.clicked.connect(self.update_table)  # Обновление данных таблицы
        self.btn_create_database.clicked.connect(self.create_database)  # Создание новой базы данных
        self.btn_save_bd.clicked.connect(self.save_database)  # Сохранение базы данных

    # Метод для открытия окна выполнения SQL-запросов
    def open_sqlexecute_window(self):
        self.executeSQlWindow.show()

    # Метод для открытия существующей базы данных
    def open_database(self):
        self.unloadTable()

        self.database_name = self.lineEdit_database_name.text()  # Получение имени базы данных из текстового поля
        if not self.database_name:  # Проверка, указано ли имя базы данных
            self.statusBar().showMessage("Ошибка, не указано название файла!")
            return
        elif not self.database_name.endswith((".db", ".sqlite3", ".sqlite", ".db3")):  # Проверка расширения файла
            self.statusBar().showMessage("Ошибка, неверное расширение файла!")
            return

        if not os.path.exists(self.database_name):  # Проверка, существует ли файл базы данных
            self.statusBar().showMessage("Ошибка, файл базы данных не существует!")
            return

        self.create_and_connect_journal()

        self.statusBar().showMessage(f"База данных {self.database_name} успешно открыта!")

    # Метод для создания новой базы данных
    def create_database(self):


        self.database_name = self.lineEdit_database_name.text()
        if not self.database_name:
            self.statusBar().showMessage("Ошибка, не указано название файла!")
            return
        elif not self.database_name.endswith((".db", ".sqlite3", ".sqlite", ".db3")):
            self.statusBar().showMessage("Ошибка, неверное расширение файла!")
            return

        if os.path.exists(self.database_name):  # Проверка на существование файла
            self.statusBar().showMessage("Ошибка, файл с таким названием уже существует!")
            return

        self.database_connection = sqlite3.connect(self.database_name)  # Создание новой базы данных
        self.create_and_connect_journal()
        open()
        self.statusBar().showMessage(f"Пустая база данных успешно создана!")

    def create_and_connect_journal(self):
        if self.database_connection:
            self.database_connection.close()
        self.journaldb_name = f"JOURNAL_{self.database_name}"  # Создание резервной копии базы данных
        shutil.copy(self.database_name, self.journaldb_name)
        self.database_connection = sqlite3.connect(self.journaldb_name)  # Подключение к базе данных через журнал
        self.load_table_names()  # Загрузка списка таблиц
        self.load_table()  # Загрузка первой таблицы

    # Метод для сохранения изменений в базе данных
    def save_database(self):
        os.remove(self.database_name)  # Удаление старой базы данных
        self.database_connection.close()  # Закрытие соединения
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Поиск и переименование резервной копии
        prefix = 'JOURNAL_'
        for filename in os.listdir(current_directory):
            if filename.startswith(prefix):
                old_path = os.path.join(current_directory, filename)
                new_filename = self.database_name
                new_path = os.path.join(current_directory, new_filename)
                os.rename(old_path, new_path)
                break

        self.update_table()

    # Метод для загрузки списка таблиц из базы данных
    def load_table_names(self):
        cursor = self.database_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        self.combobox_chose_window.clear()  # Очистка списка
        for table in tables:
            self.combobox_chose_window.addItem(table[0])  # Добавление имени таблицы в выпадающий список

    # Метод для загрузки содержимого таблицы
    def load_table(self):
        table_name = self.combobox_chose_window.currentText()  # Получение имени текущей таблицы
        if not table_name:
            return

        cursor = self.database_connection.cursor()
        sql_query = f"SELECT * FROM {table_name}"  # Выполнение запроса
        result = cursor.execute(sql_query).fetchall()

        self.tableWidget_database_content.setRowCount(len(result))  # Установка количества строк
        self.tableWidget_database_content.setColumnCount(len(cursor.description))  # Установка количества столбцов

        headers = [description[0] for description in cursor.description]
        self.tableWidget_database_content.setHorizontalHeaderLabels(headers)  # Установка заголовков столбцов

        # Заполнение таблицы данными
        for row_idx, row in enumerate(result):
            for col_idx, value in enumerate(row):
                self.tableWidget_database_content.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        # Обновление сообщения в статусной строке
        if self.tableupdate_count == 1:
            self.statusBar().showMessage(f"Таблица загрузилась")
            self.tableupdate_count += 1
        else:
            self.statusBar().showMessage(f"Таблица загрузилась x{self.tableupdate_count}")
            self.tableupdate_count += 1

    # Метод для обновления данных таблицы
    def update_table(self):
        if not self.saved_before_changes:  # Проверка, сохранены ли данные
            quit_msg = "Внимание, все несохранённые данные будут утеряны!"
            reply = QMessageBox.question(self, f'Вы уверенны что хотите обновить таблицу {self.database_name}?',
                                         quit_msg,
                                         QMessageBox.StandardButton.Yes,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return

        if not self.database_connection:
            return

        self.deleteUnsavedTable()  # Удаление несохранённых данных

        self.tableWidget_database_content.setRowCount(0)
        self.tableWidget_database_content.setColumnCount(0)
        self.combobox_chose_window.clear()
        self.saved_before_changes = True
        self.tableupdate_count = 1

        self.create_and_connect_journal()

        self.statusBar().showMessage(f"Таблица обновилась")

    # Метод для очистки интерфейса
    def unloadTable(self):
        print("unloadTable")
        if self.database_connection:
            self.tableWidget_database_content.setRowCount(0)
            self.tableWidget_database_content.setColumnCount(0)
            self.combobox_chose_window.clear()
            self.lineEdit_database_name.clear()
            self.database_connection.close()
        self.database_connection = None  # Текущая активная база данных
        self.journaldb_name = None  # Журнал изменений для базы данных
        self.database_name = None  # Имя текущей базы данных
        self.saved_before_changes = True  # Флаг сохранения данных перед изменениями
        self.tableupdate_count = 1  # Счётчик обновлений таблицы

    # Метод для обработки закрытия окна
    def closeEvent(self, event):
        print("closeEvent")
        if not self.saved_before_changes:  # Проверка, сохранены ли данные
            quit_msg = "Внимание, все несохранённые данные будут утеряны!"
            reply = QMessageBox.question(self, 'Вы уверенны что хотите закрыть программу?', quit_msg,
                                         QMessageBox.StandardButton.Yes,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                event.accept()
            else:
                event.ignore()
        self.deleteUnsavedTable()

    def deleteUnsavedTable(self):
        print("deleteUnsavedTable")
        if self.database_connection:
            self.database_connection.close()
        current_directory = os.path.dirname(os.path.abspath(__file__))
        prefix = 'JOURNAL_'
        for filename in os.listdir(current_directory):
            if filename.startswith(prefix):
                file_path = os.path.join(current_directory, filename)
                os.remove(file_path)
