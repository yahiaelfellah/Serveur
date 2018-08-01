import socket
import threading

import server3
import queue
import speech_recognition as sr

import sp

HOST = '192.168.8.100'
PORT = 8888
ADDR = (HOST, PORT)
BUFSIZE = 4096
Threads = []


def Initialize():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen(5)
    print('listening ...')
    r = sr.Recognizer()
    r.energy_threshold = 4000
    return server, r


def getIndex():
    # TODO : I Thought that we create a JSON in the server to regeister the ClinetId ( We have to GENERATE IT ) and every infomation that matter
    pass


def createClientQueue():
    task_queue = queue.Queue()


class Client:
    def __init__(self, clientId, speech, _queue):
        # threading.Thread.__init__(self)
        self.clientId = clientId
        self.speech = speech
        self.queue = _queue

    def run(self):
        task_queue = self.queue
        thread_server = server3.Server(server, BUFSIZE,1, self.clientId, True, task_queue)
        thread_sp = sp.Recognizer(self.clientId, self.speech, 0, self.queue)

        item = task_queue.get()
        if task_queue.isEmpty():
            thread_server.run()
            Threads.append(thread_server)
        else:
            thread_server.run()
            print("thred_server")
            thread_sp.run()
            print("thred_sp")


if __name__ == "__main__":
    task_queue = queue.Queue()
    server, recognizer = Initialize()
    client = Client("Sources", recognizer, task_queue)
    client.run()
