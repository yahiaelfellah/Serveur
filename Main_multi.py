import queue
import sys

import server
import sp
import socket
import select
import speech_recognition as sr


def Init():
    PORT = 8888
    HOST = "192.168.61.109"

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.setblocking(0)
    server_socket.listen(10)
    inputs = [server_socket]
    print('listening ...')
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 4000
    return server_socket, inputs, recognizer


class Manager:
    def __init__(self, CONNECTION_LIST, server_socket, queue, speech):
        self.server = server_socket
        self.inputs = CONNECTION_LIST
        self.queue = queue
        self.recognizer = speech

    def run(self):
            outputs = []
            while self.inputs:
                read_socket, write_socket, error_socket = select.select(self.inputs, outputs, self.inputs)
                for sock in read_socket:

                    if sock is self.server:
                        # A "readable" server socket is ready to accept a connection
                        connection, address = sock.accept()
                        print("Connection with " + str(address[0]) + ":" + str(address[1]))
                        self.inputs.append(connection)
                    else:
                        server_thread = server.Server(threadId=1, bufferSize=4096,
                                                      clientId="source", queue=self.queue)
                        sp_thread = sp.Recognizer(clientId="source", speech_recognizer=self.recognizer,
                                                  lastIndex=0, threadId=1, queue=self.queue)
                        self.queue = server_thread.run(sock)
                        # self.queue = sp_thread.run()
                    self.inputs.remove(sock)


if __name__ == "__main__":
    try :
        server_socket, inputs, recognizer = Init()
        tasks = queue.Queue()
        client = Manager(inputs, server_socket, tasks, recognizer)
        client.run()
    except KeyboardInterrupt:
        sys.exit()
