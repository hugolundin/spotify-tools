# backupify

Backup Spotify playlists to a Parquet file.

## Setup

Start by [registering a new Spotify application](https://developer.spotify.com/dashboard/). Copy the generated `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`.

---

The first alternative is to set them in the current environment:

```bash
$ export SPOTIFY_CLIENT_ID='<client id>'
$ export SPOTIFY_CLIENT_SECRET='<client secret>'
```

---

The second alternative is to put the keys in a file, named `.env`:

```bash
SPOTIFY_CLIENT_ID='<client id>'
SPOTIFY_CLIENT_SECRET='<client secret>'
```

It will be automatically read when `backupify` is run.

---

The third alternative is to pass the keys as arguments to `backupify`. This is less secure, because keys will be persisted in your shell history.

## Usage

```bash
$ backupify --help
Usage: backupify [OPTIONS]

Options:
  --spotify-client-id TEXT
  --spotify-client-secret TEXT
  --level [CRITICAL|FATAL|ERROR|WARN|WARNING|INFO|DEBUG|NOTSET]
  --help                          Show this message and exit.
```

Setting the level to `INFO` will give you information about what playlist is currently being downloaded.

After running `backupify`, you will find a file named `YYYY-mm-dd-spotify.parquet` in the directory where the program was invoked. It can be queried using DuckDB:

```
D select Playlist, Count(Name) Songs from '*.parquet' where list_contains(Artists, 'The Go! Team') group by Playlist;
┌─────────────────────────┬───────┐
│        Playlist         │ Songs │
├─────────────────────────┼───────┤
│ Juli (2021)             │ 1     │
│ Juni (2021)             │ 1     │
│ Maj (2021)              │ 1     │
│ Juli 2020               │ 2     │
│ April 2019              │ 1     │
│ Oktober 2018            │ 1     │
│ Februari 2018           │ 12    │
│ Discover Weekly Archive │ 6     │
│ Your Top Songs 2019     │ 1     │
│ Your Top Songs 2018     │ 1     │
│ GO! TEAM FAVOURITES     │ 57    │
│ Liked Songs             │ 21    │
└─────────────────────────┴───────┘
```
