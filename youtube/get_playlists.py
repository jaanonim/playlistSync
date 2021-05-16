from PyInquirer import prompt


def getPlaylists(youtube):

    request = youtube.playlists().list(
        part="snippet,contentDetails", maxResults=20, mine=True
    )
    response = request.execute()
    items = response["items"]
    playlists = []
    for item in items:
        playlists.append({"name": item["snippet"]["title"], "value": item["id"]})

    id = prompt(
        {
            "type": "list",
            "name": "Select Playlist",
            "message": "Select Playlist",
            "choices": playlists,
        }
    )
    return id["Select Playlist"]


def getElementsOfPlaylist(id, youtube):
    items = getElementsPage(id, youtube)
    elements = []
    for item in items:
        elements.append((item["contentDetails"]["videoId"], item["snippet"]["title"]))

    return elements


def getElementsPage(playlistId, youtube, page=None):

    request = youtube.playlistItems().list(
        part="contentDetails, snippet", playlistId=playlistId, pageToken=page
    )
    response = request.execute()

    items = response["items"]
    page = response.get("nextPageToken")
    if page:
        items += getElementsPage(playlistId, youtube, page=page)

    return items
