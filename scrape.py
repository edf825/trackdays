import json
from pprint import pprint

import focused
import msv
import nolimits
import trackdays

days = focused.scrape() +       \
       msv.scrape() +           \
       nolimits.scrape() +      \
       trackdays.scrape()

# apparently datetimes aren't json friendly. hrm.
def jsonify(day):
  day['date'] = day['date'].strftime('%Y-%m-%d')
  day['kind'] = int(day['kind'])
  day['company'] = int(day['company'])
  return day

def is_eq(a, b):
  track_len = min(len(a['track'].split(' ')), len(b['track'].split(' ')))
  a_track = a['track'][0:track_len]
  b_track = b['track'][0:track_len]
  return a['date'] == b['date'] and a['kind'] == b['kind'] and a_track == b_track

days = map(jsonify, days)
days = sorted(days, key=lambda x: (x['date'], x['kind'], x['track'], x['company']))

filtered_days = []
for day in days:
  if filtered_days and is_eq(filtered_days[-1], day):
    continue
  filtered_days.append(day)

with open('docs/trackdays.json', 'w') as fd:
  fd.write(json.dumps(days, sort_keys=True, indent=4, separators=(',', ': ')))
