from __future__ import print_function
import json
import requests

from friday_5pm_helper.replicon_services import SWIMLANE_FINDER_URL, HEADERS


# Need to change the account from SSO to Replicon account
# See https://www.replicon.com/help/what-account-should-we-use-for-integrations


class RepliconClient():
    def __init__(self, company_key, login_name, login_pass):
        self.company_key = company_key
        self.login_name = login_name
        self.login_pass = login_pass
        self.swimlane = self.__init_swimlane()

    def __init_swimlane(self):
        """

        :return:
        """
        try:
            # Getting the Swimlane information of the Company Key
            swimlaneFinderJsonBody = {}
            swimlaneFinderJsonBody['tenant'] = { 'companyKey': self.company_key }

            swimlaneFinder = requests.post(
                SWIMLANE_FINDER_URL,
                headers=HEADERS,
                data=json.dumps(swimlaneFinderJsonBody)
            )
            swimlaneFinder = swimlaneFinder.json()

            if swimlaneFinder.get('error'):
                print('Error: {0}'.format(swimlaneFinder.get('error')))
                return None

            swimlane = swimlaneFinder['d']['applicationRootUrl']
            return swimlane
        except Exception, e:
            print('Error: {0}'.format(e))


    def process_request(self, request_data):
        """
        :param request_data: RequestData object
        :return: response data in dict
        """
        try:
            response = self.post_request(
                request_data.service_url,
                request_data.data
            )
            ret_data = response.json()

            if ret_data.get('error'):
                print('Error: {0}'.format(ret_data.get('error')))
                return None
            return ret_data['d']

        except Exception, e:
            print('Error: {0}'.format)

    def post_request(self, service_url, service_data):
        """
        :param service_url:
        :param service_data:
        :return:
        """
        target_url = '{}/services/{}'.format(self.swimlane, service_url)
        return requests.post(
            target_url,
            data=json.dumps(service_data),
            headers=HEADERS,
            auth=(self.company_key + '\\' + self.login_name, self.login_pass)
        )
