# -*- coding: utf-8 -*-
import click


def find_user_urls(soup):
    tbl = soup.find('div', class_='lottery_table_area')
    users = tbl.find_all('a', class_='image_link')
    user_urls = []
    for u in users:
        user_urls.append(u['href'])
    return user_urls


@click.group()
@click.pass_context
def cli(ctx):
    """connpass CLI group"""
    pass


@cli.command(help="dump basic user data")
@click.argument('url', required=True)
def dump(url):
    click.echo("hello assholes! {0}".format(url))
