#!/usr/bin/env python
# -*- encoding: utf-8

import boto3
def get_log_events(log_group, , log_stream_name, start_time=None, end_time=None):
    client = boto3.client('logs')
    kwargs = {
        'logGroupName': log_group,
        'logStreamNames': [
            log_stream_name,
        ],
        'limit': 10000,
    }

    if start_time is not None:
        kwargs['startTime'] = start_time
    if end_time is not None:
        kwargs['endTime'] = end_time

    while True:
        resp = client.filter_log_events(**kwargs)
        yield from resp['events']
        try:
            kwargs['nextToken'] = resp['nextToken']
        except KeyError:
            break

if __name__ == '__main__':
    log_group = '<LOG_GROUP_NAME>'
    log_stream_name = '<LOG_STREAM_NAME>'
    start_time = 1570053600000 # ms_since_epoch https://www.epochconverter.com/?source=searchbar&q=1511213601140
    end_time = 1570068000000 # ms_since_epoch https://www.epochconverter.com/?source=searchbar&q=1511213601140

    logs = get_log_events(
        log_group=log_group,
        start_time=start_time,
        end_time=end_time
    )
    with open("file.txt", "w") as f:
        for event in logs:
            f.write(event['message'].rstrip()+'\n')

