from preprocessor import Preprocessor
from SPIMI import SPIMI

if __name__ == '__main__':
    p = Preprocessor('./data/Reuter21578/')
    p.extract()
    p.process()
    s = SPIMI(p.token_list)
    s.invert(10000, 5000)