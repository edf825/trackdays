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

def modify(event, meta):
  if meta == 'n':
    event['kind'] = Kind.NOVICE
  elif meta == 'e':
    event['kind'] = Kind.EVENING
  elif meta == 'eve':
    event['kind'] = Kind.EVENING
  elif meta == 'opl':
    event['kind'] = Kind.OPL
  elif meta == 'rbo':
    event['kind'] = Kind.RBO
# *shrug*
  elif meta == 'q':
    pass
  elif meta == 'bsb':
    pass
  elif meta == 'am':
    pass
  else:
    return False

  return True

def parse(elem):
  if not elem.a:
    return None

# Grab the URL, which has all the data we need
# Always of the form: /bike/calendar/2017/apr/15-sn-n.aspx
# Where 'sn' is the track (Snetterton 300)
# and 'n' is a type modifier (Novice)
  url = elem.a['href']
  match = re.search('(\d\d\d\d/.*/\d+)(.*)\.aspx', url)
  if not match:
    print 'FAILED TO MATCH ', url
    return None

  date = parser.parse(match.group(1))
  meta = match.group(2).strip('-').split('-')
  desc = elem.a.parent.find_previous('td').contents[0]

# First segment is always the track
  track = get_track(meta[0])
  if not track:
    raise Exception('Failed to resolve track ' + meta[0])

  event = {
    'company': Company.MSV,
    'date': date,
    'track': track,
    'kind': Kind.NORMAL,
    'desc': desc,
    'url': 'http://www.msvtrackdays.com' + url
  }

  for m in meta[1:]:
    if not modify(event, m):
# And by `unsupported', I mostly mean `I'm not interested in this'.
      print 'Metadata unsupported: ' + m
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
