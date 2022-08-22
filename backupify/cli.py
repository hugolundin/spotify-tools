import logging

log = logging.getLogger(__name__)

import os
import sys

import click
import dotenv
import spotipy

SPOTIFY_SCOPE = "user-library-read,playlist-read-private,playlist-read-collaborative"
SPOTIFY_REDIRECT_URI = "http://localhost:8000"


@click.command()
@click.option("--spotify-client-id", envvar="SPOTIFY_CLIENT_ID")
@click.option("--spotify-client-secret", envvar="SPOTIFY_CLIENT_SECRET")
@click.option(
    "--level", type=click.Choice(logging._nameToLevel.keys()), default="WARNING"
)
def backupify(spotify_client_id, spotify_client_secret, level):
    logging.basicConfig(
        stream=sys.stdout,
        format="%(levelname)s: %(message)s",
        level=logging._nameToLevel[level],
    )

    dotenv.load_dotenv()

    if not spotify_client_id:
        spotify_client_id = os.environ.get("SPOTIFY_CLIENT_ID")

    if not spotify_client_secret:
        spotify_client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    spotify = spotipy.Spotify(
        auth_manager=spotipy.oauth2.SpotifyOAuth(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SPOTIFY_SCOPE,
        )
    )

    backupify.run(spotify)


if __name__ == "__main__":
    backupify()
