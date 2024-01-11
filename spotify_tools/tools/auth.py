import logging; log = logging.getLogger(__name__)  # fmt: skip

import click
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup

from . import api


@click.command()
@click.pass_context
def auth(ctx):
    spotify = ctx.obj
    print(f"Signed in as {spotify.me()['display_name']}")
