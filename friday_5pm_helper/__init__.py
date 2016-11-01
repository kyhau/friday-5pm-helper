import json
from collections import namedtuple
from datetime import datetime, timedelta


TimeEntryData = namedtuple('TimeEntryData', 'year month day interval comment task_uri')

EXPECTED_DATETIME_FORMATS = [
    '%Y-%m-%dT%H:%M:%S+11:00',
    '%Y-%m-%dT%H:%M:%S+10:00',
    '%Y-%m-%d'
]


def worklog_time_spent(time_spent_secs):
    return '{:02d}:{:02d}'.format(time_spent_secs / 3600, time_spent_secs % 3600 / 60)


def worklog_date(updated_date_str):
    for f in EXPECTED_DATETIME_FORMATS:
        try:
            updated_dt = datetime.strptime(updated_date_str, f)
            return updated_dt
        except:
            pass
    return datetime.now()


def start_and_end_of_week_of_a_day(a_day):
    # monday is 0, sunday is 7
    day_of_week = a_day.weekday()

    to_beginning_of_week = timedelta(days=day_of_week)
    beginning_of_week = a_day - to_beginning_of_week

    to_end_of_week = timedelta(days=6 - day_of_week)
    end_of_week = a_day + to_end_of_week

    return (beginning_of_week, end_of_week)


def read_json(input_json_file):
    with open(input_json_file) as json_file:
        data = json.load(json_file)
        return data
