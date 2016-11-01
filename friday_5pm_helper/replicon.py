from __future__ import print_function
import sys

from datetime import datetime

import friday_5pm_helper.gcalendar as g
import friday_5pm_helper.jira_checker as j
from friday_5pm_helper import read_json, start_and_end_of_week_of_a_day
from friday_5pm_helper.replicon_services import service_defs
from friday_5pm_helper.replicon_services.client import RepliconClient

# Default client credentials file
REPLICON_JSON = 'client_secret_replicon.json'

# Need to change the account from SSO to Replicon account
# See https://www.replicon.com/help/what-account-should-we-use-for-integrations
# Arguments defined in the client credential file
ARG_COMPANY_KEY="company_key"
ARG_UNAME="login_name"
ARG_UPASS="login_pass"


def retrieve_user_data(start_date, end_date):
    """
    Retrieves user data from different sources.
    :return: a list of TimeEntryData
    """
    # Retrieve calendar events
    print('Retrieving Google Calendar event data ...')
    time_entry_data_list = g.retrieve_gcalendar_event_data(start_date, end_date)
    for i in time_entry_data_list:
        print(i)

    print('Retrieving JIRA issues being updated since the start of the week ...')
    time_entry_data_list_2 = j.retrieve_jira_issues_updated_since_start_of_week()
    for i in time_entry_data_list_2:
        print(i)

    return time_entry_data_list + time_entry_data_list_2


def create_replicon_time_entries(replicon_client, time_entry_data_list):
    """
    :param replicon_client: a RepliconClient object
    :param time_entry_data_list: list of TimeEntryData to be pushed
    :return: result
    """
    print('Creating replicon time entries ...')
    for i in time_entry_data_list:
        try:
            interval_parts = i.interval.split(':')

            request_data = service_defs.put_time_entry(
                login_name=replicon_client.login_name,
                y=i.year,
                m=i.month,
                d=i.day,
                hrs=int(interval_parts[0]),
                mins=int(interval_parts[1]),
                task_uri=i.task_uri
            )
            ret = replicon_client.process_request(request_data)
            print(ret)

        except Exception as e:
            print('Error {}'.format(e))


def retrieve_user_uri(replicon_client):
    """
    Retrieve time enties
    :param replicon_client: a RepliconClient object
    :return: user uri
    """
    print('Retrieving user uri for login name {} ...'.format(replicon_client.login_name))
    request_data = service_defs.get_user_2(replicon_client.login_name)
    user_uri = replicon_client.process_request(request_data)['uri']
    print(user_uri)
    return user_uri


def retrieve_timesheet_uri(replicon_client, user_uri, y, m, d):
    """
    Retrieve timesheet uri
    :param replicon_client: a RepliconClient object
    :param user_uri: user uri
    :param y: year
    :param m: month
    :param d: day
    :return: timesheet uri
    """
    print('Retrieving timesheet uri for {}-{}-{} ...'.format(y, m, d))
    request_data = service_defs.get_timesheet_for_date_2(user_uri, y, m, d)
    ret = replicon_client.process_request(request_data)
    timesheet_uri = ret['timesheet']['uri']
    print(timesheet_uri)
    return timesheet_uri


def retrieve_time_entry_list(replicon_client, login_name, start_date, end_date):
    request_data = service_defs.get_time_entries_for_user_and_date_range(
        replicon_client.login_name,
        start_date.year, start_date.month, start_date.day,
        end_date.year, end_date.month, end_date.day
    )
    time_entry_list = replicon_client.process_request(request_data)
    print_time_entry_list(time_entry_list)
    return time_entry_list


def print_time_entry_list(time_entry_list):
    for i in time_entry_list:
        print('---------------------------------------------')
        print('Entry {}:'.format(i))
        print(i['entryDate'])
        print(i['interval'])
        for m in i['customMetadata']:
            if m['keyUri'] == "urn:replicon:time-entry-metadata-key:task":
                print('Task: {}'.format(m['value']))
            elif m['keyUri'] == "urn:replicon:time-entry-metadata-key:comments":
                print('Comment: {}'.format(m['value']))
        print(i['uri'])


def main():

    # Retrieve the start date (Monday) and end date (Sunday) of this week
    (start_date, end_date) = start_and_end_of_week_of_a_day(datetime.utcnow())

    # Retrieve user data
    time_entry_data_list = retrieve_user_data(start_date, end_date)

    # Prepare connection to replicon
    user_profile = read_json(REPLICON_JSON)
    replicon_client = RepliconClient(
        company_key=user_profile[ARG_COMPANY_KEY],
        login_name=user_profile[ARG_UNAME],
        login_pass=user_profile[ARG_UPASS]
    )

    # Create and push new time entries
    #create_replicon_time_entries(replicon_client, time_entry_data_list)

    # Retrieve time entries from Replicon
    retrieve_time_entry_list(replicon_client, replicon_client.login_name, start_date, end_date)

    return 0

if __name__ == '__main__':
    sys.exit(main())