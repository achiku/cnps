# -*- coding: utf-8 -*-
import json
from time import sleep

import click
import requests
from bs4 import BeautifulSoup

from . import __version__
from .dump import (DatetimeEncoder, find_user_details, find_user_event_details,
                   find_user_urls)
from .filter import (duplicate_event_filter_generator,
                     event_tab_count_filter_generator, read_user_data,
                     recent_event_interval_filter_generator,
                     social_link_filter_generator)
from .user import format_user_info

try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin


@click.group(help="cnps cli (v{0})".format(__version__))
@click.pass_context
def cli(ctx):
    """connpass CLI group"""
    pass


@cli.command(help="dump basic event applicants data")
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
        events = find_user_event_details(
            BeautifulSoup(user_res.text, 'html.parser'),
            user_url,
        )
        u['events'] = events
        user_data.append(u)
        click.echo("[{0}/{1}]: {2}".format(idx, len(user_urls), u['user_id']), err=True)
        sleep(1)
    click.echo(json.dumps(user_data, sort_keys=True, indent=2, cls=DatetimeEncoder))


@cli.command(help="filter applicants data with multiple options")
@click.argument('file-path', required=True)
@click.option('--facebook-link/--no-facebook-link', default=None)
@click.option('--github-link/--no-github-link', default=None)
@click.option('--twitter-link/--no-twitter-link', default=None)
@click.option('--duplicate-event/--no-duplicate-event', default=None)
@click.option('--own-event/--no-own-event', default=None)
@click.option('--presentation/--no-presentation', default=None)
@click.option('--avg-event-interval', default=None, type=float)
def filter(
        file_path, facebook_link, github_link, twitter_link,
        avg_event_interval, duplicate_event, own_event, presentation):
    filter_funcs = []
    if twitter_link is not None:
        filter_funcs.append(social_link_filter_generator('twitter', required=twitter_link))
    if facebook_link is not None:
        filter_funcs.append(social_link_filter_generator('facebook', required=facebook_link))
    if github_link is not None:
        filter_funcs.append(social_link_filter_generator('github', required=github_link))
    if avg_event_interval is not None:
        filter_funcs.append(recent_event_interval_filter_generator(avg_event_interval))
    if own_event is not None:
        filter_funcs.append(event_tab_count_filter_generator('num_own_events', own_event))
    if presentation is not None:
        filter_funcs.append(event_tab_count_filter_generator('num_presentations', presentation))
    if duplicate_event is not None:
        filter_funcs.append(duplicate_event_filter_generator(duplicate_event))
    user_data = read_user_data(file_path)
    users = [u for u in user_data if all([f(u) for f in filter_funcs])]
    for u in users:
        click.echo(format_user_info(u))


if __name__ == '__main__':
    cli()
