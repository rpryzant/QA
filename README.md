# QA

## IDEAS

### WikiMovies KB + generated questions
**Pros**
* some initial progress
* semantically interesting topic (people like movies)

**Cons**
* Graph sparsity

### Ice's dataset ([paper](https://nlp.stanford.edu/software/sempre/wikitable/))
**Pros**
* the data is there

**Cons**
* too small: 20k questions
* IR-heavy task where simple algos can do very well
* small splash

### WebQueryTable + (turk/generated) questions ([paper](https://arxiv.org/pdf/1706.02427.pdf))
**Pros**
* 200k tables to generate questions from

**Cons**
* IR-heavy
* many tables may not be interesting
* small splash

### Large open DB + generated questions (wikitable/dbpedia)
**Pros**
* dense graph
* open domain
* would make a _big_ splash

**Cons**
* ingesting the KB would be hard and take time
* scaling to massive kb's requires significant algorithmic innovation, might detract from _reasoning_


### SAT solver: find short stories + generate questions
**Pros**
* dense graphs
* encoding is easy (not as much of an IR focus)
* would make a _big_ splash

**Cons**
* where to get stories? reddit? generate them? have turkers write them?
* how to get questions? generated from kb? turkers (how to encourage compositionality)? 

