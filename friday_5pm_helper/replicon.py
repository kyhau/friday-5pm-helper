from __future__ import print_function
import sys

from replicon_services.client import RepliconClient
from replicon_services.utils import *
from replicon_services import service_defs


def print_time_entry_list(time_entry_list):
    for i in time_entry_list:
        print(i['entryDate'])
        print(i['interval'])
        for m in i['customMetadata']:
            if m['keyUri'] == "urn:replicon:time-entry-metadata-key:task":
                print('Task: {}'.format(m['value']))
            elif m['keyUri'] == "urn:replicon:time-entry-metadata-key:comments":
                print('Comment: {}'.format(m['value']))
        print(i['uri'])
        print('---------------------------------------------')


def main():
    if len(sys.argv) != 2:
        print('Usage: {} CONFIG_JSON'.format(sys.argv[0]))
        return 1

    user_profile = read_user_profile(sys.argv[1])

    replicon_client = RepliconClient(
        company_key=user_profile[ARG_COMPANY_KEY],
        login_name=user_profile[ARG_UNAME],
        login_pass=user_profile[ARG_UPASS]
    )

    request_data = service_defs.get_user_2(replicon_client.login_name)
    user_uri = replicon_client.process_request(request_data)['uri']
    print(user_uri)

    request_data = service_defs.get_timesheet_for_date_2(user_uri, 2016, 10, 24)
    ret = replicon_client.process_request(request_data)
    timesheet_uri = ret['timesheet']['uri']
    print(timesheet_uri)

    request_data = service_defs.get_time_entries_for_user_and_date_range(
        replicon_client.login_name, 2016, 10, 24, 2016, 10, 24
    )
    time_entry_list = replicon_client.process_request(request_data)
    print_time_entry_list(time_entry_list)

    request_data = service_defs.put_time_entry(replicon_client.login_name, 2016, 10, 31, 1, 0, task_uri="")
    ret = replicon_client.process_request(request_data)
    print(ret)

    return 0

if __name__ == '__main__':
    sys.exit(main())