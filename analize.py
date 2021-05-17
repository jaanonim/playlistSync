import re

from spotify.search import SpotifySearcher

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
    "live",
]


class Analize:
    def __init__(self, youtube, spotify):
        api, self.yt = youtube
        token, self.sp = spotify
        self.sp_searcher = SpotifySearcher(token)

        playlist = []
        t = 0
        f = 0
        for item in self.yt:
            i = self.findItemOnSpotify(item)
            if i:
                playlist.append({"youtube": item, "spotify": i})
                t += 1
            else:
                playlist.append({"youtube": item, "spotify": None})
                f += 1

        print(f"{t}/{f}")

    def findItemOnSpotify(self, item):
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

        return self.sp_searcher.find(name)
