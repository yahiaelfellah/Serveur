import sys
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QDesktopWidget


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.title = "Message Box"
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(300, 300, 300, 200)
        self.center()
        self.show()

    # Override the functionality of the closing window (X)
    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit ?', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Example()
    sys.exit(app.exec_())
