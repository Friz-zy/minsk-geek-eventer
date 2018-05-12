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
import re

from six.moves.html_parser import HTMLParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
  u"iot.belarus.community",
]

STOPWORDS = [
  u"Обучение английскому в онлайн-школе Skyeng",
  u"KinoKORPUS",
]

HEADERS = {"Accept-Language": "en"}


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
    h = HTMLParser()

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

    # instantiate a chrome options object so you can set the size and headless preference
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=800x5000")
    chrome_options.add_argument('--no-sandbox') # fix for running from root
    chrome_options.add_argument("-lang=en")

    # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
    chrome_driver = "/usr/lib/chromium-browser/chromedriver"

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)


    # Facebook
    # Facebook closed their graph api so now we would parse it manually
    if FACEBOOK:
        facebook_events = []
        for page in FACEBOOK:
            link = 'https://m.facebook.com/{0}/events'.format(page)
            print('Getting events from {}'.format(link))
            #page = requests.get(link, headers=HEADERS)
            driver.get(link)
            # get 14 next events
            ids = re.findall('href="/events/([0-9]*)\?', driver.page_source)

            for id in ids:
                try:
                    event = {'id': id}
                    link = 'https://m.facebook.com/events/{0}'.format(id)
                    #page = requests.get(link, headers=HEADERS)
                    #event['name'] = h.unescape(re.findall('<title>(.*)</title>', page.text)[0])
                    #event['date'] = h.unescape(re.findall('<div class="[^>]*>([^<]*)</div>', page.text)[0])
                    #event['place'] = h.unescape(re.findall('<div class="[^>]*>([^<]*)</div>', page.text)[2])
                    #event['address'] = h.unescape(re.findall('<div class="[^>]*>([^<]*)</div>', page.text)[3])
                    #event['description'] = ''

                    driver.get(link)
                    event['name'] = h.unescape(re.findall('<title>(.*)</title>', driver.page_source)[0])
                    event['date'] = h.unescape(re.findall('<div class="[^>]*>([^<]*)</div>', driver.page_source)[1])
                    event['place'] = h.unescape(re.findall('<div class="[^>]*>([^<]*)</div>', driver.page_source)[4])
                    event['address'] = h.unescape(re.findall('<div class="[^>]*>([^<]*)</div>', driver.page_source)[5])
                    event['description'] = ''


                    if "UTC" in event['date']:
                        event['timeZone'] = event['date'].split()[-1]
                        event['date'] = event['date'][:-len(event['timeZone'])]
                        if event['timeZone'] != 'UTC':
                            event['timeZone'] += ':00'
                    else:
                        event['timeZone'] = 'UTC'

                    if u'\xb7' in event['date']:
                        start, end = event['date'].split(u'\xb7')[1].split('-')
                        event['start_time'] = dateparser.parse(start).isoformat()
                        event['end_time'] = dateparser.parse(end).isoformat()
                    elif ' - ' in event['date']:
                        start, end = event['date'].split('-')
                        if ' at ' not in end:
                            end = start.split()[:-2] + end.split()
                            end = ' '.join(end)
                        event['start_time'] = dateparser.parse(start).isoformat()
                        event['end_time'] = dateparser.parse(end).isoformat()
                    else:
                        event['start_time'] = dateparser.parse(event['date']).isoformat()
                        event['end_time'] = event['start_time']

                    # stopwords
                    bullshit_bingo = False
                    for word in STOPWORDS:
                        if word in event['name']:
                            bullshit_bingo = "Bingo!"
                            break
                    if bullshit_bingo:
                        continue
                    elif event['name'] not in events_summary and dateparser.parse(event['start_time']) > dateparser.parse('yesterday'):
                        calendar_event_data = {
                            'summary': event['name'],
                            'location': ", ".join((event['place'], event['address'])),
                            'description': link + "\n\n" + event['description'],
                            'start': {
                                'dateTime': event['start_time'],
                                'timeZone': event['timeZone'],
                            },
                            'end': {
                                'dateTime': event['end_time'],
                                'timeZone': event['timeZone'],
                            }
                        }
                        calendar_event = service.events().insert(calendarId=calendarId, body=calendar_event_data).execute()
                        print('Event created: {}'.format(calendar_event.get('htmlLink')))

                        events_summary.append(event['name'])
                        facebook_events.append(event)
                except Exception as er:
                    print("Can't add '{}' event".format(link))
                    print(event)
                    print(er.__doc__)
                    # print(er.message)

    print('Parsing events.dev.by rss')
    rss = feedparser.parse('https://events.dev.by/rss')
    for e in rss['entries']:
        # Enable it back but only while facebook disabled api
        # https://developers.facebook.com/blog/post/2018/04/04/facebook-api-platform-product-changes
        if facebook_events:
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
                        'timeZone': 'GMT',
                    },
                    'end': {
                        'dateTime': datetime.datetime.strptime(dates.split('/')[1], "%Y%m%dT%H%M%S").isoformat(),
                        'timeZone': 'GMT',
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
