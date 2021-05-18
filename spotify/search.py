import re

import requests

from .auth import onInvalidToken

INLEGAL_CHARS = "|(){}[]\\/@»&~"
INLEGAL_WORLDS = [
    "official",
    "oficial",
    "video",
    "lyrics",
    "ft",
    "feat",
    "audio",
    "seperate altogether acoustic",
    "official live room session",
    "live @ colour conference 2018",
]


class SpotifySearcher:
    def __init__(self, token):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def makeRequest(self, query):
        url = f"https://api.spotify.com/v1/search?q={query}&type=artist,track"
        res = requests.get(url, headers=self.headers)

        if res.status_code != 200:
            if res.status_code == 404:
                print("ERROR: Cannot find track.")
                exit()
            onInvalidToken()

        response = res.json()

        items = response["tracks"]["items"]
        if len(items):
            return (items[0]["uri"], items[0]["name"])

    def find(self, item):
        id, name = item
        name = name.strip().lower()
        for char in INLEGAL_CHARS:
            name = name.replace(char, "")

        name = re.sub("(HD|HQ|720p|1080p|4k)*", "", name)
        name = re.sub("([oO]f+icial *)?([Mm]usic *)?[Vv]ideo", "", name)
        name = re.sub("[lL]yrics?", "", name)
        name = re.sub("([Ff]eat|[fF]t|[fF]eaturing)\..*$", "", name)
        name = re.sub("[Ww]ith.*$", "", name)

        for word in INLEGAL_WORLDS:
            name = name.replace(word, "")

        return self.makeRequest(name)
