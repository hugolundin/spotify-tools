import logging

log = logging.getLogger(__name__)

import itertools
import os
import sys

import click
import dotenv
import pandas
import spotipy

SPOTIFY_SCOPE = "user-library-read,playlist-read-private,playlist-read-collaborative"
SPOTIFY_REDIRECT_URI = "http://localhost:8000"


def playlists(spotify: spotipy.Spotify):
    response = spotify.current_user_playlists()

    while response:
        for item in response["items"]:
            yield item

        response = spotify.next(response)


def tracks(spotify: spotipy.Spotify):
    def get_tracks(response):
        for data in response.get("items", []):
            track = data.get("track")
            if not track:
                continue

            name = track.get("name")
            if not name:
                continue

            artists = [
                artist
                for artist in [
                    artist.get("name") for artist in track.get("artists", [])
                ]
                if artist
            ]
            if not artists:
                continue

            yield name, artists

    for playlist in playlists(spotify):
        logging.info(f"Downloading '{playlist['name']}'")
        response = spotify.playlist_tracks(playlist["id"])

        while response:
            for track in get_tracks(response):
                yield *track, playlist["name"]

            response = spotify.next(response)

    logging.info(f"Downloading 'Liked Songs'")
    response = spotify.current_user_saved_tracks()
    while response:
        for track in get_tracks(response):
            yield *track, "Liked Songs"

        response = spotify.next(response)


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

    logging.info(f"Signed in as {spotify.me()['display_name']}")

    pandas.DataFrame(
        tracks(spotify), columns=["Name", "Artists", "Playlist"]
    ).to_parquet("spotify.parquet", compression="gzip")


if __name__ == "__main__":
    backupify()
