# -*- coding: utf-8 -*-
import pytest
from click.testing import CliRunner


def test_filter():
    from cnps.cli import filter as fil
    runner = CliRunner()
    result = runner.invoke(fil, ['./data/user.json'])
    print(result.output)


def test_read_user_data():
    from cnps.filter import read_user_data
    user_data = read_user_data('./data/user.json')
    print(user_data)


@pytest.mark.parametrize("links, target, required, expected", [
    (
        [
            {'twitter': 'https://twitter/_achiku'}
        ], 'twitter', True, True
    ),
    (
        [
            {'twitter': 'https://twitter/_achiku'}
        ], 'twitter', False, False
    ),
    (
        [
            {'twitter': 'https://twitter/_achiku'}
        ], 'facebook', True, False
    ),
    (
        [
            {'twitter': 'https://twitter/_achiku'}
        ], 'facebook', False, True
    ),
])
def test_social_link_filter_generator(links, target, required, expected):
    from cnps.filter import social_link_filter_generator
    user = {'social_links': links}
    f = social_link_filter_generator(target, required=required)
    assert f(user) == expected
