import logging; log = logging.getLogger(__name__)  # fmt: skip

from datetime import date

import click
import pandas

from . import api


@click.command()
@click.pass_context
def backup(ctx):
    spotify = ctx.obj["spotify"]

    pandas.DataFrame(
        api.get_all_tracks(spotify), columns=["Name", "Artists", "URI", "Playlist"]
    ).to_parquet(
        f"{date.today().isoformat()}-spotify-backup.parquet", compression="gzip"
    )
