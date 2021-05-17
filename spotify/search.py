import requests

from .auth import onInvalidToken


class SpotifySearcher:
    def __init__(self, token):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    def find(self, query):
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
