from PyInquirer import prompt

from setting import Settings
from spotify.add import SpotifyAdd
from spotify.auth import auth as sp_auth
from spotify.get_playlists import SpotifyPlaylist
from spotify.local import SpotifyLocal
from youtube.auth import auth as yt_auth
from youtube.get_playlists import YoutubePlaylist
from youtube.local import YoutubeLocal


def youtube():
    api = yt_auth()
    playlist = YoutubePlaylist(api)
    return api, playlist.getElements()


def spotify():
    token = sp_auth()
    playlist = SpotifyPlaylist(token)
    return token, playlist.getElements()


def main():
    print("================ YouTube ================")
    yt = youtube()
    print()

    print("================ Spotify ================")
    sp = spotify()
    print()

    print("=============== Analizing ===============")
    YoutubeLocal(yt)
    items = SpotifyLocal(sp).getListToSync()
    print()

    print("============= Synchronizing =============")
    length = len(items)
    if length > 0:
        if not Settings.getInstance().getSettings().get("skip"):
            if not prompt(
                {
                    "type": "confirm",
                    "name": "Apply",
                    "message": f"Add {length} tracks to Spotify playlist?",
                }
            )["Apply"]:
                exit()

        SpotifyAdd(sp).addItems(items)
    print("There is nothing to sync.")


if __name__ == "__main__":
    main()
