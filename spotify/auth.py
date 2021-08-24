import json
import os

import spotipy
import spotipy.oauth2 as oauth2

file_name = "spotify.json"


def auth():
    print("Autoryzowenie...")
    try:
        f = open(file_name)
        data = json.load(f)
        f.close()
        if data == {}:
            raise Exception
    except Exception as e:
        print("Cannot found " + file_name)
        exit()

    credentials = oauth2.SpotifyClientCredentials(
        client_id=data["clientID"], client_secret=data["clientSecret"]
    )
    token = credentials.get_access_token()
    return token["access_token"]


def onInvalidToken():
    print("ERROR: Invalid token!")
    exit()
