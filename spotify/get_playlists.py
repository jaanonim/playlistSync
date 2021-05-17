import requests
from PyInquirer import prompt
from setting import Settings

from .auth import onInvalidToken


class SpotifyPlaylist:
    def __init__(self, token):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        settingsObj = Settings.getInstance()
        s = settingsObj.getSettings()
        if s.get("sp_id"):
            self.id = s.get("sp_id")
        else:
            self.id = self.getId()
            s["sp_id"] = self.id
            settingsObj.setSettings(s)

    def getId(self):
        url = "https://api.spotify.com/v1/me/playlists"
        res = requests.get(url, headers=self.headers)

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
        return id["Select Playlist"]

    def getElements(self):
        print("Getting elements of playlist...")

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
            headers=self.headers,
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
