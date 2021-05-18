from setting import Settings


class YoutubeLocal:
    def __init__(self, youtube):
        api, playlist = youtube
        self.settingsObj = Settings.getInstance()
        self.settings = self.settingsObj.getSettings()
        items = self.settings.get("items")
        if not items:
            items = []

        newItems = 0

        if len(items) > 0:
            for p in playlist:
                f = True
                for i in items:
                    element = i.get("yt")
                    if element:
                        a, b = p
                        if [a, b] == element:

                            f = False
                            break
                    else:
                        print("ERROR: something went wrong")
                        exit()
                if f:
                    newItems += 1
                    items.append({"yt": p})
        else:
            for p in playlist:
                items.append({"yt": p})
        print(f"YouTube: Found {newItems} new tracks.")
        self.settings["items"] = items
        self.settingsObj.setSettings(self.settings)
