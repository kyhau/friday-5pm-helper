import json
import uuid

from collections import namedtuple
from datetime import datetime, timedelta


TimeEntryData = namedtuple('TimeEntryData', 'year month day interval comment taskid')

EXPECTED_DATETIME_FORMATS = [
    '%Y-%m-%dT%H:%M:%S+11:00',
    '%Y-%m-%dT%H:%M:%S+10:00',
    '%Y-%m-%dT%H:%M:%S.%f+11:00',
    '%Y-%m-%dT%H:%M:%S.%f+10:00',
    '%Y-%m-%d'
]


def unique_unit_of_work_id():
    return uuid.uuid4().hex


def worklog_time_spent(time_spent_secs):
    return '{:02d}:{:02d}'.format(time_spent_secs / 3600, time_spent_secs % 3600 / 60)


def worklog_date(updated_date_str):
    if updated_date_str is not None:
        for f in EXPECTED_DATETIME_FORMATS:
            try:
                updated_dt = datetime.strptime(updated_date_str, f)
                return updated_dt
            except Exception as e:
                pass

        try:
            parts = updated_date_str.split('-')
            d_part = parts[2].split('T')[0]
            return datetime(int(parts[0]), int(parts[1]), int(d_part))
        except Exception as e:
            pass

        print('Error: unable to parse {}. Use now time.'.format(updated_date_str))
    return datetime.now()


def start_and_end_of_week_of_a_day(a_day):
    # monday is 0, sunday is 7
    day_of_week = a_day.weekday()

    to_beginning_of_week = timedelta(days=day_of_week)
    beginning_of_week = a_day - to_beginning_of_week
    beginning_of_week = beginning_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    to_end_of_week = timedelta(days=6 - day_of_week)
    end_of_week = a_day + to_end_of_week
    end_of_week = end_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

    return (beginning_of_week, end_of_week)


def read_json(input_json_file):
    with open(input_json_file) as json_file:
        data = json.load(json_file)
        return data
