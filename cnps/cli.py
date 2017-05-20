# -*- coding: utf-8 -*-
import json
from time import sleep
try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin

import click
import requests
from bs4 import BeautifulSoup

from . import __version__
from .dump import find_user_details, find_user_urls, DatetimeEncoder


@click.group(help="cnps cli (v{0})".format(__version__))
@click.pass_context
def cli(ctx):
    """connpass CLI group"""
    pass


@cli.command(help="dump basic user data")
@click.argument('event-url', required=True)
def dump(event_url):
    participant_url = urljoin(event_url, 'participation')
    event_res = requests.get(participant_url)
    event_body = BeautifulSoup(event_res.text, 'html.parser')

    user_data = []
    user_urls = find_user_urls(event_body)
    for idx, user_url in enumerate(user_urls):
        user_res = requests.get(user_url)
        u = find_user_details(
            BeautifulSoup(user_res.text, 'html.parser'),
            user_url,
        )
        user_data.append(u)
        click.echo("[{0}/{1}]: {2}".format(idx, len(user_urls), u['user_id']), err=True)
        sleep(1)
    click.echo(json.dumps(user_data, sort_keys=True, indent=2, cls=DatetimeEncoder))


if __name__ == '__main__':
    cli()
