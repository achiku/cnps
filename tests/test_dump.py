# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from click.testing import CliRunner


def test_find_user_urls():
    from cnps.dump import find_user_urls
    urls = []
    with open('./data/connpass_user_list.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        urls = find_user_urls(soup)
    assert len(urls) == 32


def test_find_user_detail():
    from cnps.dump import find_user_details
    user = {}
    with open('./data/connpass_user_detail.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        user = find_user_details(soup, 'https://connpass.com/user/KeisukeKogure/')
    assert user['user_id'] == 'KeisukeKogure'


def test_dump_user_data():
    from cnps.cli import dump
    runner = CliRunner()
    result = runner.invoke(dump, ['https://fintech-engineers-drink-up.connpass.com/event/56057/'])
    print(result.output)
