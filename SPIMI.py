# -*- coding:utf8 -*-
import pickle
import os
import time


class SPIMI:

    def __init__(self, token_list):
        self.token_list = token_list
        self.block_list = []
        self.dictionary = {}
        if not os.path.exists('DISK'):
            os.makedirs('DISK')

    def invert(self, memory_size, block_size):
        tic = time.clock()
        init_memory_size = memory_size
        dictionary = {}
        for token in self.token_list:
            if memory_size >= block_size:
                self.__add_to_dictionary__(dictionary, token)
                memory_size -= 4
            else:
                self.__save_block__(dictionary, str(len(self.block_list) + 1))
                self.block_list.append('BLOCK' + str(len(self.block_list) + 1))
                dictionary = {}
                memory_size = init_memory_size
                self.__add_to_dictionary__(dictionary, token)
                memory_size -= 4
        self.__save_block__(dictionary, str(len(self.block_list) + 1))
        print(str(len(self.block_list)) + ' blocks files are saved.')
        self.__merge_block__()
        toc = time.clock()
        print('Invert finished after ' + str(toc - tic))

    def __merge_block__(self):
        print('Merging all blocks......')
        for block in self.block_list:
            with open('DISK/' + block + '.pickle', 'rb') as pickle_file:
                block_dictionary = pickle.load(pickle_file)
                for term, docID in block_dictionary.items():
                    if term in self.dictionary:
                        self.dictionary[term] = self.dictionary[term] + block_dictionary[term]
                    else:
                        self.dictionary[term] = block_dictionary[term]
        print('Merged completed.')
        self.__save_block__(self.dictionary, 'INDEX')

    def __save_block__(self, dictionary, name):
        with open('DISK/BLOCK' + name + '.pickle', 'wb+') as pickle_file:
            pickle.dump(dictionary, pickle_file)

    def __add_to_dictionary__(self, dictionary, token):
        # check if term is exist
        if token['term'] not in dictionary:
            dictionary[token['term']] = []
        # check if docID is duplicated
        if token['docID'] not in dictionary[token['term']]:
            dictionary[token['term']].append(token['docID'])




