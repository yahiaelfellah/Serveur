import logging
import os
import queue
import socket
import tempfile
import threading
import time

title = ""
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )


# Obsolete
# TODO : Verifiy if this work : run this alone
def reformat(raw_bytes):
    titleBin = ' '.join(map(lambda x: '{:08b}'.format(x), raw_bytes))

    STARTING = titleBin.find('1')
    titleBin = titleBin[STARTING:]
    SPACE_INDEX = titleBin.find(' ')
    tempStr = titleBin[:SPACE_INDEX]

    for x in range(8 - len(tempStr)):
        tempStr = '0' + tempStr
    titleBin = tempStr + titleBin[SPACE_INDEX:]
    print(titleBin)

    for word in titleBin.split(' '):
        title = title + chr(int(word, 2))
    print(title)
    return title


def createFolder(directory):
    if not os.path.exists(directory):
        os.mkdir(directory, mode=0o777)


def granted_accss(f):
    if os.path.exists(f):
        try:
            os.rename(f, f)
            print('Access on file "' + f + '" is available!')
        except OSError as e:
            print('Access-error on file "' + f + '"! \n' + str(e))


def sleep(n):
    time.sleep(n)


class Server:
    queue = queue.Queue()
    pending = False

    def __init__(self, _server=None, bufferSize=None, threadId=None,
                 clientId=None, pending=None,condition=None,queue=None):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.clientId = clientId
        self._server = _server
        self.bufferSize = bufferSize
        self.pending = pending
        self.condition = condition
        self.queue = queue
        createFolder(clientId)

    def run(self):
        # TODO : Refomat the server3.py ! Done
        # TODO : Create a thread Class  ! Done 2:25 PM
        print("Server is listening for incoming Data ")
        while True:
            if not self.queue.full():
                conn, address = self._server.accept()
                titleData = 0
                print('client connected ... ' + str(address[0]) + ":" + str(address[1]))
                # We create a temporary files
                # The title we don't need it so we delete it !
                createFolder(self.clientId)
                titleFile = tempfile.NamedTemporaryFile('w+b', dir=self.clientId, delete=True)
                dataFile = tempfile.NamedTemporaryFile('w+b', dir=self.clientId, delete=True)
                print(str(self.threadId))
                while self.pending:
                    data = conn.recv(self.bufferSize)
                    if not data:
                        self.pending = False
                        break
                    if titleData >= 4096:
                        dataFile.write(data)
                        print('writing file .... temp_data ... ', len(data))
                    if titleData < 4096:
                        if titleData + len(data) > 4096:
                            print('EXCEPTION')
                            titleFile.write(data[:4096 - titleData])
                            print('writing file .... temp_title ... ', 4096 - titleData)
                            dataFile.write(data[4096 - titleData:])
                            print('writing file .... temp_data ... ', len(data[4096 - titleData:]))
                            titleData = titleData + len(data)
                        else:
                            titleFile.write(data)
                            print('writing file .... temp_title ... ', len(data))
                            titleData = titleData + len(data)

                print('split done')
                try:
                    titleFile.seek(0)
                    title = titleFile.read().decode("utf-8").replace('\x00', "")
                    print(title)
                    original_filename = dataFile.name
                    print(original_filename)
                    path = os.getcwd() + "\\" + self.clientId + "\\" + title[:15]
                    # path = "%s'\\'%s'\\'%s" % os.getcwd() % self.clientId % title
                    os.link(original_filename, path)

                except Exception as e:
                    print(e)
                    pass
                dataFile.close()
                self.condition.acquire()
                print ('condition acquired by %s' % self.clientId)
                granted_accss(path)
                titleFile.close()
                self.queue.put(path)
                self.condition.notify()
                self.condition.release()
                logging.debug('Putting ' + str(path)
                              + ' : ' + str(self.queue.qsize()) + ' items in queue')
                print('finished writing file')
                conn.close()
                print('client disconnected')
            return self.queue

    def get_name(self):
        return self.get_name()


if __name__ == "__main__":
    # TODO : I HAVE TO change the principal functionality
    # The use of this class :
    HOST = '192.168.61.109'
    PORT = 8888
    ADDR = (HOST, PORT)
    BUFSIZE = 4096
    OFFSET = BUFSIZE * 8 + BUFSIZE
    THREAD_NUM = 2
    queue = queue.Queue()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)

    server.listen(5)
    print("serving through : %i" % PORT)
    print('listening ...')

    thread_server = Server(server, BUFSIZE, 1, "source", True, None)
    thread_server1 = Server(server, BUFSIZE, 2, "source", True, None)
    # executor = ThreadPoolExecutor(max_workers=THREAD_NUM)
    # a = executor.submit(thread_server.run())
    # b = executor.submit(thread_server1.run())

    # for i in range(THREAD_NUM):
    #    thread_server = Server(server, BUFSIZE, i, "source", True, None)
    #    thread_server.run()
