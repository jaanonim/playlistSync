import requests
from PyInquirer import prompt

from .auth import onInvalidToken


def getPlaysists(token):
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
    return id["Select Playlist"]


def getElementsOfPlaylist(id, token):
    items = getElementsPage(token, f"https://api.spotify.com/v1/playlists/{id}/tracks")
    elements = []
    for item in items:
        elements.append((item["track"]["uri"], item["track"]["name"]))

    return elements


def getElementsPage(token, url):
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

    items = response["items"]

    if response["next"]:
        items += getElementsPage(token, response["next"])

    return items
