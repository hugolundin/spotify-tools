import logging; log = logging.getLogger(__name__)  # fmt: skip

import click
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup

from . import api


@click.command()
@optgroup.group("playlist", cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option("--name", help="Name to find the id for.")
@optgroup.option("--url", help="URL to extract the id from.")
@click.pass_context
def playlist(ctx, name, url):
    spotify = ctx.obj

    if name:
        if pid := api.get_playlist_id_from_name(spotify, name):
            print(pid)
        else:
            log.info(f"No matches for playlist name '{name}'.")
    else:
        if pid := api.get_playlist_id_from_url(url):
            print(pid)
        else:
            log.info(f"Unable to extract id from url '{url}'.")
