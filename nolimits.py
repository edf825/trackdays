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

def parse(elem):
  url = elem.a['href']
  date = re.search('date=([0-9\-]+)', url).group(1)
  track = elem.find('h1').contents[0].strip()
  desc = elem.find('p').contents[0].strip()
  kind_id = re.search('event=(\d+)', url).group(1).strip()
  kind = toKind(kind_id)

  if not kind:
    print "couldn't get kind from {!r}; kind id = {!r}".format(url, kind_id)
    return None

  return {
    'company': Company.NO_LIMITS,
    'date': parser.parse(date),
    'track': track,
    'kind': kind,
    'desc': desc,
    'url': 'http://nolimitstrackdays.com' + url,
  }

def scrape():
  soup = fetch_soup('nolimits.html',
                    'https://nolimitstrackdays.com/events-list.html')
  events = map(parse, soup.find_all(class_='event-block'))
  return filter(bool, events)

if __name__ == '__main__':
  for e in scrape():
    print e
