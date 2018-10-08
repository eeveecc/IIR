# -*- coding:utf8 -*-
import time
import os
import re


class Preprocessor:

    def __init__(self, path):
        self.path = path
        self.doc_list = []
        self.token_list = []
        self.stopword = []
        with open('data/stopword.txt', 'r') as sw:
            for line in sw:
                self.stopword.append(line.replace('\n', ''))

    def extract(self):
        META_CHARS = ['&', '<', '>', '\"', '\'', ''];
        META_CHAR_SER = ['&amp;', '&lt;', '&gt;', '&quot;', '&apos;', 'Reuter &#3;']
        print('Reading from ' + self.path + '..........')
        tic = time.clock()
        if os.path.isdir(self.path):
            docID = 1
            for filename in os.listdir(self.path):
                if filename.endswith('sgm'):
                    # clean the doc and convert to plain text with only title and content
                    with open(self.path + filename, 'r', encoding='utf-8', errors='ignore') as f:
                        body_flag = 0
                        output = {}
                        for line in f:
                            if re.match('<TITLE>.*</TITLE>', line):
                                output['title'] = re.sub('<TITLE>|</TITLE>', '', line).replace('\n', '')
                            elif re.match('.*<BODY>.*', line):
                                body_flag = 1
                                output['body'] = line.split('<BODY>')[1]
                            elif re.match('.*</BODY>.*', line):
                                body_flag = 0
                                output['docID'] = docID
                                docID += 1
                                # remove noise
                                for index, char in enumerate(META_CHAR_SER):
                                    output['body'] = output['body'].replace(char, META_CHARS[index])
                                    output['title'] = output['title'].replace(char, META_CHARS[index])
                                self.doc_list.append(output)
                                output = {}
                            elif body_flag == 1:
                                output['body'] += line
                            else:
                                pass
                    break
            tok = time.clock()
            print('Extraction finished after ' + str(tok - tic))
        else:
            print('Path doesn\'t exist, please verify.')

    def process(self):
        if len(self.doc_list) == 0:
            print('Nothing to tokenize.')
        else:
            print('Tokenizing the docs......')
            tic = time.clock()
            # append all data into one string
            for doc in self.doc_list:
                raw_string = self.__normalize__(doc)
                doc_token = self.__tokenize__(raw_string)
                doc_token = self.__remove_stopword__(doc_token)
                for token in doc_token:
                    self.token_list.append({
                        'docID': doc['docID'],
                        'term': token
                    })
            toc = time.clock()
            print('Tokenization finished after ' + str(toc - tic))

    def get_token_list(self):
        return self.token_list

    def __normalize__(self, doc):
        raw_string = re.sub('\t|-|\'|,|\.|\d|/|\n|<|>|\(|\)', ' ', doc['title'] + ' ' + doc['body'])
        raw_string = re.sub('\s+', ' ', raw_string)
        raw_string = raw_string.lower()
        return raw_string

    def __tokenize__(self, raw_string):
        doc_token = raw_string.split(' ')
        try:
            doc_token.remove(' ')
        except ValueError:
            pass
        return doc_token

    def __remove_stopword__(self, doc_token):
        for stopword in self.stopword:
            try:
                doc_token.remove(stopword)
            except ValueError:
                continue
        return doc_token
