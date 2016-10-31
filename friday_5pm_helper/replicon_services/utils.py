from __future__ import print_function
import json


# Need to change the account from SSO to Replicon account
# See https://www.replicon.com/help/what-account-should-we-use-for-integrations
ARG_COMPANY_KEY="company_key"
ARG_UNAME="login_name"
ARG_UPASS="login_pass"


def read_user_profile(conf_json):
    with open(conf_json) as json_file:
        profile_data = json.load(json_file)
        return profile_data
