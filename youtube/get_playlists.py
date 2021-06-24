from PyInquirer import prompt
from setting import Settings


class YoutubePlaylist:
    def __init__(self, api):
        self.api = api

        settingsObj = Settings.getInstance()
        s = settingsObj.getSettings()
        if s.get("yt_id"):
            self.id = s.get("yt_id")
        else:
            self.id = self.getId()
            s["yt_id"] = self.id
            settingsObj.setSettings(s)

    def getId(self):
        request = self.api.playlists().list(
            part="snippet,contentDetails", maxResults=100, mine=True
        )
        response = request.execute()
        items = response["items"]
        playlists = []
        for item in items:
            playlists.append({"name": item["snippet"]["title"], "value": item["id"]})

        id = prompt(
            {
                "type": "list",
                "name": "Select Playlist",
                "message": "Select Playlist",
                "choices": playlists,
            }
        )
        return id["Select Playlist"]

    def getElements(self):
        print("Getting elements of playlist...")

        items = self.getElementsPage()
        elements = []
        for item in items:
            elements.append(
                (item["contentDetails"]["videoId"], item["snippet"]["title"])
            )

        return elements

    def getElementsPage(self, page=None):

        request = self.api.playlistItems().list(
            part="contentDetails, snippet", playlistId=self.id, pageToken=page
        )
        try:
            response = request.execute()
        except Exception as e:
            print(e)
            exit()

        items = response["items"]
        page = response.get("nextPageToken")
        if page:
            items += self.getElementsPage(page=page)

        return items
