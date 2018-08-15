from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal as SIGNAL, pyqtSlot
import sys
import sp_background
from multiprocessing import cpu_count
import main
import Graphic.design as design
import os
import server3
import socket
import speech_recognition as sr
import queue

PORT = 8888
BUFSIZE = 4096


def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print(args)


sys.excepthook = trap_exc_during_debug


class Manager(QThread):
    def __init__(self, server, clientId, speech, queue_task, queue_command):
        """

        :param clientId:
        :param speech:
        :param queue_task:
        :param queue_command:
        """
        QThread.__init__(self)
        self.clientId = clientId
        self.speech = speech
        self.queue_task = queue_task
        self.queue_command = queue_command
        self.server = server
        #  used internally
        self.THREADS = []
        self.server_worker = []
        self.sp_worker = []
        self.NUMBER_THREAD = cpu_count()

    def __del__(self):
        self.wait()

    @pyqtSlot()
    def run(self):
        # self.emit(SIGNAL('add_post(QString)'), "Running")
        self.server_worker = [server3.Server(self.server, BUFSIZE, i, self.clientId, True, self.queue_task) for i in
                              range(self.NUMBER_THREAD)]
        self.sp_worker = sp_background.Recognizer(1, self.clientId, self.speech, 0, 1, self.queue_task,
                                                  self.queue_command)
        # command_worker = commands.CommandManager(self.queue_command)
        print("running %i thread for each " % self.NUMBER_THREAD)
        # while True:
        for t in self.server_worker:
            self.queue_task = t.run()
            self.queue_task.task_done()
            self.THREADS.append(t)
            path = self.queue_task.get()
            self.queue_task.put(path)
            if not os.access(path, os.R_OK):
                continue
            else:
                self.queue_task, self.queue_command = self.sp_worker.run()
            try:
                # command_worker.run_match()
                pass
            except Exception as e:
                print(e)


class ThreadingTutorial(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self, task_queue, command_queue):
        super(ThreadingTutorial, self).__init__()
        self.queue_task = task_queue
        self.queue_command = command_queue
        self.clientId = ""
        self.speech = None
        self.server = None
        self.setupUi(self)
        self.btn_start.clicked.connect(self.startServer)
        self.btn_init.clicked.connect(self.Initialize)

    def Initialize(self):

        global HOST
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            HOST = socket.gethostbyname(socket.gethostname())
        except socket.gaierror as e:
            QtWidgets.QMessageBox.critical(self, "No subreddits", e,
                                           QtWidgets.QMessageBox.Ok)
        ADDR = (HOST, PORT)
        self.server.bind(ADDR)
        self.server.listen(10)
        self.speech = sr.Recognizer()
        self.speech.energy_threshold = 4000
        message = "HostAddress : %s\n" % HOST + "Port : %i\nServer started successfully\nRecognize started successfully" % PORT
        QtWidgets.QMessageBox.information(self, "Starting", message)
        self.btn_init.setEnabled(False)
        self.btn_start.setEnabled(True)
        self.add_post("Listening............")
        return

    def startServer(self):

        self.get_thread = Manager(self.server, 'source', self.speech, self.queue_task, self.queue_command)

        # self.connect(self.get_thread, SIGNAL("add_post(QString)"), self.add_post)

        # self.connect(self.get_thread, SIGNAL("finished()"), self.done)
        try :
            self.get_thread.run()
        except Exception as e :
            print(e)
            pass
        self.btn_stop.setEnabled(True)
        self.btn_stop.clicked.connect(self.get_thread.terminate)
        self.btn_start.setEnabled(False)

    @pyqtSlot()
    def add_post(self, post_text):
        self.list_submissions.addItem(post_text)

    @pyqtSlot()
    def done(self):
        self.btn_stop.setEnabled(False)
        self.btn_start.setEnabled(True)
        QtWidgets.QMessageBox.information(self, "Done!", "Done fetching posts!")

    def closeEvent(self, QCloseEvent):
        reply = QtWidgets.QMessageBox.question(self, 'Message', 'Are you sure to quit ?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


def main():
    task_queue = queue.Queue()
    command_queue = queue.Queue()
    app = QtWidgets.QApplication(sys.argv)
    form = ThreadingTutorial(task_queue, command_queue)
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
