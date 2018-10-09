from preprocessor import Preprocessor
from SPIMI import SPIMI
from cli import Cli
from query import Query


if __name__ == '__main__':

    args = Cli.create_parser().parse_args()
    if args.subparser_name == 'init':
        if args.memory_size is not None and args.block_size is not None:
            p = Preprocessor('./data/Reuter21578/')
            p.extract()
            p.process()
            s = SPIMI(p.token_list)
            s.invert(int(args.memory_size), int(args.block_size))
        else:
            print('Please define memory size and block size.')
    else:
        q = Query()
        if q.is_built():
            if args.subparser_name == 'word':
                print(q.search_term(args.QUERY))
            if args.subparser_name == 'and':
                print(q.search_AND(args.QUERY))
            if args.subparser_name == 'or':
                print(q.search_OR(args.QUERY))
        else:
            print('Please use \'init\' command to build the inverted index first.')

