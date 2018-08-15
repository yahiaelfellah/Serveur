from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QToolTip
import sys


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.title = "closing"
        self.initUI()

    def initUI(self):
        button = QPushButton("Quit", self)
        button.setToolTip("This is a <b>QPushButton</b> widget")
        button.resize(button.sizeHint())
        button.move(50, 50)
        button.clicked.connect(QApplication.instance().quit)

        # In this , we connect the button with QApplication with a signal
        # button send a quit signal to the receiver which is the QApplication

        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Example()
    sys.exit(app.exec_())
