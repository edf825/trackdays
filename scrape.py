import json

import focused
import msv
import nolimits
import trackdays
import uktrackdays

days = focused.scrape() +       \
       msv.scrape() +           \
       nolimits.scrape() +      \
       trackdays.scrape() +     \
       uktrackdays.scrape()

# apparently datetimes aren't json friendly. hrm.
def jsonify(day):
  day['date'] = day['date'].strftime('%Y-%m-%d')
  day['kind'] = int(day['kind'])
  day['company'] = int(day['company'])
  return day

days = map(jsonify, days)
days = sorted(days, key=lambda x: x['date'])

with open('docs/trackdays.json', 'w') as fd:
  fd.write(json.dumps(days, sort_keys=True, indent=4, separators=(',', ': ')))
