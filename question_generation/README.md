## Question Generation

Generates questions from wikimovies

### make wikimovies DB

```
python ingest_wikimovies.py [raw wikimovies kb] wikimovies.json
python get_db_relationships.py wikimovies.json > relationships
# copy-paste `relationships` into end of wikimovies.json
```

TODO -- ingest and get relationships in one step


### make metadata file

```
python get_metadata_types.py wikimovies.json
```


### Generate questions

```
python generate_questions.py
```


TODO
summarize current state


- speedup
- randomize order
- relations
- actor/director/writer/year centric questions? (i think this is done)

