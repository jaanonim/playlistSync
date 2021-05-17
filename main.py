from spotify.auth import auth as sp_auth
from spotify.get_playlists import SpotifyPlaylist
from youtube.auth import auth as yt_auth
from youtube.get_playlists import YoutubePlaylist


def youtube():
    api = yt_auth()
    playlist = YoutubePlaylist(api)
    playlist.getElements()


def spotify():
    token = sp_auth()
    playlist = SpotifyPlaylist(token)
    playlist.getElements()


def main():
    print("======== YouTube ========")
    youtube()
    print("======== Spotify ========")
    spotify()


if __name__ == "__main__":
    main()
