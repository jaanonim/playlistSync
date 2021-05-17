import json
import os

file_name = "token.json"


def auth():
    print("Autoryzowenie...")
    try:
        f = open(file_name)
        data = json.load(f)
        token = data["token"]
        f.close()
        if token == None:
            raise Exception
    except Exception as e:
        token = input("Enter spotify token: ")
        with open(file_name, "w") as json_file:
            json.dump({"token": token}, json_file)
    return token


def onInvalidToken():
    print("ERROR: Invalid token!")
    os.remove(file_name)
    exit()
