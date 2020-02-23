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
  u"cultkorpus",
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
  u"itportal.by",
  u"iloveFSP",
  u"myfreedom.by",
  u"Marketing.by",
  u"gusarovgroup",
  u"truestoryclub",
  u"okt16",
  u"humanlibraryby",
  u"massaraksh.minsk",
  u"prowomenby",
  u"pressclubbelarus",
  u"btnkby",
  u"ShafaMinsk",
  u"FThBelarus",
  u"minsklegalhackers",
  u"salesolution.by",
  u"210metrov",
  u"ideatobiz",
  u"pokateplo",
  u"instinctools.belarus",
  u"minskchangemakers",
  u"HTPCommunity",
  u"onlinerby",
  u"4front",
  u"AEMBelarus",
  u"agileby",
  u"BAinBY",
  u"bygis",
  u"iosby",
  u"free.code.camp.Minsk",
  u"gophers.by",
  u"gowaymeetup",
  u"grodnonetcommunity",
  u"GrodnoBA",
  u"GrodnoIT",
  u"fsharpminsk",
  u"1673382339595171", # rust.by
  u"nlproc.by",
  u"Pro-Net-community-323866207998632",
  u"salesforceprofessionalsby",
  u"SolutionArchitectureGomel",
  u"storm.the.front",
  u"prdrivemedia",
  u"potantseval",
  u"minskcraftbeerfest",
  u"eventminsk.by",
  u"ItBDSMinsk",
  u"mymondayby",
  u"edu4future.by",
  u"minsk.ikraikra",
  u"minskshift",
  u"ideatobiz",
  u"bevisualstudio",
  u"MefodijBookClub",
  u"vulicabrasil",
  u"pokursuby",
  u"ScienceSoftPeople",
  u"beerncider",
  u"scifestby",
  u"lektorij.by",
  u"belarusmini",
  u"pesochnica.minsk",
  u"symbalby",
  u"redjacketsteam",
  u"belarusdigitalconference",
  u"reallyfreemarketminsk",
  u"pasternakmarket",
  u"tedxminsk",
  u"SUPCOMMUNITY",
  u"Andersensoft",
  u"GoodStartBy",
  u"FirstnerBY",
  u"kraftblick",
  u"hrmstudioru",
  u"igrow.by",
  u"quidox.by",
  u"facultativ.by",
  u"cashflowoligarh",
  u"SBHlawBY",
  u"polygonby",
  u"pronetby",
  u"maretskayaschool",
  u"ygallery.by",
  u"Humatheq",
  u"ZISconsultgroup",
  u"fashion.market.by",
  u"confuciustechnic21.10.2014",
  u"gallery.libra",
  u"paralect",
  u"www.nlb.by",
  u"homeperfection.by",
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

# https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def main():
    """"""
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow()
    timeMin = (now.date() - datetime.timedelta(days=15)).isoformat() + 'T00:00:00.000000Z'
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
            calendarId=calendarId, timeMin=timeMin, maxResults=2500, singleEvents=True,
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
    chrome_options.add_argument("--window-size=800x1500")
    chrome_options.add_argument('--no-sandbox') # fix for running from root
    chrome_options.add_argument("-lang=en")

    # download the chrome driver from https://sites.google.com/a/chromium.org/chromedriver/downloads
    chrome_driver = "/usr/bin/chromedriver"

    print('Parsing events.dev.by rss')
    rss = feedparser.parse('https://events.dev.by/rss')
    for e in rss['entries']:
        # stopwords
        bullshit_bingo = False
        for word in STOPWORDS:
            if word in e['title']:
                bullshit_bingo = "Bingo!"
                break

        duplicate = False
        for es in events_summary:
            if levenshtein(e['title'], es) < (len(e['title']) + len(es))*0.3/2:
                duplicate = True
                break

        if bullshit_bingo or duplicate:
            continue
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
            start_date = datetime.datetime.strptime(dates.split('/')[0], "%Y%m%dT%H%M%S")
            finish_date = datetime.datetime.strptime(dates.split('/')[1], "%Y%m%dT%H%M%S")

            # remove courses more than 2 weeks from calendar
            if (finish_date - start_date).days > 14:
                # remove event if it started in the past
                if (now - start_date).days > 0:
                    continue
                # otherwise add only one first day
                finish_date = start_date + datetime.timedelta(days=1)

            event = {
                'summary': e['title'],
                'location': location,
                'description': e['link'] + "\n" + desc,
                'start': {
                    'dateTime': start_date.isoformat(),
                    'timeZone': 'GMT',
                },
                'end': {
                    'dateTime': finish_date.isoformat(),
                    'timeZone': 'GMT',
                }
            }
            event = service.events().insert(calendarId=calendarId, body=event).execute()
            print('Event created: {}'.format(event.get('htmlLink')))

            events_summary.append(e['title'])
        except Exception as er:
            print("Can't add '{}' event".format(e['title']))
            print(event)
            print(er.__doc__)
            #print(er.message)

    # Facebook
    # Facebook closed their graph api so now we would parse it manually
    if FACEBOOK:
        facebook_events = []
        for page in FACEBOOK:
            link = 'https://m.facebook.com/{0}/events'.format(page)
            print('Getting events from {}'.format(link))
            #page = requests.get(link, headers=HEADERS)
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
            driver.get(link)
            # get 14 next events
            ids = re.findall('href="/events/([0-9]*)\?', driver.page_source)
            # Close chrome driver
            driver.close()
            driver.quit()

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

                    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
                    driver.get(link)
                    fields = re.findall('<div class="[^>]*>([^<]*)</div>', driver.page_source)
                    for field in list(fields):
                        for stopword in ('is on Facebook', 'log into Facebook', 'join Facebook today'):
                            if stopword in field:
                                fields.remove(field)

                    print(fields) # for debug
                    event['name'] = h.unescape(re.findall('<title>(.*)</title>', driver.page_source)[0])
                    event['date'] = h.unescape(fields[2])
                    event['place'] = h.unescape(fields[4])
                    event['address'] = h.unescape(fields[5])
                    event['description'] = ''


                    if "UTC" in event['date']:
                        event['timeZone'] = event['date'].split()[-1]
                        event['date'] = event['date'][:-len(event['timeZone'])]
                        if event['timeZone'] != 'UTC':
                            event['timeZone'] += ':00'
                    else:
                        event['timeZone'] = 'UTC+03:00'

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
                    elif ' – ' in event['date']:
                        start, end = event['date'].split('–')
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

                    duplicate = False
                    for es in events_summary:
                        if levenshtein(event['name'], es) < (len(event['name']) + len(es))*0.3/2:
                            duplicate = True
                            break

                    if bullshit_bingo or duplicate:
                        continue
                    elif dateparser.parse(event['start_time']) >= dateparser.parse('today'):
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
                finally:
                    # Close chrome driver
                    driver.close()
                    driver.quit()

    # TODO:
    # http://www.park.by/cat-38/
    # https://citydog.by/afisha/
    # https://everyng.com/place/Belarus/Minsk


if __name__ == '__main__':
    main()
