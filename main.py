from spotify import get_playlists as sp_playlists
from spotify.auth import auth as sp_auth
from youtube import get_playlists as yt_playlists
from youtube.auth import auth as yt_auth


def youtube():
    api = yt_auth()
    id = yt_playlists.getPlaylists(api)
    yt_playlists.getElementsOfPlaylist(id, api)


def spotify():
    token = sp_auth()
    id = sp_playlists.getPlaysists(token)
    sp_playlists.getElementsOfPlaylist(id, token)


def main():
    youtube()
    spotify()


if __name__ == "__main__":
    main()
