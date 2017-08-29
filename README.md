# minsk-geek-eventer
Script that parse multiple sites and add events into google calendar

Requirements:

* python libraries  
```
python2: sudo apt-get install python-googleapi python-feedparser python-requests python-bs4
```
```
python3: sudo apt-get install python3-googleapi python3-feedparser python3-requests python3-bs4
```

* Goodle API Credentials  
[Turn on the Google Calendar API](https://developers.google.com/google-apps/calendar/quickstart/python)

* Goodle API Autorization  
Run it first time manually
```
python eventer.py --noauth_local_webserver
```

Current sources of events:
- https://events.dev.by/rss