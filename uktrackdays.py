import bs4
from common import *
from dateutil import parser
import re

def commentToCompany(comment):
  soup = bs4.BeautifulSoup(comment, 'html.parser')
  content = soup.td.contents[0].lower()

  if content.startswith('castle combe'):
    return Company.CASTLE_COMBE
  elif content.startswith('bikedays.co'):
    return Company.BIKEDAYS_CO
  elif content.startswith('phil bevan'):
# These are all dupes of trackdays.co.uk days.
    return None
  elif content.startswith('silverstone'):
# Also duped at trackdays.co.uk.
    return None
  elif content.startswith('no limits'):
# We already scrape No Limits.
    return None
  raise Exception('Unknown company ' + content)

def parse(elem):
# Source company isn't shown on the page, but appears in a comment.
  comment = elem.find(text=lambda x:isinstance(x, bs4.Comment))
  company = commentToCompany(comment)

  if not company:
    return None

  cells = elem.findAll('td')

  date = parser.parse(cells[0].a.contents[0])
  track = cells[1].a.contents[0].strip()
# TODO -- all listings are full day at the moment
  kind = cells[4].contents[0]

  return {
    'company': company,
    'date': date,
    'track': track,
    'kind': Kind.NORMAL,
    'desc': 'No description available'
  }

def scrape():
  soup = fetch_soup('uktrackdays.html',
#'http://www.uktrackdays.co.uk/uktrackdays.php?action=VE&bike=1')
    'http://www.uktrackdays.co.uk/uktrackdays.php?action=VE&bike=1')
#  print soup.prettify()
  elems = soup.find_all('tr', valign='center')
  events = map(parse, elems)
  return filter(bool, events)

if __name__ == '__main__':
  for e in scrape():
    print e
