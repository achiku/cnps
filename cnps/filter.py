# -*- coding: utf-8 -*-
import json
from datetime import datetime


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


def recent_event_frequency_filter_generator(interval):
    def f(user):
        return True
    return f
