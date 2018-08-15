from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
                             QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
                             QVBoxLayout)
import main, queue
import sys
import sp_background
import commands

count = 0
server, recognizer = main.Initialize()
task_queue = queue.Queue()
command_queue = queue.Queue()
client = main.Manager("source", recognizer, task_queue, command_queue)


def slot_method():
    while True:
        client.run()


class Dialog(QDialog):

    def __init__(self):
        super(Dialog, self).__init__()

        button = QPushButton("Click")
        if count == 0:
            button.clicked.connect(slot_method)
        self.setGeometry(100, 100, 500, 20)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(button)
        self.setLayout(mainLayout)
        self.setWindowTitle("Button Example")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    try :
        dialog.exec_()
    except Exception as e :
        print(e)