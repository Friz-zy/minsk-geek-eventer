#!/usr/bin/env python
"""
python-googleapi
python-feedparser
python-requests
python-bs4

python3-googleapi
python3-feedparser
python3-requests
python3-bs4
"""

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import feedparser
import requests
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
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
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
            calendarId=calendarId, timeMin=now, maxResults=2500, singleEvents=True,
            orderBy='startTime', pageToken=page_token).execute()
        events.extend(eventsResult.get('items', []))
        page_token = eventsResult.get('nextPageToken')
        if not page_token:
            break
    events_summary = [e['summary'] for e in events]

    print('Parsing events.dev.by rss')
    rss = feedparser.parse('https://events.dev.by/rss')
    for e in rss['entries']:
        if e['title'] not in events_summary:
            try:
                page = requests.get(e['link'])
                desc = page.text[page.text.find("<div class='text'>")+18:page.text.find("</div>", page.text.find("<div class='text'>"))]
                desc = desc.replace('&laquo;', '"')
                desc = desc.replace('&raquo;', '"')
                desc = desc.replace('&nbsp;', ' ')
                desc = desc.replace('&ndash;', ' - ')
                desc = re.sub(r'\s*<li>', '- ', desc)
                desc = re.sub(r'\s*</li>', '\n', desc)
                desc = re.sub(r'\n\n+', '\n', desc)
                desc = re.sub(r'&.+;', '', desc)
                desc = re.sub(r'<(?!\/?a(?=>|\s.*>))\/?.*?>', '', desc)
                location = page.text[page.text.find("&location=")+10:page.text.find("&", page.text.find("&location=")+10)]
                dates = page.text[page.text.find("dates=")+6:page.text.find("&", page.text.find("dates="))]

                event = {
                    'summary': e['title'],
                    'location': location,
                    'description': e['link'] + "\n" + desc,
                    'start': {
                        'dateTime': datetime.datetime.strptime(dates.split('/')[0], "%Y%m%dT%H%M%S").isoformat(),
                        'timeZone': 'UTC',
                    },
                    'end': {
                        'dateTime': datetime.datetime.strptime(dates.split('/')[1], "%Y%m%dT%H%M%S").isoformat(),
                        'timeZone': 'UTC',
                    }
                }
                event = service.events().insert(calendarId=calendarId, body=event).execute()
                print('Event created: {}'.format(event.get('htmlLink')))

                events_summary.append(e['title'])
            except:
                print("Can't add '{}' event".format(e['title']))
                print(event)
                raise


if __name__ == '__main__':
    main()
