from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton
import sys
from PyQt5.QtGui import QFont


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.title = 'tooltip'
        self.initUI()

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10)) # A static method sets a font 
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton("button", self)
        btn.setToolTip("This is a <i><b>QPushButton</br></i> widget")
        btn.resize(btn.sizeHint()) # SizeHint() give a recommended size for a button
        btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle(self.title)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Example()
    sys.exit(app.exec_())