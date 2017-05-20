# -*- coding: utf-8 -*-
import json
from datetime import datetime


def find_user_urls(soup):
    tbl = soup.find('div', class_='lottery_table_area')
    users = tbl.find_all('a', class_='image_link')
    user_urls = []
    for u in users:
        user_urls.append(u['href'])
    return user_urls


def find_user_details(soup, user_url):
    event_dates = []
    event_dates_soup = soup.find_all('div', class_='event_schedule_area')
    for e in event_dates_soup:
        year = e.find('p', class_='year').text
        date = e.find('p', class_='date').text
        dt = datetime.strptime("{0}/{1}".format(year, date), '%Y/%m/%d')
        event_dates.append(dt)

    social_links = []
    social_links_soup = soup.find('span', class_='social_link').find_all('a')
    for link in social_links_soup:
        url = link['href']
        if 'twitter' in url:
            social_links.append({'twitter': url})
        elif 'facebook' in url:
            social_links.append({'facebook': url})
        elif 'github' in url:
            social_links.append({'github': url})

    user_id = user_url.replace('https://connpass.com/user/', '').strip('/')
    return {
        'user_url': user_url,
        'user_id': user_id,
        'event_dates': event_dates,
        'social_links': social_links,
    }


class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)
