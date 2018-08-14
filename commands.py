import logging
import os
import threading
import re
import queue

CONST_REPLACE_COMMAND = ""
CONST_DELETE_COMMAND = ""
CONST_INSERT_COMMAND = ""


def command_filter(line, pos_start,pos_stop=None):
    if pos_stop is None:
        return line[:pos_start]
    else :
        return line[:pos_start].append(line[x] for x in range(pos_stop,len(line)-1))


def read_last_line(path):
    with open(path, "r") as f:
        lineList = f.readlines()
        if len(lineList) > 0:
            return lineList[len(lineList) - 1]
        else:
            return ""


def line_to_list(line):
    return line.split(' ')


def save_line(line, path):
    """
    save the last modified line in file
    :param line:
    :param path:
    :return: return zero to indicate that all is clear
    """
    text = ""
    for x in line:
        text = text + x + " "
    list = open(path).read().splitlines()
    list[len(list) - 1] = text
    with open(path, "w") as f:
        for x in list:
            f.write(x + "\n")
    return 0


def read_all(path):
    listing = []
    with open(path, 'r') as f:
        for line in f:
            myfile = myfile + str(line + ' ')
            listing.append(line)
        text = myfile
        myfile = myfile.split(' ')
        myfile.pop(len(myfile) - 1)
    return myfile, listing, text


def replaceWord(item, code, word, list_word, path):
    # TODO : to implement this function to be called when we have replace request
    if item is not None:
        if type(item) == int:
            if code in [-1, -2, -3]:
                list_word.pop(item)
                list_word.insert(item, word)
                print(list_word)
        if type(item) == str and code == -4:
            while item in list_word:
                pos = list_word.index(item)
                list_word.pop(pos)
                list_word.insert(pos, word)
                print(list_word)

        else:
            print("prog closed")
    save_line(list_word, path)


def delete(item, code, list_word, path):
    if item is not None:
        if type(item) == str:
            if code == -3:
                while item in list_word:
                    # Slow performing
                    # list_word.remove(word_to_delete)
                    # Better performing
                    list_word.pop(list_word.index(item))
                    print(list_word)
        if type(item) == int:
            if code in [-4, -2]:
                list_word.pop(item)
                print(list_word)
        if code == -1:
            list_word.pop(item - 1)
            print(list_word)
    print("please specify the word to delete")
    save_line(list_word, path)


def insert(word_to_add, item, list_word, path):
    # TODO : define the position of the word to insert : DONE
    if type(item) == int:
        list_word.insert(item, word_to_add)
        print(list_word)
    if type(item) == str:
        list_word.append(word_to_add)
        print(list_word)
    print("saving new line")
    save_line(list_word, path)


def pattern_finder(line):
    insert_request = False
    delete_request = False
    replace_request = False
    matchObj_insert = re.match(r'(.*)insert (.*?) (.*?) (.*)', line, re.M and re.I)
    matchObj_delete = re.match(r'(.*)delete (.*?) (.*?) (.*)', line, re.M and re.I)
    matchObj_replace = re.match(r'(.*)replace (.*?) (.*?) (.*?) (.*)', line, re.M and re.I)
    # Let's assume there's a simple word  to  specify
    if matchObj_insert:
        insert_request = True
        print("insert_request = True")

    if matchObj_delete:
        delete_request = True
        print("delete_request = True")
    if matchObj_replace:
        replace_request = True
        print("replace_request = True")
    else:
        print("We have no match")
    return insert_request, delete_request, replace_request, (matchObj_insert or
                                                             matchObj_delete or
                                                             matchObj_replace),


