import json

data = json.loads(open('wikimovies.json').read())

s = set()
for mov in data['films']:
    for x in mov.get('has_imdb_rating', []):
        s.add(x)

print json.dumps(list(s))


