import json

data = json.loads(open('wikimovies.json').read())

s = set()
for mov in data['dbs'][0]['films']:
    for x in mov.get('title', []):
        s.add(x)

print json.dumps(list(s))


