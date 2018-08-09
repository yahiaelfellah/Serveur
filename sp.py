import logging
import os
import queue
import threading
import time

import speech_recognition as sr
import socket


# TODO : Reformat the sp script : Done 4:00 AM
def createFile(clientId):
    path = clientId + "/Transcibe.txt"
    f = open(path, "wt")
    f.close()


def writeToFile(text, clientId, mode):
    path = clientId + "/Transcibe.txt"
    if not os.path.isfile(path):
        createFile(path)
    with open(path, mode) as f:
        f.write(text)
    f.close()


class Recognizer:
    def __init__(self, clientId=None, speech_recognizer=None, lastIndex=0, threadId=0, condition=None,queue=None):
        threading.Thread.__init__(self)
        self.clientId = clientId
        self.threadId = threadId
        self.speech_recognizer = speech_recognizer
        self.lastIndex = lastIndex
        self.condition = condition
        self.queue = queue

    def run(self):
        fileIndex = self.lastIndex
        createFile(clientId=self.clientId)
        if not self.queue.empty():
            self.condition.acquire()
            r = self.speech_recognizer
            audio = self.queue.get()
            logging.debug('Getting ' + str(audio)
                          + ' : ' + str(self.queue.qsize()) + ' items in queue')
            # audio = 'recording-%i.wav' % fileIndex
            path = self.clientId + "/" + audio
            if not os.access(path, os.R_OK):
                self.condition.wait(0.1)
            if os.path.isfile(path):
                print('we are reading ' + path)
                try:
                    with sr.AudioFile(path) as source:
                        audio = r.record(source)
                except IOError as e:
                    print(e)
                    pass
                try:
                    text = r.recognize_google(audio, language="en-US")
                    writeToFile(text + "\n", self.clientId, "a+")
                    print('Done!')
                    print(text)
                    fileIndex += 1
                    if text == "audio stop":
                        fileIndex = 0

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
                self.condition.release()

        return self.queue

    def sleep(self, n):
        time.sleep(n)


if __name__ == "__main__":
    r = sr.Recognizer()
    r.energy_threshold = 4000
    fileIndex = 0
    sp_worker = Recognizer("Sources",r, 0, 1)
