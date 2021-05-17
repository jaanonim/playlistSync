import json

file_name = "settings.json"


class Settings:
    __instance = None

    @staticmethod
    def getInstance():
        if Settings.__instance == None:
            Settings()
        return Settings.__instance

    def __init__(self):

        if Settings.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Settings.__instance = self

        self.data = {}
        try:
            f = open(file_name)
            self.data = json.load(f)
            f.close()
            if self.data == {}:
                raise Exception
        except Exception as e:
            print("Cannot found " + file_name)

    def getSettings(self):
        return self.data

    def setSettings(self, data):
        self.data = data
        with open(file_name, "w") as json_file:
            json.dump(self.data, json_file)
