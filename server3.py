import os
import shutil
import threading
import tempfile
import socket
import os
import queue

title = ""


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


class Server:

    def __init__(self, _server, bufferSize, threadId, clientId, pending,_queue):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.clientId = clientId
        self._server = _server
        self.bufferSize = bufferSize
        self.pending = pending
        self.queue = _queue

    def run(self):
        # TODO : Refomat the server3.py ! Done
        # TODO : Create a thread Class  ! Done 2:25 PM
        print("Server is listening for incoming Data ")
        while self.pending:
            titleData = 0
            conn, address = self._server.accept()
            print('client connected ... ' + str(address[0]) + ":" + str(address[1]))
            # We create a temporary files
            # The title we don't need it so we delete it !
            titleFile = tempfile.NamedTemporaryFile('w+b', dir='', delete=True)
            dataFile = tempfile.NamedTemporaryFile('w+b', dir='', delete=True)

            while True:
                data = conn.recv(self.bufferSize)
                if not data:
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
                title = titleFile.read().decode("utf-8")
                print(title)
                if not self.queue.Full():
                    self.queue.put(title,False)
                else:
                    # TODO : I don't know
                    pass
                original_filename = dataFile.name
                print(original_filename)
                os.link(original_filename, title[:8])
                try:
                    self.queue.task_done()
                except ValueError:
                    pass
            except Exception as e:
                print(e)
                pass
            titleFile.close()
            dataFile.close()
            print('finished writing file')
            conn.close()
            print('client disconnected')


if __name__ == "__main__":
    # The use of this class :
    HOST = '192.168.8.100'
    PORT = 8888
    ADDR = (HOST, PORT)
    BUFSIZE = 4096
    OFFSET = BUFSIZE * 8 + BUFSIZE
    queue = queue.Queue()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(ADDR)

    server.listen(5)
    print("serving through : %i" % PORT)
    print('listening ...')
    thread_server = Server(server, BUFSIZE, 1, 2, True)
    thread_server.run()
