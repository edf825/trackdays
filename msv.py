import bs4
from common import *
from dateutil import parser
import re

def get_track(meta):
  if meta.startswith('bhgp'):
    return 'Brands Hatch Grand Prix'
  elif meta.startswith('bh'):
    return 'Brands Hatch Indy'
  elif meta.startswith('op'):
    return 'Oulton Park'
  elif meta.startswith('cp'):
    return 'Cadwell Park'
# maybe bad assumptions about the track used...
  elif meta.startswith('sn'):
    return 'Snetterton 300'
  elif meta.startswith('dp'):
    return 'Donington Park Grand Prix'
  elif meta.startswith('ba'):
    return 'Bedford Autodrome SW'
  return None

def get_kind(meta):
  if meta == 'n':
    return Kind.NOVICE
  elif meta == 'nov':
    return Kind.NOVICE
  elif meta == 'e':
    return Kind.EVENING
  elif meta == 'eve':
    return Kind.EVENING
  elif meta == 'opl':
    return Kind.OPL
  elif meta == 'rbo':
    return Kind.RBO
  elif meta == 'q':
    return Kind.NORMAL
  elif meta == '3gp':
    return Kind.NORMAL
  elif meta == '4grp':
    return Kind.NORMAL
  elif meta == 'bsb':
    pass
  elif meta == 'am':
    pass
  else:
    return None

def is_int(string):
  try:
    int(string)
    return True
  except ValueError:
    return False

def parse(elem):
  if not elem.a:
    return None

# Grab the URL, which has all the data we need
# Always of the form: /bike/calendar/2017/apr/15-sn-n.aspx
# Where 'sn' is the track (Snetterton 300)
# and 'n' is a type modifier (Novice)
  url = elem.a['href']
  match = re.search('(\d\d\d\d/.*/\d\d?)(.*)\/', url)

  if not match:
    print 'FAILED TO MATCH ', url
    return None

  try:
    date = parser.parse(match.group(1))
  except ValueError:
    print 'Skipping invalid date {}; url = {}'.format(match.group(1), url)
    return None

  meta = match.group(2).strip('-').split('-')
  desc = elem.a.parent.find_previous('td').contents[0]

  event = {
    'company': Company.MSV,
    'date': date,
    'track': None,
    'kind': Kind.NORMAL,
    'desc': desc,
    'url': 'http://www.msvtrackdays.com' + url
  }

  for m in meta:
    track = get_track(m.strip())
    kind = get_kind(m.strip())

    if is_int(m):
      print 'Ignoring number in metadata: {!r}; url {}'.format(m, url)
      continue

    if track:
      event['track'] = track
      continue
    if kind:
      event['kind'] = kind
      continue
    print 'Metadata unsupported: {!r}; url {}'.format(m, url)
    return None

  if not event['track']:
    print 'No track for url ' + url
    return None

  return event

def scrape():
  soup = fetch_soup('msv.html',
                    'http://www.msvtrackdays.com/bike/calendar.aspx')
  events = map(parse, soup.find_all('tr'))
  return filter(bool, events)

if __name__ == '__main__':
  for e in scrape():
    print e
