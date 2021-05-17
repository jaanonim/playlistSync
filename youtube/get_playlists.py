from PyInquirer import prompt


class YoutubePlaylist:
    def __init__(self,api):
        self.api = api

        request = self.api.playlists().list(
            part="snippet,contentDetails", maxResults=20, mine=True
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
        self.id = id["Select Playlist"]

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
        response = request.execute()

        items = response["items"]
        page = response.get("nextPageToken")
        if page:
            items += self.getElementsPage(page=page)

        return items
