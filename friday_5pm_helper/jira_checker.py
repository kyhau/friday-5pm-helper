from __future__ import print_function
from jira import JIRA
import json
import sys

ARG_SERVER="server"
ARG_UEMAIL="useremail"
ARG_UNAME="username"
ARG_UPASS="userpass"


def init_jira_service(server, uemail, upass):
    """
    This script shows how to connect to a JIRA instance with a
    username and password over HTTP BASIC authentication.
    :param server: JIRA server url
    :param uemail: login email address
    :param upass: pass
    :return: an JIRA object
    """
    return JIRA(
        basic_auth=(uemail, upass),
        options={ 'server': server }
    )


def jira_issues(jira_service, uname):
    """
    :param jira_service:
    :param uname:
    :return:
    """
    issues = jira_service.search_issues(
        'assignee = {} AND updated > startOfWeek(-1w) ORDER BY updated ASC'.format(uname)
    )
    ret_issues = []
    for i in issues:
        fields = i.fields

        worklogs = jira_service.worklogs(i)
        if worklogs:
            for w in worklogs:
                ret_issues.append({
                    'key': i.key,
                    'summary': fields.summary,
                    'worklog_date': w.updated,
                    'worklog_time_spent': worklog_time_spent(w.timeSpentSeconds)
                })
        else:
            ret_issues.append({
                'key': i.key,
                'summary': fields.summary,
                'worklog_date': None,
                'worklog_time_spent': '01:00'
            })

    return ret_issues

def worklog_updated_date(updated_date_str):
    from datetime import datetime
    DATETIME_STR_FORMAT_1 = '%Y-%m-%dT%H:%M:%S+11:00'
    DATETIME_STR_FORMAT_2 = '%Y-%m-%dT%H:%M:%S+10:00'
    for f in [DATETIME_STR_FORMAT_1, DATETIME_STR_FORMAT_2]:
        try:
            updated_dt = datetime.strptime(updated_date_str, f)
            return updated_dt
        except:
            pass
    return None


def worklog_time_spent(time_spent_secs):
    return '{:02d}:{:02d}'.format(time_spent_secs/3600, time_spent_secs%3600/60)


def read_user_profile(conf_json):
    with open(conf_json) as json_file:
        profile_data = json.load(json_file)
        return profile_data


def main():
    if len(sys.argv) != 2:
        print('Usage: {} CONFIG_JSON'.format(sys.argv[0]))
        return 1

    user_profile = read_user_profile(sys.argv[1])

    service = init_jira_service(
        server=user_profile[ARG_SERVER],
        uemail=user_profile[ARG_UEMAIL],
        upass=user_profile[ARG_UPASS]
    )

    issues = jira_issues(service, user_profile[ARG_UNAME])
    for i in issues:
        print('{} {} {} {}'.format(i['key'], i['summary'], i['worklog_date'], i['worklog_time_spent']))

    return 0

if __name__ == '__main__':
    sys.exit(main())