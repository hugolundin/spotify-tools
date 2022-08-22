import logging; log = logging.getLogger(__name__)  # fmt: skip

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
    ctx.obj["spotify"] = api.spotify(spotify_client_id, spotify_client_secret)


from .tools.copy import copy
from .tools.backup import backup

cli.add_command(backup)
cli.add_command(copy)

if __name__ == "__main__":
    cli(obj={})
