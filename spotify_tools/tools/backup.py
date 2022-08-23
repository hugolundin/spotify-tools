import logging; log = logging.getLogger(__name__)  # fmt: skip

from datetime import date

import click
import pandas

from . import api


@click.command()
@click.pass_context
@click.option("--regex", type=str, default="")
def backup(ctx, regex):
    spotify = ctx.obj

    pandas.DataFrame(
        api.get_all_tracks(spotify, regex=regex),
        columns=["Name", "Artists", "URI", "Playlist"],
    ).to_parquet(
        f"{date.today().isoformat()}-spotify-backup.parquet", compression="gzip"
    )
