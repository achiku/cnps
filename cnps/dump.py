# -*- coding: utf-8 -*-
import click


def find_user_urls(soup):
    tbl = soup.find('div', class_='lottery_table_area')
    users = tbl.find_all('a', class_='image_link')
    user_urls = []
    for u in users:
        user_urls.append(u['href'])
    return user_urls
