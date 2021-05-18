from setting import Settings

from .search import SpotifySearcher


class SpotifyLocal:
    def __init__(self, spotify):
        token, playlist = spotify

        self.settingsObj = Settings.getInstance()
        self.settings = self.settingsObj.getSettings()
        self.sp_searcher = SpotifySearcher(token)

        items = self.settings.get("items")
        self.needToBeAdded = []
        foundSucces = 0
        foundFalure = 0
        toSync = 0

        if not items:
            items = []
        if len(items) > 0:
            for i in items:
                yt = i.get("yt")
                sp = i.get("sp")
                if yt:
                    if sp:
                        if sp == "-":
                            continue
                        f = True
                        for p in playlist:
                            a, b = p
                            if [a, b] == sp:
                                f = False
                                break
                        if not f:
                            continue
                        else:
                            toSync += 1
                            self.needToBeAdded.append(sp)
                    else:
                        v = self.sp_searcher.find(yt)
                        if v:
                            foundSucces += 1
                            i["sp"] = v
                            self.needToBeAdded.append(v)
                        else:
                            foundFalure += 1
                            i["sp"] = "-"
                else:
                    print("ERROR: something went wrong")
                    exit()
        else:
            print("ERROR: Playlist setting is empty")
            exit()
        print(
            f"Spotify: Found {foundSucces}/{foundSucces+foundFalure} new tarcks and {toSync} old that need to be sync."
        )
        self.settings["items"] = items
        self.settingsObj.setSettings(self.settings)

    def getListToSync(self):
        return self.needToBeAdded
