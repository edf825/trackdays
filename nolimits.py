import bs4
from common import *
from dateutil import parser
import re

def toKind(kind):
  if kind == '21':
    return Kind.EVENING
  elif kind == '22':
    return Kind.NORMAL
  elif kind == '38':
    return Kind.OPL
  elif kind == '56':
    return Kind.RBO
  return None

def parse(event):
  url = event.a['href']
  date = re.search('date=([0-9\-]+)', url).group(1)
  track = event.h3.contents[0].strip()
  desc = event.find_next('span').contents[0].strip()
  kind = toKind(re.search('event=(\d+)', url).group(1))

  if not kind:
    return None

  return {
    'company': Company.NO_LIMITS,
    'date': parser.parse(date),
    'track': track,
    'kind': kind,
    'desc': desc
  }

def scrape():
  soup = fetch_soup('nolimits.html',
                    'https://nolimitstrackdays.com/events-list.html')
  events = map(parse, soup.find_all(class_='event'))
  return filter(bool, events)

if __name__ == '__main__':
  for e in scrape():
    print e
