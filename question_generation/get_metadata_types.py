"""
pulls out metadata 'type' information 
from wikimovies json file
"""

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
        "relation": ["same_directed_by", "different_directed_by", 
                     "same_starred_actors, "different_starred_actors",
                     "same_written_by", "different_written_by",
                     "bigger_has_imdb_votes", "same_has_imdb_votes", "smaller_has_imdb_votes",
                     "bigger_has_imdb_rating", "same_has_imdb_rating", "smaller_has_imdb_votes",
                     "bigger_release_year", "same_release_year", "smaller_release_year"]
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


