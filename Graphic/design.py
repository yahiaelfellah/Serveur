from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QAction, QFileDialog

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


def showDialog(mainWindow):
    fname = QFileDialog.getOpenFileName(mainWindow, 'Open file', '/')

    if fname[0]:
        f = open(fname[0], 'r')

        # with f:
        #     data = f.read()
        #     mainWondow.textEdit.setText(data)


class Ui_MainWindow(object):

    def setupUi(self, Mainwindow):
        Mainwindow.setObjectName(_fromUtf8("MainWindow"))
        Mainwindow.resize(500, 500)
        self.mainMenu = Mainwindow.menuBar()
        fileMenu = self.mainMenu.addMenu('File')
        editMenu = self.mainMenu.addMenu('Edit')
        viewMenu = self.mainMenu.addMenu('View')
        searchMenu = self.mainMenu.addMenu('Search')
        toolsMenu = self.mainMenu.addMenu('Tools')
        helpMenu = self.mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)

        helpButton = QAction('Help', self)
        helpButton.setShortcut('F1')
        helpButton.setStatusTip('Help User')
        helpMenu.addAction(helpButton)

        new_action = QAction('New', self)
        new_action.setShortcut('Ctrl+N')

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')

        open_action = QAction('&Open', self)
        open_action.setShortcut('Ctrl+O')
        # open_action.triggered.connect(showDialog(Mainwindow))

        fileMenu.addAction(new_action)
        fileMenu.addAction(open_action)
        fileMenu.addAction(save_action)
        fileMenu.addAction(exitButton)

        self.centralwidget = QWidget(Mainwindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.buttons_layout = QHBoxLayout(self.centralwidget)
        self.buttons_layout.setObjectName(_fromUtf8("buttons_layout"))
        # Button to start threads
        self.button_start_threads = QPushButton(self.centralwidget)
        self.button_start_threads.clicked.connect(self.start_threads)
        self.button_start_threads.setText("Start Server")
        self.buttons_layout.addWidget(self.button_start_threads)
        # Button to stop Threads
        self.button_stop_threads = QPushButton(self.centralwidget)
        self.button_stop_threads.setText("Stop Server")
        self.button_stop_threads.setDisabled(True)
        self.button_stop_threads.clicked.connect(self.abort_workers)
        self.buttons_layout.addWidget(self.button_stop_threads)

        self.verticalLayout.addLayout(self.buttons_layout)

        self.command_layout = QtWidgets.QVBoxLayout()
        self.command_layout.setObjectName(_fromUtf8("command_layout"))
        self.command_label = QtWidgets.QLabel(self.centralwidget)
        self.command_label.setObjectName(_fromUtf8("command_label"))
        self.command_layout.addWidget(self.command_label)
        self.log_server = QtWidgets.QListWidget(self.centralwidget)
        self.command_layout.addWidget(self.log_server)
        self.verticalLayout.addLayout(self.command_layout)

        Mainwindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(Mainwindow)
        QtCore.QMetaObject.connectSlotsByName(Mainwindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Server", None))
        # self.server_label.setText(_translate("MainWindow","Server:",None))
        # self.sp_label.setText(_translate("MainWindow","Speech:",None))
        self.command_label.setText(_translate("MainWindow", "Server:", None))
        self.button_stop_threads.setText(_translate("MainWindow", "Stop", None))
        self.button_start_threads.setText(_translate("MainWindow", "Start", None))

    def open_file(self):
        return QFileDialog.getOpenFileName(self.Mainwindow, 'Open File', '/')
