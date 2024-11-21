from PyQt6.QtWidgets import QMessageBox
import sqlite3
import os
import shutil
from MainWindowUI import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem
from ExecuteSQLWindow import ExecuteSQLWindow
from PyQt6.QtCore import pyqtSignal, QObject

class Comunicator(QObject):
    database_logs = pyqtSignal(object)
    table_and_logs = pyqtSignal(object, object, object)


# Класс главного окна приложения
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Инициализация интерфейса из UI-файла
        self.buttons_connection()  # Подключение других кнопок

        self.database_connection = None  # Текущая активная база данных
        self.journaldb_name = None  # Журнал изменений для базы данных
        self.database_name = None  # Имя текущей базы данных
        self.saved_before_changes = True  # Флаг сохранения данных перед изменениями

        self.comunticator = Comunicator()

        self.executeSQlWindow = ExecuteSQLWindow()  # Создание экземпляра окна выполнения SQL

        self.comunticator.database_logs.connect(self.executeSQlWindow.get_execution_data)
        self.comunticator.table_and_logs.connect(self.executeSQlWindow.load_data)

        self.executeSQlWindow.comunicator.query.connect(self.execute_query)

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
        if not self.database_connection:
            self.statusBar().showMessage(f"❌ Ошибка, нет базы данных")
            return
        self.executeSQlWindow.show()

    def execute_query(self, query):
        if not self.database_connection:
            self.statusBar().showMessage(f"❌ Ошибка, нет базы данных")
            return
        try:
            cursor = self.database_connection.cursor()
            if query.strip().lower().startswith("select"):
                result = cursor.execute(query).fetchall()
                columns = [description[0] for description in cursor.description]
                log_message = f"✅ Команда успешно выполнена. Затронуто данных: {len(result)}\n"
                self.comunticator.table_and_logs.emit(log_message, result, columns)
                self.saved_before_changes = False
                self.load_table_names()  # Загрузка списка таблиц
                self.load_table()  # Загрузка содержимого таблицы
            else:
                # Выполнение запросов изменения в основной базе данных

                cursor.execute(query)
                self.database_connection.commit()
                log_message = f"✅ Команда успешно выполнена.\n"
                self.comunticator.database_logs.emit(log_message)
                self.saved_before_changes = False
                self.load_table_names()  # Загрузка списка таблиц
                self.load_table()  # Загрузка содержимого таблицы
        except sqlite3.Error as e:
            log_message = f"❌ Ошибка при выполнении команды: {e}\n"
            self.comunticator.database_logs.emit(log_message)

    def send_query_logs(self, logs_data):
        if not self.database_connection:
            self.statusBar().showMessage(f"❌ Ошибка, нет базы данных")
            return
        self.comunticator.database_logs.emit(logs_data)

    # Метод для открытия существующей базы данных
    def open_database(self):
        if not self.saved_before_changes:  # Проверка, сохранены ли данные
            quit_msg = "Внимание, все несохранённые данные будут утеряны!"
            reply = QMessageBox.question(self, f'Вы уверенны что хотите открыть новую таблицу?',
                                         quit_msg,
                                         QMessageBox.StandardButton.Yes,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return

        if self.database_name == self.lineEdit_database_name.text():  # Проверка, совпадает ли имя открываемой базы данных с текущей
            self.statusBar().showMessage("❌ Ошибка, база данных уже открыта!")
            return
        if not self.lineEdit_database_name.text():  # Проверка, указано ли имя базы данных
            self.statusBar().showMessage("❌ Ошибка, не указано название файла!")
            return
        elif not self.lineEdit_database_name.text().endswith(
                (".db", ".sqlite3", ".sqlite", ".db3")):  # Проверка расширения файла
            self.statusBar().showMessage("❌ Ошибка, неверное расширение файла!")
            return

        if not os.path.exists(self.lineEdit_database_name.text()):  # Проверка, существует ли файл базы данных
            self.statusBar().showMessage("❌ Ошибка, файл базы данных не существует!")
            return

        self.unload_table()
        self.database_name = self.lineEdit_database_name.text()  # Получение имени базы данных из текстового поля

        self.create_and_connect_journal()

        self.statusBar().showMessage(f"✅ База данных {self.database_name} успешно открыта!")

    # Метод для создания новой базы данных
    def create_database(self):
        if not self.saved_before_changes:  # Проверка, сохранены ли данные
            quit_msg = "Внимание, все несохранённые данные будут утеряны!"
            reply = QMessageBox.question(self, f'Вы уверенны что хотите создать новую таблицу?',
                                         quit_msg,
                                         QMessageBox.StandardButton.Yes,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return

        self.database_name = self.lineEdit_database_name.text()
        if not self.database_name:
            self.statusBar().showMessage("❌ Ошибка, не указано название файла!")
            return
        elif not self.database_name.endswith((".db", ".sqlite3", ".sqlite", ".db3")):
            self.statusBar().showMessage("❌ Ошибка, неверное расширение файла!")
            return

        if os.path.exists(self.database_name):  # Проверка на существование файла
            self.statusBar().showMessage("❌ Ошибка, файл с таким названием уже существует!")
            return

        self.delete_unsaved_table()
        self.database_connection = sqlite3.connect(self.database_name)  # Создание новой базы данных
        self.create_and_connect_journal()
        self.open_database()
        self.statusBar().showMessage(f"✅ База данных успешно создана!")

    def create_and_connect_journal(self):
        try:
            if self.database_connection:
                self.database_connection.close()  # Закрытие существующего соединения

            self.journaldb_name = f"JOURNAL_{self.database_name}"  # Создание имени резервной копии
            shutil.copy(self.database_name, self.journaldb_name)  # Копирование базы данных
            self.database_connection = None
            self.database_connection = sqlite3.connect(self.journaldb_name)  # Подключение к копии

            self.load_table_names()  # Загрузка списка таблиц
            self.load_table()  # Загрузка содержимого первой таблицы
        except FileNotFoundError:
            self.statusBar().showMessage("❌ Ошибка, исходный файл базы данных не найден!")
        except sqlite3.Error as e:
            self.statusBar().showMessage(f"❌ Ошибка SQLite: {e}")
        except Exception as e:
            self.statusBar().showMessage(f"❌ Непредвиденная ошибка: {e}")

    # Метод для сохранения изменений в базе данных
    def save_database(self):
        if not self.database_connection:
            self.statusBar().showMessage(f"❌ Ошибка, нет базы данных")
            return
        try:
            if os.path.exists(self.database_name):
                os.remove(self.database_name)  # Удаление старой базы данных

            if self.database_connection:
                self.database_connection.close()  # Закрытие текущего соединения

            current_directory = os.path.dirname(os.path.abspath(__file__))

            # Поиск и переименование резервной копии
            prefix = 'JOURNAL_'
            journal_path = None
            for filename in os.listdir(current_directory):
                if filename.startswith(prefix):
                    journal_path = os.path.join(current_directory, filename)
                    break

            if journal_path is None:
                self.statusBar().showMessage("❌ Ошибка, резервная копия не найдена!")
                return

            new_path = os.path.join(current_directory, self.database_name)
            os.rename(journal_path, new_path)  # Переименование файла-журнала

            self.saved_before_changes = True
            self.update_table()
            self.statusBar().showMessage(f"✅ Таблица сохранена и обновлена!")
        except FileNotFoundError:
            self.statusBar().showMessage("❌ Ошибка, файл для сохранения не найден!")
        except PermissionError:
            self.statusBar().showMessage("❌ Ошибка, недостаточно прав для изменения файлов!")
        except Exception as e:
            self.statusBar().showMessage(f"❌ Непредвиденная ошибка при сохранении: {e}")

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

        if not self.database_connection:
            self.statusBar().showMessage(f"❌ Ошибка, нет базы данных")
            return

        cursor = self.database_connection.cursor()
        sql_query = f"SELECT * FROM {table_name}"  # Выполнение запроса

        if not table_name.strip():
            return

        result = cursor.execute(sql_query).fetchall()

        self.tableWidget_database_content.setRowCount(len(result))  # Установка количества строк
        self.tableWidget_database_content.setColumnCount(len(cursor.description))  # Установка количества столбцов

        headers = [description[0] for description in cursor.description]
        self.tableWidget_database_content.setHorizontalHeaderLabels(headers)  # Установка заголовков столбцов

        # Заполнение таблицы данными
        for row_idx, row in enumerate(result):
            for col_idx, value in enumerate(row):
                self.tableWidget_database_content.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    # Метод для обновления данных таблицы
    def update_table(self):
        if not self.saved_before_changes:  # Проверка, сохранены ли данные
            quit_msg = "Внимание, все несохранённые данные будут утеряны!"
            reply = QMessageBox.question(self, f'Вы уверены, что хотите обновить таблицу?',
                                         quit_msg,
                                         QMessageBox.StandardButton.Yes,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return

        if not self.database_connection:
            self.statusBar().showMessage(f"❌ Ошибка, нет базы данных")
            return

        self.unload_table()  # Очистка данных текущей таблицы
        self.create_and_connect_journal()  # Создание и подключение журнала

    # Метод для выгрузки данных текущей таблицы
    def unload_table(self):
        self.combobox_chose_window.clear()  # Очистка списка таблиц
        self.tableWidget_database_content.setRowCount(0)  # Очистка строк
        self.tableWidget_database_content.setColumnCount(0)  # Очистка столбцов

    # Метод для удаления несохранённых данных
    def delete_unsaved_table(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Поиск и удаление резервной копии
        prefix = 'JOURNAL_'
        for filename in os.listdir(current_directory):
            if filename.startswith(prefix):
                file_path = os.path.join(current_directory, filename)
                os.remove(file_path)

    def closeEvent(self, event):
        if not self.saved_before_changes:  # Проверка, сохранены ли данные
            quit_msg = "Внимание, все несохранённые данные будут утеряны!"
            reply = QMessageBox.question(self, 'Вы уверены, что хотите закрыть программу?', quit_msg,
                                         QMessageBox.StandardButton.Yes,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

        try:
            if self.database_connection:
                self.database_connection.close()
            self.database_connection = None
            self.journaldb_name = None
            self.database_name = None
            self.saved_before_changes = True

            self.executeSQlWindow.close()
            self.unload_table()
            self.delete_unsaved_table()
            self.statusBar().showMessage("✅ Приложение успешно завершено")
        except Exception as e:
            self.statusBar().showMessage(f"❌ Ошибка при завершении работы: {e}")
            event.ignore()
            return

        event.accept()
