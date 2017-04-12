import bs4
from common import *
from dateutil import parser
import re

def cleanTrack(track):
  if 'grand prix saver' in track.lower():
    return None

  if track.lower().endswith(' track & training'):
    track = track[:-len(' track & training')]
  
  return track

def kindFromDesc(desc):
  kind = Kind.NORMAL
  if 'training' in desc.lower():
    kind = Kind.TRAINING
  return kind

def parse(elem):
  desc = elem.strong.text

  dateplace = elem.find(class_='trackday_list_date').text.split(' | ')
  datestr = re.search('\d.*', dateplace[0]).group(0)
  date = parser.parse(datestr)

  track = cleanTrack(dateplace[1])
  if not track:
    return None

  kind = kindFromDesc(desc)

  url = None
  if elem.a:
    url = 'http://www.focusedevents.com' + elem.a.find_next('a')['href']

  return {
    'company': Company.FOCUSED,
    'date': date,
    'track': track,
    'kind': kind,
    'desc': desc,
    'url': url,
  }

def scrape():
  soup = fetch_soup('focused.html',
                    'http://www.focusedevents.com/uk-bike-trackdays')
  events = map(parse, soup.find_all(class_='trackday_list'))
  return filter(bool, events)

if __name__ == '__main__':
  for e in scrape():
    print e
