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
import feedparser
import requests
import json
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

FACEBOOK= [
  u"imaguruby",
  u"eventspace.by",
  u"loftbalki",
  u"john.galt.space.minsk",
  u"cech.by",
  u"HTPBelarus",
  u"cultcenterkorpus",
  u"komn302",
  u"Talaka.by",
  u"hs.minsk",
  u"falanster.by",
  u"MinskPythonMeetup",
  u"minskruby",
  u"MinskJS",
  u"BelarusJavaUserGroup",
  u"UXBelarus",
  u"DataTalks",
  u"391132934426041", #devopsby
  u"Scala-Enthusiasts-Belarus-137171759692484",
  u"modxby",
  u"AzureBelarus",
  u"opendataby",
  u"comaqa.by",
  u"gdgminsk",
  u"webnotbombs",
  u"dotnet.minsk",
  u"funcby",
  u"TheRollingScopes",
  u"BelarusKUG",
  u"javaprofessionalsby",
  u"MinskCSS",
  u"minsk.user.group",
  u"inproductshoes",
  u"kurilka.minsk",
  u"delaisvoedelo",
  u"ReveraLawFirm",
  u"VilgertsBelarus",
  u"34travel",
  u"probusiness.io",
  u"cyberfund",
  u"blockchainmeetups",
]

STOPWORDS = [
  u"Обучение английскому в онлайн-школе Skyeng",
  u"KinoKORPUS",
]


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
    now = datetime.datetime.utcnow().date().isoformat() + 'T00:00:00.000000Z' # 'Z' indicates UTC time
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

    today = datetime.datetime.today()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)

    # Facebook
    try:
        print('Getting Facebook oauth tocken')
        facebook = json.load(open('facebook.json'))
        oauth = requests.get('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&' +
                             'client_id={0}&client_secret={1}'.format(facebook['app_id'], facebook['app_secret']))
        facebook.update(json.loads(oauth.text))
    except:
        print("Can't get facebook oauth token")
        facebook= False
    if facebook:
        facebook_events = []
        for page in FACEBOOK:
            print('Getting events from https://facebook.com/{}'.format(page))
            next = 'https://graph.facebook.com/v2.11/{0}/events?access_token={1}'.format(page, facebook['access_token'])
            while next:
                r = requests.get(next)
                data = json.loads(r.text)
                if 'data' in data:
                    facebook_events.extend(data['data'])
                if 'paging' in data and 'next' in data['paging']:
                    next = data['paging']['next']
                else:
                    next = ''
        # [u'description', u'start_time', u'place', u'end_time', u'id', u'name']
        for event in facebook_events:
            # stopwords
            bullshit_bingo = False
            for word in STOPWORDS:
                if word in event['name']:
                    bullshit_bingo = "Bingo!"
                    break
            if bullshit_bingo:
                continue
            elif (event['name'] not in events_summary and 'end_time' in event and
                  datetime.datetime.strptime(event['end_time'][0:10], "%Y-%m-%d") >= today):
                try:
                    location = event['place']['name']
                    if 'location' in event['place']:
                        location = ", ".join((
                            event['place']['name'],
                            event['place']['location']['street'],
                            event['place']['location']['city'],
                            event['place']['location']['country']
                            ))
                    link = 'https://www.facebook.com/events/{}/'.format(event['id'])

                    calendar_event_data = {
                        'summary': event['name'],
                        'location': location,
                        'description': link + "\n\n" + event['description'],
                        'start': {
                            'dateTime': event['start_time'],
                        },
                        'end': {
                            'dateTime': event['end_time'],
                        }
                    }
                    calendar_event = service.events().insert(calendarId=calendarId, body=calendar_event_data).execute()
                    print('Event created: {}'.format(calendar_event.get('htmlLink')))

                    events_summary.append(event['name'])
                except Exception as er:
                    print("Can't add '{}' event".format(event['name'].encode('utf8')))
                    print(event)
                    print(er.__doc__)
                    print(er.message)

    print('Parsing events.dev.by rss')
    rss = feedparser.parse('https://events.dev.by/rss')
    for e in rss['entries']:
        # Disable this source for now
        break

        # stopwords
        bullshit_bingo = False
        for word in STOPWORDS:
            if word in e['title']:
                bullshit_bingo = "Bingo!"
                break
        if bullshit_bingo:
            continue
        elif e['title'] not in events_summary:
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
                        'timeZone': 'Europe/Minsk',
                    },
                    'end': {
                        'dateTime': datetime.datetime.strptime(dates.split('/')[1], "%Y%m%dT%H%M%S").isoformat(),
                        'timeZone': 'Europe/Minsk',
                    }
                }
                event = service.events().insert(calendarId=calendarId, body=event).execute()
                print('Event created: {}'.format(event.get('htmlLink')))

                events_summary.append(e['title'])
            except Exception as er:
                raise
                print("Can't add '{}' event".format(e['title']))
                print(event)
                print(er.__doc__)
                print(er.message)


    # TODO:
    # http://www.park.by/cat-38/
    # https://citydog.by/afisha/
    # https://everyng.com/place/Belarus/Minsk


if __name__ == '__main__':
    main()
