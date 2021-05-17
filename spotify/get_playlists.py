import requests
from PyInquirer import prompt

from .auth import onInvalidToken


class SpotifyPlaylist:
    def __init__(self, token):
        self.token = token
        url = "https://api.spotify.com/v1/me/playlists"
        res = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(token),
            },
        )

        if res.status_code != 200:
            onInvalidToken()
        response = res.json()
        playlists = []
        for item in response["items"]:
            playlists.append({"name": item["name"], "value": item["id"]})

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
        items = self.getElementsPage(
            f"https://api.spotify.com/v1/playlists/{self.id}/tracks"
        )
        elements = []
        for item in items:
            elements.append((item["track"]["uri"], item["track"]["name"]))

        return elements

    def getElementsPage(self, url):
        res = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
        )

        if res.status_code != 200:
            if res.status_code == 404:
                print("ERROR: Cannot find playlist.")
                exit()
            onInvalidToken()

        response = res.json()

        items = response["items"]

        if response["next"]:
            items += self.getElementsPage(response["next"])

        return items
