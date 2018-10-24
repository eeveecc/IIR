# -*- coding:utf8 -*-
"""
SPIMI.py contains all the implementation of SPIMI algorithm
"""
import pickle
import os
import time
import re


class SPIMI:

    # init and create DISK directory, take token stream as param
    def __init__(self, token_list):
        self.token_list = token_list
        self.block_list = []
        self.dictionary = {}
        self.memory_size = None
        if not os.path.exists('DISK'):
            os.makedirs('DISK')

    # invert index, take memory_size and block_size as params
    def invert(self, memory_size, block_size):
        print('Inverting the docs......')
        print('Word stream size: ' + str(len(self.token_list)))
        print('Free memory: ' + str(memory_size))
        tic = time.clock()
        init_memory_size = memory_size
        self.memory_size = memory_size
        dictionary = {}
        for token in self.token_list:
            # keep adding to dictionary if memory is good
            if self.memory_size >= block_size*24:
                self.__add_to_dictionary__(dictionary, token)
            # if memory is not enough, save the current dictionary to a binary file and clean the memory
            else:
                self.__save_block__(dictionary, str(len(self.block_list) + 1))
                self.block_list.append('BLOCK' + str(len(self.block_list) + 1))
                dictionary = {}
                self.memory_size = init_memory_size
                self.__add_to_dictionary__(dictionary, token)
        # save the non-full dictionary to a binary as well
        self.__save_block__(dictionary, str(len(self.block_list) + 1))
        self.block_list.append('BLOCK' + str(len(self.block_list) + 1))
        print(str(len(self.block_list) + 1) + ' blocks files are saved.')
        # merge all the dictionaries and save to a binary file
        self.__merge_block__()
        toc = time.clock()
        print('Invert finished after ' + str(toc - tic))
        dict_stat = [0, 0]
        for term in self.dictionary.keys():
            dict_stat[0] += 1
            dict_stat[1] += len(self.dictionary[term])
        print('Terms: ' + str(dict_stat[0]))
        print('Postings: ' + str(dict_stat[1]))

    # merge all the dictionaries and save to a binary file
    def __merge_block__(self):
        print('Merging all blocks......')
        # read all block binaries
        for block in self.block_list:
            with open('DISK/' + block + '.pickle', 'rb') as pickle_file:
                block_dictionary = pickle.load(pickle_file)
                for term, docID in block_dictionary.items():
                    # if term exists, add to the posting list
                    if term in self.dictionary:
                        self.dictionary[term] = self.dictionary[term] + block_dictionary[term]
                    # if not, add the term and create posting list
                    else:
                        self.dictionary[term] = block_dictionary[term]
        print('Merged completed.')
        # save to binary
        self.__save_block__(self.dictionary, 'INDEX')

    # helper method to save binary
    def __save_block__(self, dictionary, name):
        with open('DISK/BLOCK' + name + '.pickle', 'wb+') as pickle_file:
            pickle.dump(dictionary, pickle_file)

    # add to dictionary method
    def __add_to_dictionary__(self, dictionary, token):
        # check if term is exist
        if token['term'] not in dictionary:
            dictionary[token['term']] = []
            self.memory_size -= 20
        # check if docID is duplicated
        if token['docID'] not in dictionary[token['term']]:
            dictionary[token['term']].append(token['docID'])
            self.memory_size -= 4




