from __future__ import print_function
from collections import namedtuple


RequestData = namedtuple('RequestData', 'service_url data')


def get_user_2(login_name):
    return RequestData(
        service_url= 'UserService1.svc/GetUser2',
        data={"user": {"loginName": login_name}}
    )


def get_timesheet_for_date_2(user_uri, y, m, d):
    return RequestData(
        service_url='TimesheetService1.svc/GetTimesheetForDate2',
        data={
            "userUri": user_uri,
            "date": {
                "year": y,
                "month": m,
                "day": d
            }
        }
    )

def get_time_entries_for_user_and_date_range(
        login_name, start_y, start_m, start_d, end_y, end_m, end_d
):
    return RequestData(
        service_url='TimeEntryService3.svc/GetTimeEntriesForUserAndDateRange',
        data={
            "user": {
                "loginName": login_name,
            },
            "dateRange": {
                "startDate": {
                    "year": start_y,
                    "month": start_m,
                    "day": start_d
                },
                "endDate": {
                    "year": end_y,
                    "month": end_m,
                    "day": end_d
                }
            }
        }
    )

def put_time_entry(login_name, y, m, d, hrs, mins, task_uri, comment, unique_unit_of_work_id):
    return RequestData(
        service_url='TimeEntryService3.svc/PutTimeEntry',
        data={
            "timeEntry": {
                "target": {
                },
                "user": {
                    "loginName": login_name,
                },
                "entryDate": {
                    "year": y,
                    "month": m,
                    "day": d
                },
                "timeAllocationTypeUris": [
                    "urn:replicon:time-allocation-type:attendance",
                    "urn:replicon:time-allocation-type:project"
                ],
                "interval": {
                    "hours": {
                        "hours": hrs,
                        "minutes": mins,
                        "seconds": "0",
                    },
                },
                "customMetadata": [
                    {
                        "keyUri": "urn:replicon:time-entry-metadata-key:task",
                        "value": {
                            "uri": task_uri,
                        }
                    },
                    {
                        "keyUri": "urn:replicon:time-entry-metadata-key:comments",
                        "value": {
                            "text": comment
                        }
                    }
                ],
                "extensionFieldValues": []
            },
            "unitOfWorkId": unique_unit_of_work_id
        }
    )

def get_timesheet_summary(timesheet_uri):
    return RequestData(
        service_url='TimesheetService1.svc/GetTimesheetSummary',
        data={
            "timesheetUri": timesheet_uri
        }
    )

def get_standard_timesheet_2(timesheet_uri):
    return RequestData(
        service_url='TimesheetService1.svc/GetStandardTimesheet2',
        data={
            "timesheetUri": timesheet_uri
        }
    )
