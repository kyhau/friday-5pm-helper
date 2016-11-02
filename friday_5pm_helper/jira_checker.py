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
            'assignee = {} AND updated > startOfWeek(-1w) AND status not in (Open, Reopened) ORDER BY updated ASC'.format(uname)
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
                        'worklog_time_spent': worklog_time_spent(w.timeSpentSeconds),
                        'components': fields.components
                    })
            else:
                ret_issues.append({
                    'key': i.key,
                    'summary': fields.summary,
                    'worklog_date': None,
                    'worklog_time_spent': '01:00',
                    'components': fields.components
                })

        return ret_issues


def find_task_id(issue, tasks_info):
    # TODO
    # Need a better way to filter jiras and mapping to replicon tasks

    for k, v in tasks_info.iteritems():
        if v['key'] == 'component' and v['value'] in issue['components']:
            return v['taskid']

    return tasks_info['Development']['taskid']


def retrieve_jira_issues_updated_since_start_of_week(
        start_date, end_date, tasks_info, client_secret_json=JIRA_JSON
):
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

        # the issue may have been updated this week but the worklog may be created much earlier
        if start_date > updated_date or updated_date > end_date:
            continue

        time_entry_data_list.append(TimeEntryData(
            year=updated_date.year,
            month=updated_date.month,
            day=updated_date.day,
            interval=i['worklog_time_spent'],
            comment='{} {}'.format(i['key'], i['summary']),
            taskid=find_task_id(i, tasks_info)
        ))

    return time_entry_data_list


def main():
    from datetime import datetime
    from friday_5pm_helper import start_and_end_of_week_of_a_day

    today = datetime.utcnow()
    (start_date, end_date) = start_and_end_of_week_of_a_day(today)
    print(start_date, end_date)

    tasks_info = read_json('client_replicon_configs.json')['tasks']['jira']
    ret = retrieve_jira_issues_updated_since_start_of_week(start_date, end_date, tasks_info=tasks_info)
    for r in ret:
        print(r)
    return 0

if __name__ == '__main__':
    sys.exit(main())