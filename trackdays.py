import bs4
from common import *
from dateutil import parser
import re
import requests

def toKind(desc):
  lower = desc.lower()
  if 'evening' in lower:
    return Kind.EVENING
  elif 'novice' in lower:
    return Kind.NOVICE
  elif 'masterclass' in lower:
    return Kind.TRAINING
  elif 'open pitlane' in lower:
    return Kind.OPL
  elif 'road bikes only' in lower:
    return Kind.RBO
  return Kind.NORMAL

def cleanCircuit(circuit, subcircuit):
  circuit = circuit + ' ' + subcircuit
  lower = circuit.lower()
  if lower.endswith(' full circuit'):
    return circuit[:-13]
  if lower.endswith(' circuit'):
    return circuit[:-8]
  return circuit

def inUK(circuit):
  whitelist = [
    'rockingham',
    'bedford',
    'snetterton',
    'donington',
    'silverstone',
    'brands hatch',
    'pembrey',
    'castle combe',
    'cadwell park',
    'croft',
    'anglesey',
    'mallory park',
    'lydden hill',
    'oulton park',
    'blyton park',
  ]

  for ok in whitelist:
    if circuit.lower().startswith(ok):
      return True

  return False

def parse(elem):
  labels = elem.find_all('label')
  if len(labels) < 7:
    return None

  (date, circuit, subcircuit, desc) = map(lambda x: x.contents[0], labels[2:6])

# bleh. filter out the header.
  if date == 'Track':
    return None

  if not inUK(circuit):
    print 'Rejecting track ' + circuit
    return None

  date = parser.parse(date, dayfirst=True)
  kind = toKind(desc)
  circuit = cleanCircuit(circuit, subcircuit)
  url = 'https://www.trackdays.co.uk' + elem.a['href'] if elem.a else None

  return {
    'company': Company.TRACKDAYS,
    'date': date,
    'track': circuit,
    'kind': kind,
    'desc': desc,
    'url': url,
  }

def scrape():
  soup = fetch_soup('trackdays.html',
                    'https://www.trackdays.co.uk/calendar/bikes/')
  elems = soup.find_all(class_='row')
  events = map(parse, elems)
  return filter(bool, events)

if __name__ == '__main__':
  for e in scrape():
    print e
