# Form implementation generated from reading ui file 'UiExecuteSQL.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ExecuteSQL(object):
    def setupUi(self, ExecuteSQL):
        ExecuteSQL.setObjectName("ExecuteSQL")
        ExecuteSQL.resize(264, 461)
        self.centralwidget = QtWidgets.QWidget(parent=ExecuteSQL)
        self.centralwidget.setObjectName("centralwidget")
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.mainLayout.setObjectName("mainLayout")
        self.textEdit_sql_query = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.textEdit_sql_query.setObjectName("textEdit_sql_query")
        self.mainLayout.addWidget(self.textEdit_sql_query)
        self.tableView_query_result = QtWidgets.QTableView(parent=self.centralwidget)
        self.tableView_query_result.setObjectName("tableView_query_result")
        self.mainLayout.addWidget(self.tableView_query_result)
        self.btn_execute_query = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_execute_query.setObjectName("btn_execute_query")
        self.mainLayout.addWidget(self.btn_execute_query)
        ExecuteSQL.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=ExecuteSQL)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 264, 21))
        self.menubar.setObjectName("menubar")
        ExecuteSQL.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=ExecuteSQL)
        self.statusbar.setObjectName("statusbar")
        ExecuteSQL.setStatusBar(self.statusbar)

        self.retranslateUi(ExecuteSQL)
        QtCore.QMetaObject.connectSlotsByName(ExecuteSQL)

    def retranslateUi(self, ExecuteSQL):
        _translate = QtCore.QCoreApplication.translate
        ExecuteSQL.setWindowTitle(_translate("ExecuteSQL", "Выполнить SQL"))
        self.textEdit_sql_query.setPlaceholderText(_translate("ExecuteSQL", "Введите SQL команду здесь"))
        self.btn_execute_query.setText(_translate("ExecuteSQL", "Выполнить команду"))
