## Question Generation

Generates questions from wikimovies

#### Usage

Run `python generate_questions.py`, which will dump output into `questions.json`. 

`generate_questions.py` takes two input files:

1. an _input scene file_ which contains a structured db. You can prepare the raw wikimovies kb with `ingest_wikimovies.py` (see file for usage).
2. a _metadata file_, which lists the various 

TODO finish


Ingest raw wikimovie data into a CLEVR-style "scene"

```
python ingest_wikimovies.py [raw wikimovies kb] [output destination] 
```





TODO
summarize current state


- speedup
- randomize order
- relations
- actor/director/writer/year centric questions? (i think this is done)

