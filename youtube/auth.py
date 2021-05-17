import os

import googleapiclient.discovery
import googleapiclient.errors
from oauth2client import client, file, tools

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def auth():
    print("Autoryzowenie...")

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    store = file.Storage("credentials.json")
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secrets_file, scopes)
        credentials = tools.run_flow(flow, store)

    return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )
