# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


def test_find_user_urls():
    from ratemall.connpass import find_user_urls
    with open('./data/connpass_user_list.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        urls = find_user_urls(soup)
        for u in urls:
            print(u)
    assert False


def test_find_user_detail():
    with open('./data/connpass_user_detail.html') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        event_date = soup.find_all('div', class_='event_schedule_area')
        for e in event_date:
            year = e.find('p', class_='year').text
            date = e.find('p', class_='date').text
            print("{0}/{1}".format(year, date))
        social_links = soup.find('span', class_='social_link').find_all('a')
        for i in social_links:
            print(i['href'])
    assert False
