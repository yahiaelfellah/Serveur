import socket
import sys
import server3
import queue
import speech_recognition as sr

import sp

PORT = 8888
BUFSIZE = 4096
Threads = []


def Initialize():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        HOST = socket.gethostbyname(socket.getfqdn())
    except socket.gaierror as e:
        print(e)
        HOST = "192.168.61.109"
        sys.exit

    print(HOST)
    ADDR = (HOST, PORT)
    server.bind(ADDR)
    server.listen(5)
    print('listening ...')
    r = sr.Recognizer()
    r.energy_threshold = 4000
    return server, r


def getIndex():
    # TODO : I Thought that we create a JSON in the server to regeister the ClinetId
    # TODO : ( We have to GENERATE IT ) and every infomation that matter
    pass


# def createClientQueue():
#     task_queue = queue.Queue()
#

class Manager:

    def __init__(self, clientId=None, speech=None):
        # threading.Thread.__init__(self)
        self.clientId = clientId
        self.speech = speech
        self.THREADS = []
        self.thread_server = server3.Server(server, BUFSIZE, 1, self.clientId, True)
        self.thread_sp = sp.Recognizer(self.clientId, self.speech, 0)

    def run(self, _queue):
        while True:
            _queue = self.thread_server.run(_queue)
            self.THREADS.append(self.thread_server)
            self.thread_server.sleep(0.05)
            _queue = self.thread_sp.run(_queue)
            self.THREADS.append(self.thread_sp)
            self.thread_sp.sleep(0.05)

        # if len(self.tab) == 0:
        #     self.tab=thread_server.run(self.tab)
        #
        #     print(str(self.tab))
        # else:
        #     thread_server.run(self.tab)
        #     print("thred_server")
        #     thread_sp.run(self.tab[0])
        #     print("thred_sp")

    def stop(self, _queue):
        _queue.put(None)
        for t in self.THREADS:
            t.join()
        _queue.close()


if __name__ == "__main__":
    task_queue = queue.Queue()
    server, recognizer = Initialize()
    client = Manager("source", recognizer)
    client.run(task_queue)
