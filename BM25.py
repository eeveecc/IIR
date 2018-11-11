from gensim import corpora
from gensim.summarization import bm25

class BM25:

    def __init__(self, token_list):
        self.token_list = token_list

    def build_model(self):
        corpus = list()
        doc_list = list()
        for token in self.token_list:
            corpus.append(token['term'])
            doc_list.append(token['docID'])
        # build a corpora dictionary and corresponding doc-id index
        dictionary = corpora.Dictionary(corpus)
