import logging
import os
import queue
import socket
import tempfile
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )


def createFolder(directory):
    if not os.path.exists(directory):
        os.mkdir(directory, mode=0o777)


def granted_access(f):
    if os.path.exists(f):
        try:
            os.rename(f, f)
            print('Access on file "' + f + '" is available!')
        except OSError as e:
            print('Access-error on file "' + f + '"! \n' + str(e))


def sleep(n):
    time.sleep(n)


def receiving(cnx, dataFile, titleFile, bufferSize=4096):
    titleData = 0
    data = cnx.recv(bufferSize)
    if not data:
        return False
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
        return True


class Server:

    def __init__(self, threadId=None, bufferSize=4096,
                 clientId=None, queue=None, server=None):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.bufferSize = bufferSize
        self.clientId = clientId
        self.queue = queue
        self.server = server

    def run(self,cnx):
        # cnx, address = self.server.accept()
        receive = True
        # print("Connection with " + str(address[0]) + ":" + str(address[1]))
        while not self.queue.full():
            logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
            createFolder(self.clientId)
            titleFile = tempfile.NamedTemporaryFile('w+b', dir=self.clientId, delete=True)
            dataFile = tempfile.NamedTemporaryFile('w+b', dir=self.clientId, delete=True)
            while True:
                titleData = 0
                data = cnx.recv(4096)
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
            logging.info("split done")
            try:
                titleFile.seek(0)
                title = titleFile.read().decode("utf-8").replace('\x00', "")
                print(title)
                original_filename = dataFile.name
                print(original_filename)
                path = os.getcwd() + "\\" + self.clientId + "\\" + title
                os.link(original_filename, path)
            except IOError as e:
                print(e)
            titleFile.close()
            dataFile.close()
            self.queue.put(path)
            logging.debug('Putting ' + str(path)
                          + ' : ' + str(self.queue.qsize()) + ' items in queue')
            print('finished writing file')
            cnx.close()
            print('client disconnected')
        return self.queue



