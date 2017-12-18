Script that parse multiple sites and add events into [Minsk Geek Events
](https://calendar.google.com/calendar/embed?src=58deqgrcqbv4eup0l07s0pnid0%40group.calendar.google.com&ctz=Europe/Minsk) google calendar

Requirements:

* python libraries  
python2:  
```
sudo apt-get install python-googleapi python-feedparser python-requests python-bs4
```
python3:  
```
sudo apt-get install python3-googleapi python3-feedparser python3-requests python3-bs4
```

* Goodle API Credentials  
[Turn on the Google Calendar API](https://developers.google.com/google-apps/calendar/quickstart/python)

* Facebook API Credentials  
For accessing Facebook API eventer use [facebook application credentials](https://developers.facebook.com/docs/facebook-login/access-tokens#apptokens).  
You should [create your one](https://developers.facebook.com/apps) and store it in `facebook.json` near main script:
```
{"app_id": "123456789012345", "app_secret": "<long hash>"}
```

* Goodle API Autorization  
Run it first time manually
```
python eventer.py --noauth_local_webserver
```

Current sources of events:
- https://www.facebook.com/imaguruby
- https://www.facebook.com/eventspace.by
- https://www.facebook.com/loftbalki
- https://www.facebook.com/pg/john.galt.space.minsk
- http://www.facebook.com/cech.by
- https://www.facebook.com/HTPBelarus
- https://www.facebook.com/cultcenterkorpus
- https://www.facebook.com/komn302
- https://www.facebook.com/Talaka.by
- https://www.facebook.com/hs.minsk
- https://www.facebook.com/falanster.by
- https://www.facebook.com/MinskPythonMeetup
- https://www.facebook.com/minskruby
- https://www.facebook.com/MinskJS
- https://www.facebook.com/BelarusJavaUserGroup
- https://www.facebook.com/UXBelarus
- https://www.facebook.com/groups/DataTalks
- https://www.facebook.com/groups/391132934426041 # devopsby
- https://www.facebook.com/Scala-Enthusiasts-Belarus-137171759692484
- https://facebook.com/modxby
- https://www.facebook.com/groups/AzureBelarus
- https://www.facebook.com/groups/opendataby
- https://www.facebook.com/comaqa.by
- https://www.facebook.com/groups/gdgminsk
- https://www.facebook.com/groups/webnotbombs
- https://www.facebook.com/groups/dotnet.minsk
- https://www.facebook.com/groups/funcby
- https://www.facebook.com/groups/TheRollingScopes
- https://www.facebook.com/BelarusKUG
- https://www.facebook.com/javaprofessionalsby
- https://www.facebook.com/groups/MinskCSS
- https://www.facebook.com/groups/minsk.user.group
- https://www.facebook.com/inproductshoes
- https://events.dev.by/rss