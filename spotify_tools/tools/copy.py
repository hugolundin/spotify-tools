import logging; log = logging.getLogger(__name__)  # fmt: skip

import click

from . import api


@click.command()
@click.argument("source_playlist_id")
@click.argument("target_playlist_id")
@click.option("--confirm/--no-confirm", show_default=True, default=True)
@click.pass_context
def copy(ctx, source_playlist_id, target_playlist_id, confirm):
    spotify = ctx.obj
    source = api.playlist(spotify, source_playlist_id)
    target = api.playlist(spotify, target_playlist_id)

    tracks = [track[2] for track in api.get_playlist_tracks(spotify, source)]

    if not confirm or click.confirm(
        f"Do you want to copy {len(tracks)} tracks from {source['name']} to {target['name']}?",
        default=False,
    ):
        spotify.playlist_add_items(target["id"], tracks)
