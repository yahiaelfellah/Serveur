import speech_recognition as sr
import os.path as pth
import time

r = sr.Recognizer()
r.energy_threshold = 4000
fileIndex = 0

while True:

    if pth.isfile('recording-' + str(fileIndex) + '.wav'):
        start_time = time.time()
        audio = 'recording-' + str(fileIndex) + '.wav'
        try:
            with sr.AudioFile(audio) as source:
                audio = r.record(source)
        except Exception as e:
            continue

        try:
            text = r.recognize_google(audio, language="en-US")
            f = open("C:/Users/User10/stage/Transcibe.txt", "a+")
            f.write(text + "\n")
            f.close
            print('Done!')
            elapsed_time = time.time() - start_time
            print('Elapsed Time: ', elapsed_time)
            print(text)
            if text == "audio stop":
                fileIndex = 0

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            f = open("Transcibe.txt", "a+")
            f.write("Google Speech Recognition could not understand audio" + "\n")
            f.close
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            f = open("Transcibe.txt", "a+")
            f.write("Could not request results from Google Speech Recognition service" + "\n")
            f.close
        except Exception as e:
            print(e)

        fileIndex = fileIndex + 1
