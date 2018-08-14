import logging
import os
import threading
import time
import speech_recognition as sr
import queue


def createFile(clientId):
    # path = clientId + "\\Transcribe.txt"
    path = os.path.join(clientId,"Transcribe.txt")
    if os.path.isfile(path):
        f = open(path, "wt")
        f.close()


def writeToFile(text, clientId, mode):
    path = os.path.join(clientId,"Transcribe.txt")
    if not os.path.isfile(path):
        createFile(path)
    with open(path, mode) as f:
        f.write(text)
    f.close()


class Recognizer(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval, clientId, speech_recognizer,
                 lastIndex, threadId, queue_task, queue_command):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.clientId = clientId
        self.threadId = threadId
        self.speech_recognizer = speech_recognizer
        self.lastIndex = lastIndex
        self.queue_task = queue_task
        self.queue_command = queue_command
        createFile(clientId=self.clientId)
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            time.sleep(self.interval)
            print('sp running in the background')
            fileIndex = self.lastIndex
            if not self.queue_task.empty():
                r = self.speech_recognizer
                path_task = self.queue_task.get()
                logging.debug('Getting ' + str(path_task)
                              + ' : ' + str(self.queue_task.qsize()) + ' items in queue_task')
                if os.path.isfile(path_task):
                    print('we are reading ' + path_task)
                    try:
                        with sr.AudioFile(path_task) as source:
                            audio = r.record(source)
                    except IOError as e:
                        print("handling error")
                        print(e)
                        pass
                    try:
                        text = r.recognize_google(audio, language="en-US")
                        writeToFile(text + "\n", self.clientId, "a+")
                        print('Done!')
                        print(text)
                        fileIndex += 1
                        # if text == "audio stop":
                        #     fileIndex = 0
                    except sr.UnknownValueError:
                        writeToFile("Google Speech Recognition could not understand audio" + "\n", self.clientId
                                    , "a+")
                    except sr.RequestError:
                        writeToFile("Could not request results from Google Speech Recognition service", self.clientId
                                    , "a+")
                    except Exception as e:
                        print(e)
                    else:
                        print("no more files to transcribe for %s ......... " % self.clientId)
                        path_command = self.clientId + "\\"+"Transcribe.txt"
                        self.queue_command.put(path_command)
                        logging.debug('Putting ' + str(path_command)
                                      + ' : ' + str(self.queue_command.qsize()) + ' items in queue_command')
            else :
                print("queue is empty we are waiting ! ")
            return self.queue_task ,self.queue_command
