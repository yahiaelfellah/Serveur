import json
import sys

# TODO : General :  function like exist must be called one time for the same client
# TODO : define a global variable that holds a boolean  indicates the same client or not

same = True


def init():
    data = {"server": []}
    with open("data.txt", "wt") as f:
        json.dump(data, f)


def same_client(oldclient, newclient):
    return oldclient is newclient


def save_user(clientId, lastIndex):
    exist, position = user_exist(clientId)
    if exist:
        print("user exist :p !!!!")
        return
    else:
        print("Adding User")
        with open("data.txt", "r") as read_file:
            try:
                data = json.load(read_file)
            except json.JSONDecodeError as e:
                print(e)
                sys.exit()
            userdata = {"clientId": clientId, "lastIndex": lastIndex}
            data["server"].append(userdata)
            with open("data.txt", "w") as write_file:
                json.dump(data, write_file)


def get_userId(index):
    with open("data.txt", "r") as read_file:
        try:
            data = json.load(read_file)
        except json.JSONDecodeError as e:
            print(e)
            sys.exit()
        return data["server"][index]["clientId"]


def user_exist(clientId):
    with open("data.txt", "r") as read_file:
        try:
            data = json.load(read_file)
        except json.JSONDecodeError as e:
            print(e)
            sys.exit()
    users = data["server"]
    index = 0
    for x in users:
        if x["clientId"] is clientId:
            return True, index
        index += 1
    return False, -1


def get_lastIndex(clientId):
    exist, position = user_exist(clientId)
    if exist:
        with open("data.txt", "r") as read_file:
            try:
                data = json.load(read_file)
            except json.JSONDecodeError as e:
                print(e)
                sys.exit()
            return data["server"][position]["lastIndex"]


def save_lastIndex(clientId, index):
    exist, position = user_exist(clientId)
    if exist:
        with open("data.txt", "r") as read_file:
            try:
                data = json.load(read_file)
            except json.JSONDecodeError as e:
                print(e)
                sys.exit()
        data["server"][position]["lastIndex"] = index
        with open("data.txt", "w") as write_file:
            json.dump(data, write_file)


if __name__ == "__main__":
    init()
    save_user(1, 2)
    print(user_exist(1))
