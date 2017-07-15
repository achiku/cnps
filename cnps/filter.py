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
        if key == 'events':
            d = [
                {'date': datetime.strptime(t['date'], "%Y-%m-%d %H:%M:%S"), 'status': t['status']}
                for t in value
            ]
            json_dict[key] = d
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


def _group_dates(dates):
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


def avg_event_interval(dates):
    sum_diff = timedelta()
    dates = _group_dates(dates)
    for x, y in dates:
        sum_diff = sum_diff + (x - y)
    if len(dates) == 0:
        return 0
    avg_interval = float(sum_diff.days) / float(len(dates))
    return avg_interval


def recent_event_interval_filter_generator(interval):
    def f(user):
        event_dates = [t['date'] for t in user['events']]
        avg_interval = avg_event_interval(event_dates)
        if avg_interval <= interval:
            return True
        return False
    return f


def event_tab_count_filter_generator(target, required):
    def f(user):
        if user[target] > 0:
            return True
        if not required:
            return True
        return False
    return f


def duplicate_event_filter_generator(required):
    def f(user):
        event_dates = user['events']
        for dt in event_dates:
            count = sum([1 for d in event_dates if d == dt])
            if count >= 2 and required:
                return True
            elif count >= 2 and not required:
                return False
        if not required:
            return True
        return False
    return f
