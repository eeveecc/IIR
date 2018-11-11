# -*- coding:utf8 -*-
"""
preprocessor.py contains all the functions that used to process the raw data.
"""
import time
import os
import re


class Preprocessor:

    # init function
    def __init__(self, path):
        self.path = path
        self.doc_list = list()
        self.token_list = list()
        self.stopword = list()
        with open('data/stopword.txt', 'r') as sw:
            for line in sw:
                self.stopword.append(line.replace('\n', ''))

    # extract the raw data and convert it into doc_list
    # format:
    # [{
    #   "docID": 1,
    #   "title": "The title of the doc",
    #   "body": "sentence\nin\nthe\ndoc"
    # }]
    def extract(self):
        META_CHARS = ['&', '<', '>', '\"', '\'', '']
        META_CHAR_SER = ['&amp;', '&lt;', '&gt;', '&quot;', '&apos;', 'Reuter &#3;']
        print('Reading from ' + self.path + '..........')
        tic = time.clock()
        if os.path.isdir(self.path):
            for filename in os.listdir(self.path):
                if filename.endswith('sgm'):
                    # clean the doc and convert to plain text with only title, docID and content
                    with open(self.path + filename, 'r', encoding='utf-8', errors='ignore') as f:
                        body_flag = 0
                        output = {}
                        for line in f:
                            # extract the NEWID to be docID
                            if re.findall('NEWID="\d+"', line):
                                output['docID'] = int(re.findall('NEWID="\d+"', line)[0].replace('NEWID="', '').replace('"', ''))
                            # extract the title
                            elif re.match('<TITLE>.*</TITLE>', line):
                                output['title'] = re.sub('<TITLE>|</TITLE>', '', line).replace('\n', '')
                            # starting line of the body
                            elif re.match('.*<BODY>.*', line):
                                body_flag = 1
                                output['body'] = line.split('<BODY>')[1]
                            # end line of the body
                            elif re.match('.*</BODY>.*', line):
                                body_flag = 0
                                # remove noise
                                for index, char in enumerate(META_CHAR_SER):
                                    output['body'] = output['body'].replace(char, META_CHARS[index])
                                    output['title'] = output['title'].replace(char, META_CHARS[index])
                                self.doc_list.append(output)
                                output = {}
                            # extract all lines in body
                            elif body_flag == 1:
                                output['body'] += line
                            # ignore the noise
                            else:
                                pass
            tok = time.clock()
            print('Extraction finished after ' + str(tok - tic))
        else:
            print('Path doesn\'t exist, please verify.')

    # tokenize and normalize the docs and save the results in token_list (aka token stream)
    # format:
    # [{
    #   "docID": 1,
    #   "term": "concordia"
    # }]
    def process(self):
        if len(self.doc_list) == 0:
            print('Nothing to tokenize.')
        else:
            print('Tokenizing the docs......')
            tic = time.clock()
            for doc in self.doc_list:
                raw_string = self.__normalize__(doc)
                doc_token = self.__tokenize__(raw_string)
                for token in doc_token:
                    self.token_list.append({
                        'docID': doc['docID'],
                        'term': token
                    })
            toc = time.clock()
            print('Tokenization finished after ' + str(toc - tic))

    # return token_list (aka token stream)
    def get_token_list(self):
        return self.token_list

    # normalize the string
    def __normalize__(self, doc):
        # combine title and body, then replace all tab and newline to space
        raw_string = doc['title'] + ' ' + doc['body']
        raw_string = re.sub('\t|\n', ' ', raw_string)
        # lower case the string
        raw_string = raw_string.lower()
        # replace all numbers to empty
        raw_string = re.sub('\d+', '', raw_string)
        # replace multiple spaces to one space
        raw_string = re.sub('\s+', ' ', raw_string)
        return raw_string

    # tokenization and remove stop words
    def __tokenize__(self, raw_string):
        doc_token = raw_string.split(' ')
        try:
            doc_token.remove(' ')
        except ValueError:
            pass
        for stopword in self.stopword:
            try:
                doc_token.remove(stopword)
            except ValueError:
                pass
        return doc_token

