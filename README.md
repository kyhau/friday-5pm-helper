# friday-5pm-helper
Scripts for pre-filling Replicon timesheet with Google Calendar events and JIRA entries

## Build
[![Build Status](https://travis-ci.org/kyhau/friday-5pm-helper.svg?branch=master)](https://travis-ci.org/kyhau/friday-5pm-helper)

**Linux**

    virtualenv env
    . env/bin/activate
    pip install -e .
    
    python friday_5pm_helper/replicon.py
    
    # for running pytest
    pip install -r requirements-test.txt
    
    # for full testing with tox and building wheel
    tox -r

**Windows**

    virtualenv env
    env\Scripts\activate
    pip install -e .
    
    python friday_5pm_helper\replicon.py
    
    # for running pytest
    pip install -r requirements-test.txt
    
    # for full testing with tox and building wheel
    tox -r
    
## Prerequisites

1. Copy the example files in `config-example` into your workspace.

2. Update `client_secret_jira.json`, `client_secret_replicon.json` accordingly.

3. Update `client_replicon_configs.json` to map the JIRA tickets to Replicon Task-IDs.

4. Create your Google Calendar API credential (see [Turn on the Google Calendar API](https://developers.google.com/google-apps/calendar/quickstart/python)). 
Copy it to your workspace rename it to `client_secret_gcalendar.json`
   

## Run

**Linux**

    <path-to>/env/bin/replicon-helper
    # or just
    <path-to>/env/bin/gcalender-helper
    # or just
    <path-to>/env/bin/jira-helper

**Windows**

    <path-to>/env/bin/replicon-helper
    # or just
    <path-to>/env/bin/gcalender-helper
    # or just
    <path-to>/env/bin/jira-helper
