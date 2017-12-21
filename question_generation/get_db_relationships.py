"""
pulls out relationship information 
from wikimovies json file
"""
import sys
import json
from collections import defaultdict

data = json.loads(open(sys.argv[1]).read())




relationships = defaultdict(list)

# ordinal mappings for comparison 
votes_map = {
    'unknown': 0,
    'unheard of': 1,
    'well known': 2,
    'highly watched': 3,
    'famous': 4
}
rating_map = {
    'bad': 0,
    'okay': 1,
    'good': 2,
    'fantastic': 3
}
# binary attrs have same/different relationships
binary_attrs = [
    'directed_by',
    'in_language',
    'starred_actors',
    'written_by',
]
# ordered attrs have same/bigger/smaller relationships
ordered_attrs = [
    'release_year',
    'has_imdb_votes',
    'has_imdb_rating',
]

# get a comparable attribute value from a movie
def get_val(attr, mov):
    if attr not in mov: return None

    raw_val = mov[attr]

    if attr in binary_attrs:
        return raw_val
    elif attr == 'release_year':
        return int(raw_val[0])
    elif attr == 'has_imdb_votes':
        return votes_map[raw_val[0]]
    elif attr == 'has_imdb_rating':
        return rating_map[raw_val[0]]


for attr in binary_attrs + ordered_attrs:
    # for each movie, compare it to all other movies,
    # and record their relationship
    for i, movi in enumerate(data['dbs'][0]['films']):
        if attr in binary_attrs:
            relationships['same_%s' % attr].append([])
            relationships['different_%s' % attr].append([])
        else:
            relationships['bigger_%s' % attr].append([])
            relationships['same_%s' % attr].append([])
            relationships['smaller_%s' % attr].append([])

        if not attr in movi: continue
        i_val = get_val(attr, movi)

        for j, movj in enumerate(data['dbs'][0]['films']):
            if i == j: continue

            j_val = get_val(attr, movj)

            if attr in binary_attrs:
                # movie i and j are "different" if j lacks the selected attribute
                if j_val is not None and len(set(i_val) & set(j_val)) > 0:
                    relationships['same_%s' % attr][-1].append(j)
                else:
                    relationships['different_%s' % attr][-1].append(j)
            else:
                if not attr in movj: continue

                if j_val == i_val: 
                    relationships['same_%s' % attr][-1].append(j)
                elif j_val > i_val:
                    relationships['bigger_%s' % attr][-1].append(j)
                else:
                    relationships['smaller_%s' % attr][-1].append(j)


print json.dumps({'relationships': relationships})







