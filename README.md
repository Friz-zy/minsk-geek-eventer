Script that parse multiple sites and add events into [Minsk Geek Events
](https://calendar.google.com/calendar/embed?src=58deqgrcqbv4eup0l07s0pnid0%40group.calendar.google.com&ctz=Europe/Minsk) google calendar

Requirements:

* python libraries  
python2:  
```
sudo apt-get install python-pip python-googleapi python-feedparser python-requests python-selenium chromium-chromedriver
sudo pip install dateparser six
```
python3:  
```
sudo apt-get install python3-pip python3-googleapi python3-feedparser python3-requests python3-selenium chromium-chromedriver
sudo pip3 install dateparser six
```

* Goodle API Credentials  
[Turn on the Google Calendar API](https://developers.google.com/google-apps/calendar/quickstart/python)

* Facebook API Credentials
Facebook disabled graph api for applications so now this script just parse the pages directly with chromium-chromedriver and selenium (curl is a very limited option)

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
- https://www.facebook.com/cultkorpus
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
- https://www.facebook.com/kurilka.minsk
- https://www.facebook.com/delaisvoedelo
- https://www.facebook.com/ReveraLawFirm
- https://www.facebook.com/VilgertsBelarus
- https://www.facebook.com/34travel
- https://www.facebook.com/probusiness.io
- https://www.facebook.com/pg/cyberfund
- https://www.facebook.com/blockchainmeetups
- https://www.facebook.com/groups/iot.belarus.community
- https://www.facebook.com/groups/itportal.by
- https://www.facebook.com/groups/iloveFSP
- https://www.facebook.com/myfreedom.by
- https://www.facebook.com/Marketing.by
- https://www.facebook.com/gusarovgroup
- https://www.facebook.com/pg/truestoryclub
- https://www.facebook.com/okt16
- https://www.facebook.com/humanlibraryby
- https://www.facebook.com/massaraksh.minsk
- https://www.facebook.com/prowomenby
- https://www.facebook.com/pg/pressclubbelarus
- https://www.facebook.com/pg/btnkby
- https://www.facebook.com/pg/ShafaMinsk
- https://www.facebook.com/pg/FThBelarus
- https://www.facebook.com/minsklegalhackers
- https://www.facebook.com/salesolution.by
- https://www.facebook.com/210metrov
- https://www.facebook.com/ideatobiz
- https://www.facebook.com/pokateplo
- https://www.facebook.com/instinctools.belarus
- https://www.facebook.com/minskchangemakers/
- https://www.facebook.com/HTPCommunity

- https://events.dev.by/rss

Possible sources:
https://afisha.tut.by/places/concert/
https://afisha.tut.by/concert/
https://citydog.by/afisha/
