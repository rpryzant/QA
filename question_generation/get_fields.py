import json
import sys


data = json.loads(open(sys.argv[1]).read())

def fields_for_attr(a):
    s = set()
    # TODO -- multiple actors??
    for mov in data['dbs'][0]['films']:
        for x in mov.get(a, []):
            s.add(x)

    return json.dumps(list(s))



print """
        "title": %s,
        "release_year": %s,
        "in_language": %s,
        "has_imdb_votes": %s,
        "has_imdb_rating": %s,
        "has_genre": %s,
        "starred_actors": %s,
        "written_by": %s,
        "directed_by": %s
""" % (
    fields_for_attr("title"),
    fields_for_attr("release_year"),
    fields_for_attr("in_language"),
    fields_for_attr("has_imdb_votes"),
    fields_for_attr("has_imdb_rating"),
    fields_for_attr('has_genre'),
    fields_for_attr('starred_actors'),
    fields_for_attr('written_by'),
    fields_for_attr('directed_by'),
)


