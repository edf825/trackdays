import bs4
from common import *
from enum import IntEnum
import requests
import sys

DEBUG = False

class Kind(IntEnum):
  NORMAL = 0
  EVENING = 1
  OPL = 2
  RBO = 3
  NOVICE = 4
  TRAINING = 5

class Company(IntEnum):
  MSV = 0
  NO_LIMITS = 1
  TRACKDAYS = 2
  FOCUSED = 3
  CASTLE_COMBE = 4
# Duped at trackdays.co.uk
# SILVERSTONE = 5
# All dupes of trackdays.co.uk
# PHIL_BEVAN = 6
  BIKEDAYS_CO = 7

def fetch_soup(filename, url):
  if DEBUG:
    with open(filename) as fd:
      return bs4.BeautifulSoup(fd.read(), 'html.parser')
  else:
    r = requests.get(url)
    if r.status_code != 200:
      raise Exception('uh oh, server returned sadness')
    return bs4.BeautifulSoup(r.text, 'html.parser')
