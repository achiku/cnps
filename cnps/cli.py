# -*- coding: utf-8 -*-
import click

from . import __version__


@click.group(help="cnps cli (v{0})".format(__version__))
@click.pass_context
def cli(ctx):
    """connpass CLI group"""
    pass


@cli.command(help="dump basic user data")
@click.argument('event-url', required=True)
def dump(event_url):
    click.echo("hello assholes! {0}".format(event_url))


if __name__ == '__main__':
    cli()
