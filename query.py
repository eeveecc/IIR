# -*- coding:utf8 -*-
"""
query.py contains search query functions.
"""
import pickle
from collections import Counter


class Query:

    # load the inverted index from local binary file
    def __init__(self):
        self.index = None
        try:
            with open('DISK/BLOCKINDEX.pickle', 'rb') as pickle_file:
                self.index = pickle.load(pickle_file)
        except FileNotFoundError:
            print('cant find it.')

    # search and return a list of single word query result
    def search_term(self, term):
        try:
            return sorted(self.index[term.lower()])
        except KeyError:
            return []

    # search and return a list of AND query result
    def search_AND(self, query):
        query_term_list = query.split(',')
        posting_lists = []
        for term in query_term_list:
            posting_lists.append(self.search_term(term))
        result = set(posting_lists[0])
        for posting in posting_lists[1:]:
            result.intersection_update(posting)
        return sorted(list(result))

    # search and return a list of OR query result
    def search_OR(self, query):
        query_term_list = query.split(',')
        result = []
        for term in query_term_list:
            result = result + self.search_term(term)
        return [item[0] for item in Counter(result).most_common()]

    # check if the inverted index is built
    def is_built(self):
        return self.index is not None



