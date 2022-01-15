#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import dateparser
import feedparser
import requests
import json
import time
import re


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
CLIENT_CREDENTIALS_FILE = 'client_credentials.json'
APPLICATION_NAME = 'Minsk Geek Eventer'
CALENDAR = 'Minsk Geek Events'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    store = Storage(CLIENT_CREDENTIALS_FILE)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + CLIENT_CREDENTIALS_FILE)
    return credentials

def main():
    """"""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    calendarId = 'primary'

    # Fetch all calendars and get id of CALENDAR
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if CALENDAR == calendar_list_entry["summary"]:
                calendarId = calendar_list_entry["id"]
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    print('Getting the already existed events')
    events = []
    page_token = None
    while True:
        eventsResult = service.events().list(
            calendarId=calendarId, maxResults=2500, singleEvents=True,
            orderBy='startTime', pageToken=page_token).execute()
        events.extend(eventsResult.get('items', []))
        page_token = eventsResult.get('nextPageToken')
        if not page_token:
            break

    for n, event in enumerate(events):
        for latest_event in events[n + 1:]:
            if 'dateTime' in event['start'] and 'dateTime' in latest_event['start']:
                if (event['summary'] == latest_event['summary'] and
                    event['start']['dateTime'] == latest_event['start']['dateTime'] ):
                    print("Deleting %s %s event" % (event['start']['dateTime'], event['summary']))
                    try:
                        service.events().delete(calendarId=calendarId, eventId=event['id']).execute()
                        continue
                    except Exception as e:
                        print(e)
                        time.sleep(1)
                        continue
            elif 'date' in event['start'] and 'date' in latest_event['start']:
                if (event['summary'] == latest_event['summary'] and
                    event['start']['date'] == latest_event['start']['date'] ):
                    print("Deleting %s %s event" % (event['start']['date'], event['summary']))
                    try:
                        service.events().delete(calendarId=calendarId, eventId=event['id']).execute()
                        continue
                    except Exception as e:
                        print(e)
                        time.sleep(1)
                        continue

if __name__ == '__main__':
    main()
