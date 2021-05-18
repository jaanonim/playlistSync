import requests

from spotify.auth import auth as sp_auth
from spotify.auth import onInvalidToken


def main():
    token = sp_auth()
    while True:
        url = input("Enter url:").strip()
        url = url.replace("https://open.spotify.com/track/", "").strip()
        id, _ = url.split("?")
        makeRequest(token, id)


def makeRequest(token, id):
    url = f"https://api.spotify.com/v1/tracks/{id}"
    res = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )

    if res.status_code != 200:
        if res.status_code == 404:
            print("ERROR: Cannot find track.")
            exit()
        onInvalidToken()

    response = res.json()

    print(f'["{response["uri"]}","{response["name"]}"]')


if __name__ == "__main__":
    main()
