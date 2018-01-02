## Question Generation

Generates questions from wikimovies

### make wikimovies json DB

```
python ingest_wikimovies.py [raw wikimovies kb] wikimovies.json
python get_db_relationships.py wikimovies.json > relationships
# copy-paste `relationships` into end of wikimovies.json
```

TODO -- ingest and get relationships in one step


### get variable types

```
python get_metadata_types.py wikimovies.json
# copy-paste these ouputs into metadata.json
```


### Generate questions

```
python generate_questions.py
```


## TODOs

- speedup
- randomize order
- relations with multiple hops
- actor/director/writer/year (i.e. non-movie) centric questions? (this might be done)
- handling missing question fields
- synonyms
- what to do with multiple-value attributes 
- make "year" an int instead of its own datatype?
