import time
import sys
from multiprocessing import cpu_count
import server3
import sp_background
import os
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget

BUFSIZE = 4096


def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print(args)


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug


class Manager(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """

    sig_step = pyqtSignal(int, str)  # worker id, step description: emitted every step through work() loop
    sig_done = pyqtSignal(int)  # worker id: emitted at end of work()
    sig_msg = pyqtSignal(str)  # message to be shown to user

    def __init__(self, id: int, server, clientId, speech, queue_task, queue_command):
        super().__init__()
        self.__id = id
        self.__abort = False
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

    def run(self):
        # self.emit(SIGNAL('add_post(QString)'), "Running")
        self.server_worker = [server3.Server(self.server, BUFSIZE, i, self.clientId, True, self.queue_task) for i in
                              range(self.NUMBER_THREAD)]
        self.sp_worker = sp_background.Recognizer(1, self.clientId, self.speech, 0, 1, self.queue_task,
                                                  self.queue_command)
        # command_worker = commands.CommandManager(self.queue_command)
        print("running %i thread for each " % self.NUMBER_THREAD)
        while True:
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
                # command_worker.run_match()



    @pyqtSlot()
    def work(self):
        """
        Pretend this worker method does work that takes a long time. During this time, the thread's
        event loop is blocked, except if the application's processEvents() is called: this gives every
        thread (incl. main) a chance to process events, which in this sample means processing signals
        received from GUI (such as abort).
        """
        thread_name = QThread.currentThread().objectName()
        thread_id = int(QThread.currentThreadId())  # cast to int() is necessary
        self.sig_msg.emit('Running worker #{} from thread "{}" (#{})'.format(self.__id, thread_name, thread_id))
        self.run()
        self.sig_step.emit(self.__id, 'step ' )
        # check if we need to abort the loop; need to process events to receive signals;
        app.processEvents()  # this could cause change to self.__abort
        if self.__abort:
        # note that "step" value will not necessarily be same for every thread
            self.sig_msg.emit('Worker #{} aborting work at step'+str(self.__id))
        self.sig_done.emit(self.__id)

    def abort(self):
        self.sig_msg.emit('Worker #{} notified to abort'.format(self.__id))
        self.__abort = True


class MyWidget(QWidget):
    NUM_THREADS = 5

    # sig_start = pyqtSignal()  # needed only due to PyCharm debugger bug (!)
    sig_abort_workers = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Thread Example")
        form_layout = QVBoxLayout()
        self.setLayout(form_layout)
        self.resize(400, 800)

        self.button_start_threads = QPushButton()
        self.button_start_threads.clicked.connect(self.start_threads)
        self.button_start_threads.setText("Start {} threads".format(self.NUM_THREADS))
        form_layout.addWidget(self.button_start_threads)

        self.button_stop_threads = QPushButton()
        self.button_stop_threads.clicked.connect(self.abort_workers)
        self.button_stop_threads.setText("Stop threads")
        self.button_stop_threads.setDisabled(True)
        form_layout.addWidget(self.button_stop_threads)

        self.log = QTextEdit()
        form_layout.addWidget(self.log)

        self.progress = QTextEdit()
        form_layout.addWidget(self.progress)

        QThread.currentThread().setObjectName('main')  # threads can be named, useful for log output
        self.__workers_done = None
        self.__threads = None

    def start_threads(self):
        self.log.append('starting {} threads'.format(self.NUM_THREADS))
        self.button_start_threads.setDisabled(True)
        self.button_stop_threads.setEnabled(True)

        self.__workers_done = 0
        self.__threads = []
        for idx in range(self.NUM_THREADS):
            worker = Worker(idx)
            thread = QThread()
            thread.setObjectName('thread_' + str(idx))
            self.__threads.append((thread, worker))  # need to store worker too otherwise will be gc'd
            worker.moveToThread(thread)

            # get progress messages from worker:
            worker.sig_step.connect(self.on_worker_step)
            worker.sig_done.connect(self.on_worker_done)
            worker.sig_msg.connect(self.log.append)

            # control worker:
            self.sig_abort_workers.connect(worker.abort)

            # get read to start worker:
            # self.sig_start.connect(worker.work)  # needed due to PyCharm debugger bug (!); comment out next line
            thread.started.connect(worker.work)
            thread.start()  # this will emit 'started' and start thread's event loop

        # self.sig_start.emit()  # needed due to PyCharm debugger bug (!)

    @pyqtSlot(int, str)
    def on_worker_step(self, worker_id: int, data: str):
        self.log.append('Worker #{}: {}'.format(worker_id, data))
        self.progress.append('{}: {}'.format(worker_id, data))

    @pyqtSlot(int)
    def on_worker_done(self, worker_id):
        self.log.append('worker #{} done'.format(worker_id))
        self.progress.append('-- Worker {} DONE'.format(worker_id))
        self.__workers_done += 1
        if self.__workers_done == self.NUM_THREADS:
            self.log.append('No more workers active')
            self.button_start_threads.setEnabled(True)
            self.button_stop_threads.setDisabled(True)
            # self.__threads = None

    @pyqtSlot()
    def abort_workers(self):
        self.sig_abort_workers.emit()
        self.log.append('Asking each worker to abort')
        for thread, worker in self.__threads:  # note nice unpacking by Python, avoids indexing
            thread.quit()  # this will quit **as soon as thread event loop unblocks**
            thread.wait()  # <- so you need to wait for it to *actually* quit

        # even though threads have exited, there may still be messages on the main thread's
        # queue (messages that threads emitted before the abort):
        self.log.append('All threads exited')


if __name__ == "__main__":
    app = QApplication([])

    form = MyWidget()
    form.show()

    sys.exit(app.exec_())
