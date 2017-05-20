# -*- coding: utf-8 -*-
from .filter import avg_event_interval


def format_user_info(u):
    return '{0} {1} {2}'.format(u['user_id'], u['user_url'], avg_event_interval(u['event_dates']))
