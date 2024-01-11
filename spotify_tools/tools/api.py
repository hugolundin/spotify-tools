import logging; log = logging.getLogger(__name__)  # fmt: skip

import re
from urllib.parse import urljoin, urlparse

import spotipy

SPOTIFY_LIKED_SONGS = "Liked Songs"
SPOTIFY_REDIRECT_URI = "http://localhost:8000"

SPOTIFY_SCOPE = (
    "user-library-read,"
    "playlist-read-private,"
    "playlist-read-collaborative,"
    "playlist-modify-private,"
    "playlist-modify-public"
)


def spotify(spotify_client_id, spotify_client_secret):
    s = spotipy.Spotify(
        auth_manager=spotipy.oauth2.SpotifyOAuth(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope=SPOTIFY_SCOPE,
        )
    )

    logging.info(f"Signed in as {s.me()['display_name']}")
    return s


def playlists(spotify: spotipy.Spotify):
    response = spotify.current_user_playlists()

    while response:
        for item in response["items"]:
            yield item

        response = spotify.next(response)


def playlist(spotify: spotipy.Spotify, playlist_id: str):
    return spotify.playlist(playlist_id)


def get_playlist_id_from_name(spotify, name):
    for playlist in playlists(spotify):
        if playlist["name"] == name:
            return playlist["id"]

    return None


def get_playlist_id_from_url(url):
    return urljoin(url, urlparse(url).path).split("/")[-1]


def _get_tracks(response):
    for data in response.get("items", []):
        track = data.get("track")
        if not track:
            continue

        name = track.get("name")
        if not name:
            continue

        artists = [
            artist
            for artist in [artist.get("name") for artist in track.get("artists", [])]
            if artist
        ]
        if not artists:
            continue

        urls = track.get("external_urls")
        if not urls:
            continue

        uri = urls.get("spotify")
        if not uri:
            continue

        yield name, artists, uri


def get_all_tracks(spotify: spotipy.Spotify, regex: str = None):
    for playlist in playlists(spotify):
        if regex and not re.match(regex, playlist["name"]):
            logging.info(f"Skipping '{playlist['name']}'")
            continue

        logging.info(f"Downloading '{playlist['name']}'")
        response = spotify.playlist_tracks(playlist["id"])

        while response:
            for track in _get_tracks(response):
                yield *track, playlist["name"]

            response = spotify.next(response)

    if regex and not re.match(regex, SPOTIFY_LIKED_SONGS):
        return

    logging.info(f"Downloading '{SPOTIFY_LIKED_SONGS}'")
    response = spotify.current_user_saved_tracks()
    while response:
        for track in _get_tracks(response):
            yield *track, SPOTIFY_LIKED_SONGS

        response = spotify.next(response)


def get_playlist_tracks(spotify: spotipy.Spotify, playlist):
    response = spotify.playlist_tracks(playlist["id"])

    while response:
        for track in _get_tracks(response):
            yield track

        response = spotify.next(response)
