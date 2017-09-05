# -*- coding: utf-8 -*-
import json
from datetime import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup


def find_user_urls(soup):
    # check lottery first
    tbls = soup.find_all('div', class_='lottery_table_area')
    if tbls is None:
        tbl = soup.find('div', class_='participation_table_area')

    user_urls = []
    for tbl in tbls:
        users = tbl.find_all('a', class_='image_link')
        for u in users:
            user_urls.append(u['href'])
    return user_urls


def find_user_event_details(soup, user_url):
    events = _parse_event(soup)

    page_area = soup.find('div', class_='paging_area')
    if page_area is None:
        return events

    page_count = 0
    for i in page_area.find_all('li'):
        if i.text != '次へ>>':
            page_count += 1

    page_limit = min(page_count, 3)
    for i in range(1, page_limit):
        page_num = i + 1
        event_res = requests.get(user_url, params={'page': page_num})
        soup = BeautifulSoup(event_res.text, 'html.parser')
        evt = _parse_event(soup)
        events.extend(evt)
        sleep(1)
    return events


def _parse_event(soup):
    event_dates = []
    event_dates_soup = soup.find_all('div', class_='event_list vevent')
    for e in event_dates_soup:
        year = e.find('p', class_='year').text
        date = e.find('p', class_='date').text
        status = e.find('p', class_='label_status_tag').getText()

        status_label = ''
        if status == 'キャンセル':
            status_label = 'canceled'
        elif status == '補欠':
            status_label = 'on_waitlist'
        elif status == '申込済':
            status_label = 'applyed'
        elif status == '抽選中':
            status_label = 'in_lottery'

        dt = datetime.strptime("{0}/{1}".format(year, date), '%Y/%m/%d')
        event_dates.append({'status': status_label, 'date': dt})
    return event_dates


def find_user_details(soup, user_url):
    social_links = {}
    social_links_soup = soup.find('span', class_='social_link').find_all('a')
    for link in social_links_soup:
        url = link['href']
        if 'twitter' in url:
            social_links['twitter'] = url
        elif 'facebook' in url:
            social_links['facebook'] = url
        elif 'github' in url:
            social_links['github'] = url

    summary_tabs = ['events', 'own_events', 'presentations', 'bookmarks']
    summary_soup = soup.find('ul', class_='square_tab tab_length_four_parts clearfix mb_15')
    counters = summary_soup.find_all('span', class_='num')
    summary = {}
    for idx, count in enumerate(counters):
        summary[summary_tabs[idx]] = int(count.text)

    user_id = user_url.replace('https://connpass.com/user/', '').strip('/')
    return {
        'user_url': user_url,
        'user_id': user_id,
        'social_links': social_links,
        'num_events': summary['events'],
        'num_own_events': summary['own_events'],
        'num_presentations': summary['presentations'],
        'num_bookmarks': summary['bookmarks'],
    }


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)
