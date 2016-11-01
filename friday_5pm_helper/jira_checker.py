from __future__ import print_function
from jira import JIRA
import sys

from friday_5pm_helper import (
    TimeEntryData,
    worklog_date,
    worklog_time_spent,
    read_json
)

# Default client credentials file
JIRA_JSON = 'client_secret_jira.json'

# Arguments defined in the client credential file
ARG_SERVER="server"
ARG_UEMAIL="useremail"
ARG_UNAME="username"
ARG_UPASS="userpass"


class JiraClient():
    def __init__(self, server, uemail, upass):
        """
        Prepares connection to a JIRA instance with a username and password
        over HTTP BASIC authentication.
        :param server: JIRA server url
        :param uemail: login email address
        :param upass: password
        """
        self.service = JIRA(
            basic_auth=(uemail, upass),
            options={ 'server': server }
        )

    def jira_issues_updated_since_start_of_week(self, uname):
        """
        :param jira_service:
        :param uname: user name
        :return:
        """
        issues = self.service.search_issues(
            'assignee = {} AND updated > startOfWeek(-1w) ORDER BY updated ASC'.format(uname)
        )
        ret_issues = []
        for i in issues:
            fields = i.fields

            worklogs = self.service.worklogs(i)
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


def retrieve_jira_issues_updated_since_start_of_week(client_secret_json=JIRA_JSON):
    """
    Retrieve jira issues' data in TimeEntryData format
    :return: list of TimeEntryData
    """
    user_profile = read_json(client_secret_json)

    service = JiraClient(
        server=user_profile[ARG_SERVER],
        uemail=user_profile[ARG_UEMAIL],
        upass=user_profile[ARG_UPASS]
    )

    time_entry_data_list = []

    issues = service.jira_issues_updated_since_start_of_week(user_profile[ARG_UNAME])
    for i in issues:
        updated_date = worklog_date(i['worklog_date'])

        time_entry_data_list.append(TimeEntryData(
            year=updated_date.year,
            month=updated_date.month,
            day=updated_date.day,
            interval=i['worklog_time_spent'],
            comment='{} {}'.format(i['key'], i['summary']),
            task_uri='TODO'
        ))

    return time_entry_data_list


def main():
    retrieve_jira_issues_updated_since_start_of_week()
    return 0

if __name__ == '__main__':
    sys.exit(main())