class CommandManager:

    def __init__(self, queue_command=None, path=None):
        self.line = ""
        self.list = line_to_list(self.line)
        if not queue_command is None:
            self.queue_command = queue_command
        else:
            self.queue_command = queue.Queue()
            self.queue_command.put(path)
        # thread = threading.Thread(target=self.run_match, args=())
        # thread.daemon = True
        # thread.start()
        print('commandManger is running .... ')

    def run_match(self):
        # TODO : implement the insert checker :DONE
        # TODO : implement the delete checker : partially DONE (Done = 7/18 ; 9:41 PM )
        # TODO : implement the replace checker : DONE = 7/18 ; 11:03 AM
        # TODO : implement it as a service : infinite loop
        while True:
            # if not self.queue_command.empty():
            if True:
                # path = self.queue_command.get()
                path = os.path.join('', "Transcribe.txt")
                if os.path.isfile(path):
                    print("File exist .......................................")
                logging.debug('Getting ' + str(path)
                              + ' : ' + str(self.queue_command.qsize()) + ' items in self.queue_command')
                self.line = read_last_line(path)
                self.list = line_to_list(self.line)
                insert_request, delete_request, replace_request, matchObj = pattern_finder(self.line)
                try:
                    if matchObj:
                        print("we have match............")
                        if "before" in matchObj.group(3).lower():
                            string = matchObj.group(4)
                            print("inserting before  : " + string)
                            # TODO  : We have to call replace function : DONE !
                            # TODO : filter the command from the text and eliminate it

                            if replace_request:
                                pos_start = self.list.inde("replace")
                                self.list = command_filter(self.list, pos_start)
                                replaceWord(self.list.index(string), -1, matchObj.group(5).split(' ')[1], self.list,
                                            path)
                                return self.queue_command
                            # TODO : Define the condition to call delete and insert functions
                            if delete_request:
                                delete(self.list.index(string), -1, self.list, path)
                            if insert_request:
                                pos_start = self.list.index("insert")
                                self.list = command_filter(self.list, pos_start)
                                insert(matchObj.group(2), (self.list.index(string)), self.list, path)
                                return self.queue_command
                        if "after" in matchObj.group(3).lower():
                            string = matchObj.group(4)
                            print("...........inserting after : " + string)

                            # TODO  : We have to call replace function : DONE !
                            if replace_request:
                                pos_start = self.list.inde("replace")
                                self.list = command_filter(self.list, pos_start)
                                replaceWord(self.list.index(string), -2, matchObj.group(5).split(' ')[1], path)
                                return self.queue_command
                            if delete_request:
                                # TODO : there's a specification in after to clarify
                                delete((self.list.index(string) + 1), -2, self.list, path)
                            if insert_request:
                                insert(matchObj.group(2), (self.list.index(string) + 1), self.list, path)
                                return self.queue_command
                        # Insert a simple word in the the text
                        # TODO : Insert a hole phrase in the position we want
                        if insert_request and "between" in matchObj.group(3):
                            string = matchObj.group(4).lower()
                            match_between = re.match(r'(.*) and (.*)', string, re.M and re.I)
                            if match_between:
                                word1 = match_between.group(1).lower()
                                word2 = match_between.group(2).lower()
                                pos_start = self.list.index("insert")
                                pos_stop = self.list.index(word2)
                                self.list = command_filter(self.list, pos_start,pos_stop)
                                insert(matchObj.group(2), (self.list.index(word1) + 1), self.list, path)
                                return self.queue_command

                            else:
                                print("request to specification")
                        # This is a alternative for a sentence like "delete word
                        if delete_request and (matchObj.group(2) or matchObj.group(3)):
                            if "all" in matchObj.group(3).lower():
                                delete(matchObj.group(2), -3, self.list, path)
                                return self.queue_command
                            # delete last word in the phrase
                            if "last" in matchObj.group(2):
                                word = matchObj.group(3)
                                delete((len(self.list) - 1 - self.list[::-1].index(word)), -4, self.list, path)
                                return self.queue_command
                            else:
                                print("--- request more specification ----- ")
                                return None, None
                        # TODO  : We have to call replace function :DONE !
                        if replace_request:
                            string = matchObj.group(3)
                            string1 = matchObj.group(5)
                            if "last" in matchObj.group(2):
                                replaceWord((len(self.list) - 1 - self.list[::-1].index(string)), -3, string1,
                                            self.list,
                                            path)
                                return self.queue_command
                            if "all" in matchObj.group(2):
                                replaceWord(string, -4, string1, self.list, path)
                                return self.queue_command
                            else:
                                print("--- request more specification ----- ")
                                return None, None
                        else:
                            tt = matchObj.group(2)
                            return {matchObj.group(2), -1}
                    else:
                        print("no Match !! ")

                except Exception as e:
                    print(e)
                    print("there's an error ")
            else:
                print("queue is empty we are waiting ...")
            return self.queue_command


if __name__ == '__main__':
    path = os.path.join('source', "Transcribe.txt")
    print(path)
    command = CommandManager(None, path)
    command.run_match()
