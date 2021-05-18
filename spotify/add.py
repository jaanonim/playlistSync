import json

import requests
from progress.bar import IncrementalBar
from setting import Settings

from .auth import onInvalidToken


class SpotifyAdd:
    def __init__(self, spotify):
        token, _ = spotify
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        self.id = Settings.getInstance().getSettings()["sp_id"]

    def addItems(self, items):
        print("Adding tracks to spotify:")
        bar = IncrementalBar("", max=len(items))
        i = 0
        part = []
        for item in items:
            bar.next()
            part.append(item[0])
            i += 1
            if i == 10:
                self.__add(part)
                part = []
                i = 0
        if len(part) > 0:
            self.__add(part)

    def __add(self, part):
        url = f"https://api.spotify.com/v1/playlists/{self.id}/tracks"
        res = requests.post(url, headers=self.headers, data=json.dumps({"uris": part}))

        if res.status_code != 201:
            if res.status_code == 401:
                onInvalidToken()
            print(res.json())
            print("ERROR: Somethig went wrong.")
            exit()
