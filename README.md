# Spotify Tools

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

It will be automatically read when `spotify-tools` is run.

---

The third alternative is to pass the keys as arguments to `spotify-tools`. This is less secure, because keys will be persisted in your shell history.

## Usage

```bash
$ spotify-tools --help
Usage: spotify-tools [OPTIONS]

Options:
  --spotify-client-id TEXT
  --spotify-client-secret TEXT
  --level [CRITICAL|FATAL|ERROR|WARN|WARNING|INFO|DEBUG|NOTSET]
  --help                          Show this message and exit.

Commands:
    backup
    copy
```
