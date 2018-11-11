# -*- coding:utf8 -*-
"""
query.py contains search query functions.
"""
import pickle
import os
import re

from collections import Counter


class Query:

    # load the inverted index from local binary file
    def __init__(self):
        try:
            with open('DISK/BLOCKINDEX.pickle', 'rb') as pickle_file:
                self.spimi_model = pickle.load(pickle_file)
            with open('DISK/bm25.pickle', 'rb') as pickle_file:
                self.bm25_model = pickle.load(pickle_file)
            self.average_idf = sum(map(lambda k: float(self.bm25_model['model'].idf[k]), self.bm25_model['model'].idf.keys())) / len(self.bm25_model['model'].idf.keys())
            self.stopword = list()
            with open('data/stopword.txt', 'r') as sw:
                for line in sw:
                    self.stopword.append(line.replace('\n', ''))
        except FileNotFoundError:
            print('Please build the index and BM25 model first.')
            os._exit(1)

    # search and return a list of single word query result
    def search_term(self, query, ranking):
        query = self.__normalize__(query)
        if len(query) == 1:
            try:
                # raw results from SPIMI
                result = self.spimi_model[query[0]]
                # return ranked result using bm25 model
                if ranking:
                    return self.__bm25_rank__(query, result)
                # return raw result without ranking
                else:
                    return sorted(result)
            except KeyError:
                return list()
        else:
            return list()

    # search and return a list of AND query result
    def search_AND(self, query, ranking):
        query = self.__normalize__(query)
        if len(query) >= 1:
            try:
                posting_lists = []
                # raw result of each term
                for term in query:
                    posting_lists.append(self.spimi_model[term])
                # get intersection for AND
                result = set(posting_lists[0])
                for posting in posting_lists[1:]:
                    result.intersection_update(posting)
                # return ranked result using bm25 model
                if ranking:
                    return self.__bm25_rank__(query, result)
                # return raw result without ranking
                else:
                    return sorted(list(result))
            except KeyError:
                return list()
        else:
            return list()

    # search and return a list of OR query result
    def search_OR(self, query, ranking):
        query = self.__normalize__(query)
        if len(query) >= 1:
            try:
                # append all the results of every term in the query
                result = []
                for term in query:
                    result = result + self.spimi_model[term]
                result = [item[0] for item in Counter(result).most_common()]
                # return ranked result using bm25 model
                if ranking:
                    return self.__bm25_rank__(query, result)
                # return raw result without ranking
                else:
                    return result
            except KeyError:
                return list()
        else:
            return list()

    # rank the result using BM25
    def __bm25_rank__(self, query, result):
        # get scores from the bm25 model
        doc_scores = self.bm25_model['model'].get_scores(query, self.average_idf)
        result_scores = dict()
        for doc in result:
            result_scores[doc] = doc_scores[self.bm25_model['doc_index'].index(doc)]
        return sorted(result_scores, key=result_scores.get)

    # normalize query
    def __normalize__(self, query):
        query = query.split(',')
        new_query = list()
        for term in query:
            term = re.sub('\t|-|,|\.|\n', ' ', term)
            # replace parenthesis, <>, slashes to empty
            term = re.sub('/|<|>|\(|\)|\+', '', term)
            # lower case the string
            term = term.lower()
            # replace all numbers to empty
            term = re.sub('\d+', '', term)
            # replace multiple spaces to one space
            term = re.sub('\s+', ' ', term)
            if term != '':
                new_query.append(term)
        for stopword in self.stopword:
            try:
                query = [value for value in new_query if value != stopword]
            except ValueError:
                pass
        return query


