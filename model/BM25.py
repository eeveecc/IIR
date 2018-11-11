from gensim.summarization import bm25
import time
import pickle
import os

class BM25:

    def __init__(self, token_list):
        self.token_list = token_list
        if not os.path.exists('DISK'):
            os.makedirs('DISK')

    def build_model(self):
        doc_corpus = list()
        doc_list = list()
        print('Building BM25 Model.........')
        print('Building corpus format for gensim........')
        tic = time.clock()
        for token in self.token_list:
            if token['docID'] not in doc_list:
                doc_list.append(token['docID'])
                doc_corpus.append(list())
            doc_corpus[doc_list.index(token['docID'])].append(token['term'])
        print('Corpus size: ' + str(len(doc_corpus)))
        print('Document size: ' + str(len(doc_corpus)))
        print('Note that corpus size should be equal to document size.')
        bm25_model = bm25.BM25(doc_corpus)
        print('BM25 Model is built after ' + str(time.clock() - tic))
        print('Saving BM25 model to binary.........')
        bm25_model_with_index = {
            'model': bm25_model,
            'doc_index': doc_list
        }
        with open('DISK/bm25.pickle', 'wb+') as pickle_file:
            pickle.dump(bm25_model_with_index, pickle_file)

