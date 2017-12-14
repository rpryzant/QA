"""
converts wikimovies-formatted data into structured
JSON for question generation

python ingest_wikimovies.py ../raw_data/movieqa/knowledge_source/wiki_entities/wiki_entities_kb.txt wikimovies.json
"""
import sys
from collections import defaultdict
import json
import time

def parse_kb_entry(kb_entry_str):
    if not kb_entry_str:
        return

    out = {}
    for l in kb_entry_str.split('\n'):
        parts = l.strip().split()
        i, relation = next((i, x) for i, x in enumerate(parts) if '_' in x)
        title = ' '.join(parts[1:i])
        values =  ' '.join(parts[i+1:]).split(', ')

        # skip plot summary -- TODO -- keep this?
        if relation != 'has_plot':
            out[relation] = values
    out['title'] = [title]

    return out




if __name__ == '__main__':
    out = {
        'films': []
        # metadata?
    }
    print 'Parsing raw kb...'
    start = time.time()
    with open(sys.argv[1]) as kb:
        for kb_entry_str in kb.read().split('\n\n'):
            kb_entry = parse_kb_entry(kb_entry_str)
            if kb_entry:
                out['films'].append(kb_entry)
    print 'Done. Took %.2fs, found %d entries' % (time.time() - start, len(out['films']))
    
    print 'Writing to %s' % sys.argv[2]
    with open(sys.argv[2], 'w') as outfile:
        json.dump(out, outfile)























