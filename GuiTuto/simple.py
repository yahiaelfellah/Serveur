"""
We create a simple window using PyQt5
with 2 differente method we can do that
"""
from PyQt5.QtWidgets import QWidget, QApplication
import sys


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "sample"
        self.width = 250
        self.height = 150
        self.top = 100
        self.left = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


if __name__ == '__main__':

    # SAMPLE 1 : we create a class
    app1 = QApplication(sys.argv)
    w1 = App()
    sys.exit(app1.exec_())

    # We use it in the main loop
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(250, 150)
    w.move(250, 50)
    # w.mouseDoubleClickEvent(QMouseEvent=event())
    w.setWindowTitle("Hello")
    w.show()
    sys.exit(app.exec_())
