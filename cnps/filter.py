# -*- coding: utf-8 -*-
import json
from datetime import datetime, timedelta


def read_user_data(file_path):
    content = ''
    with open(file_path, 'r') as fh:
        content = fh.read()
    return json.loads(content, object_hook=date_hook)


def date_hook(json_dict):
    for key, value in json_dict.items():
        if key == 'event_dates':
            json_dict[key] = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S") for t in value]
        else:
            pass
    return json_dict


def social_link_filter_generator(target, required=False):
    def f(user):
        links = user['social_links']
        for link in links:
            for k, _ in link.items():
                if k == target and required:
                    return True
                elif k == target and not required:
                    return False
        if not required:
            return True
        return False
    return f


def group_dates(dates):
    p = datetime.now()
    paired_dates = []
    for i, d in enumerate(dates):
        if i == 0:
            p = d
            continue
        else:
            paired_dates.append((p, d))
            p = d
    return paired_dates


def recent_event_frequency_filter_generator(interval):
    def f(user):
        sum_diff = timedelta()
        dates = group_dates(user['event_dates'])
        for x, y in dates:
            sum_diff = sum_diff + (x - y)
        avg_diff = float(sum_diff.days) / float(len(dates))
        if avg_diff >= interval:
            return True
        return False
    return f


def duplicate_event_filter_generator(required):
    def f(user):
        for event_date in user['event_dates']:
            count = sum([1 for d in user['event_dates'] if d == event_date])
            if count >= 2 and required:
                return True
            elif count >= 2 and not required:
                return False
        if not required:
            return True
        return False
    return f
