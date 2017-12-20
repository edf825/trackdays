import bs4
from common import *
from enum import IntEnum
import requests
import sys

DEBUG = False

class Kind(IntEnum):
  NORMAL = 1
  EVENING = 2
  OPL = 3
  RBO = 4
  NOVICE = 5
  TRAINING = 6

class Company(IntEnum):
  MSV = 0
  NO_LIMITS = 1
  FOCUSED = 2
  TRACKDAYS = 3
# All from uktrackdays -- a subset of trackdays.co.uk.
# CASTLE_COMBE = 4
# SILVERSTONE = 5
# PHIL_BEVAN = 6
# BIKEDAYS_CO = 7

def fetch_soup(filename, url):
  if DEBUG:
    with open(filename) as fd:
      return bs4.BeautifulSoup(fd.read(), 'html.parser')
  else:
    r = requests.get(url)
    if r.status_code != 200:
      raise Exception('uh oh, server returned sadness')
    return bs4.BeautifulSoup(r.text, 'html.parser')
