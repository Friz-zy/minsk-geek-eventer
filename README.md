# [minsk-geek-eventer](https://l.facebook.com/l.php?u=https%3A%2F%2Fcalendar.google.com%2Fcalendar%2Fembed%3Fsrc%3D58deqgrcqbv4eup0l07s0pnid0%2540group.calendar.google.com%26ctz%3DEurope%2FMinsk&h=ATP_AzmO6kCEaJJVY3plDj1OBqIk1sHV6WJgpqgTDyK9gB1R4e3qvRv9UuqmiwKRYTsorgaZ4bIVJFGIdO-xFOXxYu26ehdAxoroYaXpogkcSa6euzxKB0cwVWy8EyWl9fI9_5aD6rdyBnWLaG42cNXOnIneWKfdme2OvcqxLzMdCFSY0uDAiNSbzNXHXKp8h9rBsPGURF6Rz0DrIF6sCJKyTyLXm7_3sD2edl74vAoNGmhG66lkMujdqS31jSQgwHJO4S2Xsn-YhAimbT3WPjvnHVNYEHpY6QT3Qw)
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