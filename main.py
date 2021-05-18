from analize import Analize

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
    print("======== YouTube ========")
    yt = youtube()
    print("======== Spotify ========")
    sp = spotify()

    print("======== Analize ========")
    YoutubeLocal(yt)
    print("Searching for items in Spotify ...")
    SpotifyLocal(sp)


if __name__ == "__main__":
    main()
