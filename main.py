from spotify.auth import auth
from youtube.auth import auth
from youtube.get_playlists import getElementsOfPlaylist, getPlaylists


def youtube():
    api = auth()
    id = getPlaylists(api)
    getElementsOfPlaylist(id, api)


def spotify():
    auth()


def main():
    spotify()


if __name__ == "__main__":
    main()
