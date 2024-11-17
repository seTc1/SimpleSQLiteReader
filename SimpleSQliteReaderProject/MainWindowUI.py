# Form implementation generated from reading ui file 'SimpleReaderUI.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(886, 617)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 864, 601))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_create_database = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btn_create_database.setObjectName("btn_create_database")
        self.horizontalLayout.addWidget(self.btn_create_database)
        self.btn_open_database = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btn_open_database.setObjectName("btn_open_database")
        self.horizontalLayout.addWidget(self.btn_open_database)
        self.btn_save_bd = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btn_save_bd.setObjectName("btn_save_bd")
        self.horizontalLayout.addWidget(self.btn_save_bd)
        self.lineEdit_database_name = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_database_name.setEnabled(True)
        self.lineEdit_database_name.setMaximumSize(QtCore.QSize(225, 16777215))
        self.lineEdit_database_name.setObjectName("lineEdit_database_name")
        self.horizontalLayout.addWidget(self.lineEdit_database_name)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lable_tabletext = QtWidgets.QLabel(parent=self.layoutWidget)
        self.lable_tabletext.setObjectName("lable_tabletext")
        self.horizontalLayout_2.addWidget(self.lable_tabletext)
        self.combobox_chose_window = QtWidgets.QComboBox(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combobox_chose_window.sizePolicy().hasHeightForWidth())
        self.combobox_chose_window.setSizePolicy(sizePolicy)
        self.combobox_chose_window.setMinimumSize(QtCore.QSize(100, 0))
        self.combobox_chose_window.setObjectName("combobox_chose_window")
        self.horizontalLayout_2.addWidget(self.combobox_chose_window)
        self.btn_update_table = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btn_update_table.setObjectName("btn_update_table")
        self.horizontalLayout_2.addWidget(self.btn_update_table)
        self.btn_execute_sql = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.btn_execute_sql.setObjectName("btn_execute_sql")
        self.horizontalLayout_2.addWidget(self.btn_execute_sql)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.tableView_database_content = QtWidgets.QTableView(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tableView_database_content.sizePolicy().hasHeightForWidth())
        self.tableView_database_content.setSizePolicy(sizePolicy)
        self.tableView_database_content.setMinimumSize(QtCore.QSize(550, 0))
        self.tableView_database_content.setObjectName("tableView_database_content")
        self.verticalLayout_3.addWidget(self.tableView_database_content)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.action = QtGui.QAction(parent=MainWindow)
        self.action.setObjectName("action")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SQLite Database Manager"))
        self.btn_create_database.setText(_translate("MainWindow", "Создать БД"))
        self.btn_open_database.setText(_translate("MainWindow", "Открыть БД"))
        self.btn_save_bd.setText(_translate("MainWindow", "Сохранить БД"))
        self.lineEdit_database_name.setPlaceholderText(_translate("MainWindow", "Введите название базы данных"))
        self.lable_tabletext.setText(_translate("MainWindow", "Таблица:"))
        self.btn_update_table.setText(_translate("MainWindow", "Обновить таблицу"))
        self.btn_execute_sql.setText(_translate("MainWindow", "Выполнить SQL"))
        self.action.setText(_translate("MainWindow", "Создать базу данных"))
