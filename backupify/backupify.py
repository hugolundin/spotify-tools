import logging

log = logging.getLogger(__name__)

import pandas
import spotipy


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


def run(spotify):
    logging.info(f"Signed in as {spotify.me()['display_name']}")

    pandas.DataFrame(
        tracks(spotify), columns=["Name", "Artists", "Playlist"]
    ).to_parquet("spotify.parquet", compression="gzip")
