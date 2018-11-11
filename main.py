# -*- coding:utf8 -*-
"""
main.py is the driver of the application
"""
from preprocessor import Preprocessor
from model.SPIMI import SPIMI
from model.BM25 import BM25
from cli import Cli
from query import Query
import psutil


if __name__ == '__main__':

    # create and parse user input using command line
    args = Cli.create_parser().parse_args()
    # build the inverted index
    if args.subparser_name == 'init_spimi':
        if args.block_size is not None:
            p = Preprocessor('./data/Reuter21578/')
            p.extract()
            p.process()
            s = SPIMI(p.token_list)
            if args.memory_size is None:
                args.memory_size = psutil.virtual_memory().available
            s.invert(int(args.memory_size), int(args.block_size))
            b = BM25(p.token_list)
            b.build_model()
        else:
            print('Please define memory size and block size.')
    else:
        # set param to True to enable bm25 ranking
        q = Query()
        result = None
        if args.subparser_name == 'word':
            result = q.search_term(args.QUERY)
        if args.subparser_name == 'and':
            result = q.search_AND(args.QUERY)
        if args.subparser_name == 'or':
            result = q.search_OR(args.QUERY)
        print('Found ' + str(len(result)) + ' results:')
        print(result)

