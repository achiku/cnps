# -*- coding: utf-8 -*-
from datetime import date
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


@pytest.mark.parametrize("event_dates, required, expected", [
    (
        [
            date(2017, 5, 20),
            date(2017, 5, 20),
            date(2017, 5, 21),
        ], True, True
    ),
    (
        [
            date(2017, 5, 20),
            date(2017, 5, 24),
            date(2017, 5, 21),
        ], True, False
    ),
    (
        [
            date(2017, 5, 20),
            date(2017, 5, 20),
            date(2017, 5, 21),
        ], False, False
    ),
    (
        [
            date(2017, 5, 20),
            date(2017, 5, 24),
            date(2017, 5, 21),
        ], False, True
    ),
])
def test_duplicate_event_filter_generator(event_dates, required, expected):
    from cnps.filter import duplicate_event_filter_generator
    user = {'event_dates': event_dates}
    f = duplicate_event_filter_generator(required)
    assert f(user) == expected


@pytest.mark.parametrize("event_dates, interval, expected", [
    (
        [
            date(2017, 5, 22),
            date(2017, 5, 20),
            date(2017, 5, 18),
        ], 1, False
    ),
    (
        [
            date(2017, 5, 22),
            date(2017, 5, 20),
            date(2017, 5, 18),
        ], 2, True
    ),
    (
        [
            date(2017, 5, 22),
            date(2017, 5, 20),
            date(2017, 5, 18),
        ], 3, True
    ),
])
def test_recent_event_frequency_filter_generator(event_dates, interval, expected):
    from cnps.filter import recent_event_interval_filter_generator
    user = {'event_dates': event_dates}
    f = recent_event_interval_filter_generator(interval)
    assert f(user) == expected


@pytest.mark.parametrize("event_dates, interval", [
    (
        [
            date(2017, 5, 22),
            date(2017, 5, 20),
            date(2017, 5, 18),
        ], 2.0
    ),
    (
        [
            date(2017, 5, 22),
        ], 0
    ),
    (
        [], 0
    ),
    (
        [
            date(2017, 6, 2),
            date(2017, 6, 1),
            date(2017, 5, 31),
            date(2017, 5, 30),
            date(2017, 5, 29),
        ], 1.0
    ),
])
def test_avg_event_interval(event_dates, interval):
    from cnps.filter import avg_event_interval
    i = avg_event_interval(event_dates)
    assert i == interval


@pytest.mark.parametrize("dates", [
    (
        [
            date(2017, 5, 22),
            date(2017, 5, 20),
            date(2017, 5, 18),
        ]
    ),
    (
        [
            date(2017, 5, 22),
            date(2017, 5, 18),
        ]
    ),
    (
        [
            date(2017, 5, 22),
        ]
    ),
])
def test_group_dates(dates):
    from cnps.filter import _group_dates
    dd = _group_dates(dates)
    print(dd)
