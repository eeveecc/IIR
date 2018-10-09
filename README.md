# IIR - SPIMI

Some cool implementation of information retrieval.

## To run the application
- install the dependencies with `pip install -r requirements.txt`
- run `python -m main init -b {block_size} -m {memory_size}` to build the inverted index. The `{memory_size}` is optional and by default it will take the value of the free memory of your computer.
- run `python -m main {word,and,or} QUERY` for searching. Note that for `word` the system treat the query as a term.

## Test Queries
- Single word query: `python -m main word america`
- AND query: `python -m main and america,china`
- OR query: `python -m main or america,china`

