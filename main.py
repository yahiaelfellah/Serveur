import os
import socket
import threading

import server3
import queue
import speech_recognition as sr
from multiprocessing import cpu_count
from old import sp
import sp_background
import commands

# HOST = "192.168.61.109"
PORT = 8888
BUFSIZE = 4096
Threads = []


def Initialize():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        HOST = socket.gethostbyname(socket.gethostname())
        print(HOST)
    except socket.gaierror as e:
        print(e)
    ADDR = (HOST, PORT)
    server.bind(ADDR)
    server.listen(10)
    print('listening ...')
    r = sr.Recognizer()
    r.energy_threshold = 4000
    return server, r


def getIndex():
    # TODO : I Thought that we create a JSON in the server to regeister the ClinetId
    # TODO : ( We have to GENERATE IT ) and every infomation that matter
    pass


class Manager:

    def __init__(self, clientId, speech, queue_task,queue_command):
        self.clientId = clientId
        self.speech = speech
        self.THREADS = []
        self.queue_task = queue_task
        self.queue_command = queue_command
        self.server_worker = []
        self.sp_worker = []
        self.thread_server = server3
        self.thread_sp = sp.Recognizer(self.clientId, self.speech, 0, 1)
        self.NUMBER_THREAD = cpu_count()

    def run(self):

        condition = threading.Condition()
        self.server_worker = [server3.Server(server, BUFSIZE, i, self.clientId, True, self.queue) for i in
                              range(self.NUMBER_THREAD)]
        sp_worker = sp_background.Recognizer(1, self.clientId, self.speech, 0, 1, self.queue)
        command_worker = commands.CommandManager.run_match()
        print("running %i thread for each " % self.NUMBER_THREAD)
        for t in self.server_worker:
            self.queue_task = t.run()
            self.queue_task.task_done()
            self.THREADS.append(t)
            path = self.queue_task.get()
            self.queue_task.put(path)
            if not os.access(path, os.R_OK):
                continue
            else:
                sp_worker.run()

    def get_thread_tab(self):
        return self.THREADS

    def stop(self, _queue):
        _queue.put(None)
        for t in self.THREADS:
            t.join()
        _queue.close()


if __name__ == "__main__":
    server, recognizer = Initialize()
    task_queue = queue.Queue()
    command_queue = queue.Queue()
    client = Manager("source", recognizer, task_queue,command_queue)
    while True:
        client.run()
