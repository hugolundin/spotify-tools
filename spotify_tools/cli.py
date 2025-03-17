import logging; log = logging.getLogger(__name__)  # fmt: skip

import os
import sys

import click
import dotenv

from .tools import api


@click.group()
@click.option("--spotify-client-id", envvar="SPOTIFY_CLIENT_ID")
@click.option("--spotify-client-secret", envvar="SPOTIFY_CLIENT_SECRET")
@click.option(
    "--level", type=click.Choice(logging._nameToLevel.keys()), default="WARNING"
)
@click.pass_context
def cli(ctx, spotify_client_id, spotify_client_secret, level):
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

    if spotify_client_id and spotify_client_secret:
        ctx.obj = api.spotify(spotify_client_id, spotify_client_secret)
    else:
        log.error("No authentication provided.")
        exit(1)


from .tools.auth import auth
from .tools.copy import copy
from .tools.backup import backup
from .tools.playlist import playlist

cli.add_command(backup)
cli.add_command(copy)
cli.add_command(playlist)
cli.add_command(auth)

if __name__ == "__main__":
    cli()
