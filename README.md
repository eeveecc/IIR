# IIR - SPIMI

Some cool implementation of information retrieval.

## To run the application
- install the dependencies with `pip install -r requirements.txt`
- run `python -m main init -b {block_size} -m {memory_size}` to build the inverted index and BM25 model. The `{memory_size}` is optional and by default it will take the value of the free memory of your computer.
- run `python -m main {word,and,or} {-r} QUERY` for searching. Note that for `word` the system treat the query as a term. with `-r` option the search results will be ranked using BM25 scoring model.

## Test Queries
- Single word query: `python -m main word america`
- AND query: `python -m main and america,china`
- OR query: `python -m main or america,china`

## Test Results

america (without ranking)

```
python -m main word america

Found 399 results:
[2, 50, 51, 74, 79, 224, 382, 397, 412, 474, 478, ...]
```

america (with ranking)

```
python -m main word -r america
Found 399 results:
[17357, 6657, 7135, 12277, 3534, 6896, 5004, 4969, 5473, ...]
```

america&&china (without ranking)

```
python -m main and america,china
Found 6 results:
[7578, 10302, 10347, 14858, 15472, 18473]
```

america&&china (with ranking)

```
python -m main and -r america,china
Found 6 results:
[14858, 10347, 10302, 7578, 15472, 18473]
```

america||china (without ranking)

```
python -m main or america,china
Found 687 results:
[7578, 10302, 10347, 14858, 15472, 18473, 2, 50, 51, 74, 79, 224, ...]
```

america||china (with ranking)

```
python -m main or america,china
Found 687 results:
[17357, 6657, 7135, 12277, 3534, 6896, 5004, 4969, 5473, 1579, 8483, 12848, ...]
```

Democrats’(without ranking)

```
python -m main word Democrats'
Found 85 results:
[28, 219, 234, 1416, 1786, 1857, 1895, 1900, 1908, 1999, 2011, 2132, 2140, ...]
```

Democrats' (with ranking)

```
python -m main word Democrats' -r
Found 85 results:
[21508, 1895, 9848, 15369, 12773, 9774, 10905, 18731, 14419, 1786, 15154, ...]
```

